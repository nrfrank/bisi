import base64
from unittest.mock import call, patch

import botocore.exceptions
import pytest

from bisi.providers import Aws
from bisi.resources import Dockerfile, Resource, Job, BatchJobConfig, ECRConfig
from bisi.utils import get_git_branch, clean_string


@pytest.mark.unit
class TestAwsProvider:

    @patch('bisi.providers.aws.Aws.push_to_ecr')
    @patch('bisi.providers.aws.Aws.create_batch_job_definition')
    def test_deploy_no_resources(self, batch_mock, ecr_mock):
        Resource.clear_resources()
        aws = Aws('.')
        aws.deploy()
        assert batch_mock.call_count == 0
        assert ecr_mock.call_count == 0

    @patch('bisi.providers.aws.Aws.push_to_ecr')
    @patch('bisi.providers.aws.Aws.create_batch_job_definition')
    def test_deploy_multi(self, batch_mock, ecr_mock):
        Resource.clear_resources()
        d1 = Dockerfile()
        Job(name='test-name1', entrypoint='my/script')
        job2 = Job(name='test-name2', entrypoint='my/script',
                   batch_config=BatchJobConfig(jobQueue='my-queue', jobDefinitionName='name2'))
        job3 = Job(name='test-name3', entrypoint='my/script',
                   batch_config=BatchJobConfig(jobQueue='my-queue', jobDefinitionName='name3'))
        ecr_mock.side_effect = ['repo_name1', 'repo_name2']
        aws = Aws('.')
        aws.deploy()
        assert ecr_mock.call_args_list == [
            call(dockerfile=d1),
            call(dockerfile=d1)
        ]
        assert batch_mock.call_args_list == [
            call(full_repo_name='repo_name1', job=job2),
            call(full_repo_name='repo_name2', job=job3)
        ]

    @patch('bisi.providers.aws.ecr_client')
    def test_ensure_repository_exists_create(self, ecr_mock):
        ecr_mock.describe_repositories.side_effect = botocore.exceptions.ClientError(dict(), '')
        ecr_mock.create_repository.return_value = {'repository': {'repositoryUri': 'my-cool-uri'}}

        assert Aws.ensure_repository_exists(repository_name='my-repo', my='other args') == 'my-cool-uri'

        ecr_mock.describe_repositories.assert_called_with(repositoryNames=['my-repo'])
        ecr_mock.create_repository.assert_called_with(repositoryName='my-repo', my='other args')

    @patch('bisi.providers.aws.ecr_client')
    def test_ensure_repository_exists_repo_exists(self, ecr_mock):
        ecr_mock.describe_repositories.return_value = {'repositories': [{'repositoryUri': 'my-cool-uri'}]}

        assert Aws.ensure_repository_exists(repository_name='my-repo', my='other args') == 'my-cool-uri'

        ecr_mock.describe_repositories.assert_called_with(repositoryNames=['my-repo'])

    @patch('bisi.providers.aws.ecr_client')
    @patch('os.system')
    def test_ensure_ecr_authenticated_pass(self, os_mock, ecr_mock):
        ecr_mock.get_authorization_token.return_value = {
            'authorizationData': [{'authorizationToken': base64.b64encode(b'user:password')}]}
        os_mock.return_value = 0

        Aws.ensure_ecr_authenticated('my://server')

        assert os_mock.call_args == call('docker login --username user --password password my://server')

    @patch('bisi.providers.aws.ecr_client')
    @patch('os.system')
    def test_ensure_ecr_authenticated_pass(self, os_mock, ecr_mock):
        ecr_mock.get_authorization_token.return_value = {
            'authorizationData': [{'authorizationToken': base64.b64encode(b'user:password')}]}
        os_mock.return_value = 1

        with pytest.raises(Exception):
            Aws.ensure_ecr_authenticated('my://server')

    @patch('os.system')
    @patch('bisi.providers.aws.docker_client')
    @patch('bisi.providers.aws.Aws.ensure_repository_exists')
    @patch('bisi.providers.aws.Aws.ensure_ecr_authenticated')
    def test_push_to_ecr(self, ecr_auth_mock, repo_mock, docker_mock, os_mock):
        d1 = Dockerfile(name='my-test-image', ecr_config=ECRConfig(repositoryName='test-repo', other='arg'),
                        extra_tags=['test'])
        repo_mock.return_value = 'account.server.com/bisi'
        docker_mock.api.tag.return_value = True
        os_mock.return_value = 0

        assert Aws.push_to_ecr(d1) == 'account.server.com/bisi'

        assert repo_mock.call_args == call('test-repo', other='arg')
        assert ecr_auth_mock.call_args == call('account.server.com')
        assert docker_mock.api.tag.call_args_list == [
            call('my-test-image:latest', 'account.server.com/bisi', force=True, tag='latest'),
            call(f'my-test-image:{clean_string(get_git_branch())}', 'account.server.com/bisi', force=True,
                 tag=clean_string(get_git_branch())),
            call('my-test-image:test', 'account.server.com/bisi', force=True, tag='test')
        ]
        assert os_mock.call_args_list == [
            call('docker push account.server.com/bisi:latest'),
            call(f'docker push account.server.com/bisi:{clean_string(get_git_branch())}'),
            call('docker push account.server.com/bisi:test')
        ]

    @patch('bisi.providers.aws.Aws.get_ecr_image_digest')
    @patch('bisi.providers.aws.batch_client')
    def test_create_batch_job_definition(self, batch_mock, digest_mock):
        Resource.clear_resources()
        Dockerfile('test-image')
        job = Job('my-job', 'my/script', batch_config=BatchJobConfig('my-queue,', jobDefinitionName='my-test-job'))
        digest_mock.return_value = 'sha256:hash'

        Aws.create_batch_job_definition(job=job, full_repo_name='my-full-repo.name/test-image')

        assert batch_mock.register_job_definition.call_args == \
               call(containerProperties={'vcpus': 2, 'memory': 1024,
                                         'image': 'my-full-repo.name/test-image@sha256:hash'},
                    jobDefinitionName='my-test-job', type='container')

    def test_run_no_resources(self):
        Resource.clear_resources()
        aws = Aws('.')
        with pytest.raises(Exception):
            aws.run('no-name', ['my', 'no', 'args'])

    def test_run_no_batch_config(self):
        Resource.clear_resources()
        Dockerfile()
        Job(name='test-name', entrypoint='entrypoint')
        aws = Aws('.')
        with pytest.raises(AssertionError):
            aws.run('test-name', ['my', 'no', 'args'])

    @patch('bisi.providers.aws.batch_client')
    def test_run_single(self, batch_mock):
        Resource.clear_resources()
        d1 = Dockerfile()
        Job(name='foo', entrypoint='my/script', dockerfile=d1,
            batch_config=BatchJobConfig('some-queue', jobDefinitionName='my-job-name'))
        aws = Aws('.')
        aws.run('foo', ["one arg"])
        assert batch_mock.submit_job.call_args == call(
            jobName='foo', jobQueue='some-queue', jobDefinition='my-job-name',
            containerOverrides={'command': ['my/script', 'one arg'], 'environment': []})

    @patch('bisi.providers.aws.batch_client')
    def test_run_multi(self, batch_mock):
        Resource.clear_resources()
        d1 = Dockerfile(name='docker1', file='fake_dockerfile_one')
        Dockerfile(name='docker2', file='fake_dockerfile_two')
        Job(name='multi', entrypoint='my/script', dockerfile=Dockerfile(name='docker1', file='fake_dockerfile_one'),
            batch_config=BatchJobConfig('some-queue', jobDefinitionName='my-job-name'))
        Resource()
        Job(name='foo', entrypoint='my/script', dockerfile=d1,
            batch_config=BatchJobConfig('some-queue', jobDefinitionName='my-job-name2'))
        aws = Aws('.')
        aws.run('multi', ["one", "two", "three"])
        assert batch_mock.submit_job.call_args == call(
            jobName='multi', jobQueue='some-queue', jobDefinition='my-job-name',
            containerOverrides={'command': ['my/script', "one", "two", "three"], 'environment': []})

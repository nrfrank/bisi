
import os
import pytest

from unittest.mock import patch

from bisi.providers import Local
from bisi.resources import Dockerfile, Job

test_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))


@pytest.mark.integration
class TestLocal:
    def test_build_docker(self):
        provider = Local(project_root_dir=test_project_dir)
        test_dockerfile = Dockerfile(file='Dockerfile', build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})

        provider.build_dockerfile(test_dockerfile)

    @patch('bisi.resources.dockerfile.get_git_branch')
    def test_build_docker_tags(self, branch_patch):
        branch_patch.return_value = 'feature/test'
        provider = Local(project_root_dir=test_project_dir)
        test_dockerfile = Dockerfile(file='Dockerfile', build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})

        provider.build_dockerfile(test_dockerfile)

    def test_build_docker_fail(self):
        provider = Local(project_root_dir=test_project_dir)
        test_dockerfile = Dockerfile(file='bad.Dockerfile', build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})

        with pytest.raises(Exception):
            provider.build_dockerfile(test_dockerfile)

    def test_run_bash(self, capsys):
        provider = Local(project_root_dir=test_project_dir)
        test_dockerfile = Dockerfile(file='Dockerfile', build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})
        test_job = Job(name='test_bash', entrypoint='./test.sh', dockerfile=test_dockerfile)

        provider.run_job(test_job, [])
        assert 'it worked from sh' in capsys.readouterr().out

    def test_run_python(self):
        provider = Local(project_root_dir=test_project_dir)
        test_dockerfile = Dockerfile(file='Dockerfile', build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})
        test_job = Job(name='test_python', entrypoint='./test.py', dockerfile=test_dockerfile)

        provider.run_job(test_job, [])


import os

import pytest

from bisi.providers import Aws, Local
from bisi.resources import Dockerfile, Job, Resource
from bisi.resources.config import BatchJobConfig

test_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))


@pytest.mark.integration
def test_aws_workflow():
    Resource.clear_resources()
    local_provider = Local(project_root_dir=test_project_dir)
    aws_provider = Aws(project_root_dir=test_project_dir)
    test_dockerfile = Dockerfile(file='Dockerfile', build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})
    Job(name='test_bash', entrypoint='./test.sh', dockerfile=test_dockerfile, environment={'TEST': 'Value'},
        batch_config=BatchJobConfig(jobQueue='bisi-test-jq'))

    local_provider.build_dockerfile(dockerfile=test_dockerfile)
    aws_provider.deploy()
    aws_provider.run('test_bash', ['my', 'arg'])

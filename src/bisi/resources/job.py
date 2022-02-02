
from typing import Union, Dict

from bisi.resources import Resource, Dockerfile
from bisi.resources.config import LocalJobConfig, BatchJobConfig, ECRConfig
from bisi.utils import get_git_branch, clean_string, get_project_root_dir


class Job(Resource):

    def __init__(self, name: str, entrypoint: str, dockerfile: Union[str, Dockerfile] = None,
                 environment: Dict[str, str] = None, local_config: Union[dict, LocalJobConfig] = None,
                 batch_config: Union[dict, BatchJobConfig] = None):
        """Creates a resource representing a job

        Args:
            name: the name of this dockerfile
            entrypoint: relative path to the dockerfile from the root of the project
            dockerfile: the name of the dockerfile to run in, required if there are multiple dockerfiles defined
            environment: a dictionary of environment variables to run the job with
            local_config: a LocalJobConfig object to use when running this job locally
            batch_config: a BatchJobConfig object to use when running this job in AWS Batch
        """
        super().__init__()
        self.name = name
        self.entrypoint = entrypoint

        if dockerfile is None:
            dockerfiles = self.get_resources(resource_type=Dockerfile)
        elif isinstance(dockerfile, str):
            dockerfiles = self.get_resources(resource_type=Dockerfile, name=dockerfile)
        else:
            dockerfiles = [dockerfile]

        if len(dockerfiles) == 0:
            raise Exception('Must specify at least one dockerfile resource in your resources')
        if len(dockerfiles) > 1:
            raise Exception('Must specify the dockerfile name if more than one dockerfile is defined')

        self.dockerfile = dockerfiles[0]

        self.environment = environment if environment is not None else dict()
        self.local_config = LocalJobConfig(**local_config) if isinstance(local_config, dict) else local_config
        self.batch_config = BatchJobConfig(**batch_config) if isinstance(batch_config, dict) else batch_config

        if self.batch_config is not None:
            if self.batch_config.jobDefinitionName is None:
                self.batch_config.jobDefinitionName = f'{self.dockerfile.name}-{self.name}'
                branch = get_git_branch()
                if branch is not None:
                    self.batch_config.jobDefinitionName += f'-{clean_string(branch)}'
            if self.dockerfile.ecr_config is None:
                self.dockerfile.ecr_config = ECRConfig(repositoryName=get_project_root_dir().name)

        if self.local_config is None:
            self.local_config = LocalJobConfig()

    def __repr__(self):
        return f'Job(name={self.name}, entrypoint={self.entrypoint}, dockerfile={self.dockerfile})'

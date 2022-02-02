
from typing import Dict, List, Union

from bisi.utils import get_project_root_dir, get_git_branch, clean_string
from bisi.resources import Resource
from bisi.resources.config import ECRConfig


class Dockerfile(Resource):

    def __init__(self, name: str = None, file: str = 'Dockerfile', build_args: Dict[str, str] = None,
                 extra_tags: List[str] = None, ssh: str = None, secret: List[str] = None,
                 ecr_config: Union[dict, ECRConfig] = None):
        """Creates a resource representing a dockerfile

        Args:
            name: the name of this dockerfile
            file: relative path to the dockerfile from the root of the project
            build_args: a dictionary of build arguments to pass to the docker build step
            extra_tags: a list of extra tags the built image should have
            ssh: the ssh agent or keys to expose to the docker build (see --ssh at https://docs.docker.com/engine/reference/commandline/build/)
            secret: a list of secrets to expose to the docker build (see --secret at https://docs.docker.com/engine/reference/commandline/build/)
        """
        super().__init__()
        if name is None:
            name = get_project_root_dir().name
        self.name = name
        self.file = file
        self.build_args = build_args
        self.tags = ['latest']
        self.ssh = ssh
        self.secret = secret

        branch = get_git_branch()
        if branch is not None:
            self.tags.append(f'{clean_string(branch)}')

        if extra_tags is not None:
            self.tags.extend(extra_tags)

        self.ecr_config = ECRConfig(**ecr_config) if isinstance(ecr_config, dict) else ecr_config

    def latest_image_tag(self):
        return f'{self.name}:{self.tags[0]}'

    def __repr__(self):
        return f'Dockerfile(name={self.name}, file={self.file})'

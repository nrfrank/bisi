
from typing import Dict, List


class LocalJobConfig:

    def __init__(self, extra_args: List[str] = None, environment: Dict[str, str] = None, remove: bool = True, **kwargs):
        """Config class for configuring local jobs
        Most arguments get passed to https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run
        image and command are set by bisi so are ignored in this class

        Args:
            extra_args: a list of extra arguments to call the entrypoint with
            environment: a dictionary of environment variables to set for local jobs
            auto_remove: whether to remove the container after it exits
            **kwargs: extra parameters to pass to docker.containers.run
        """
        self.extra_args = extra_args if extra_args else list()
        self.environment = environment if environment else dict()
        self.remove = remove
        self.kwargs = kwargs

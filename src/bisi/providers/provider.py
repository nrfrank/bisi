
from pathlib import Path
from typing import Union


class Provider:

    def __init__(self, project_root_dir: Union[str, Path]):
        """Creates the provider instance

        Args:
            project_root_dir: the root directory of the project
        """
        self.project_root_dir = Path(project_root_dir)

    def build(self, *args, **kwargs):
        raise NotImplementedError("Child classes must implement the build method.")

    def run(self, *args, **kwargs):
        raise NotImplementedError("Child classes must implement the run method.")


class CloudMixin:

    def deploy(self, *args, **kwargs):
        raise NotImplementedError("Child classes must implement the deploy method.")

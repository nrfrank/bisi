
import os
import yaml

from pathlib import Path
from typing import Union

from bisi.resources import Resource


def create_python_resources(path: Union[str, Path]) -> None:
    """Executes the python file to create the resources defined in it
    The resources will be accessible via Resource.get_resources()

    Args:
        path:
    """
    # TODO: Should we blindly exec the Python file? Is there another way to collect the resource(s)?
    path = Path(path)

    with open(path, 'r') as fp:
        exec(fp.read())


def create_resources(project_root_dir: Union[str, Path]) -> None:
    """Creates the resources defined at a root directory expecting either a yaml configuration or python definition
    The resources will be accessible via Resource.get_resources()

    Args:
        project_root_dir: The path to the root directory to get the resource definitions from
    """
    Resource.clear_resources()
    project_root_dir = Path(project_root_dir)

    python_path = os.path.join(project_root_dir, 'bisi_resources.py')
    if os.path.exists(python_path):
        create_python_resources(python_path)

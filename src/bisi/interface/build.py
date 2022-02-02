
from typing import Union
from pathlib import Path

from bisi.providers import all_providers
from bisi.resources import Resource, collect
from bisi.utils import get_project_root_dir


def build(project_root_dir: Union[str, Path] = None) -> None:
    """Builds the resources defined in the project bisi files

    Args:
        project_root_dir: the root directory to build out of
    """
    print('building...')
    project_root_dir = get_project_root_dir() if project_root_dir is None else Path(project_root_dir)

    collect.create_resources(project_root_dir)

    for provider_name, provider_class in all_providers.items():
        print(f'building resources for {provider_name}')
        provider_class(project_root_dir).build()

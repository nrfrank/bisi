
from typing import Iterable, Union
from pathlib import Path

from bisi.providers import Provider, all_providers
from bisi.resources import collect
from bisi.utils import get_project_root_dir


def run(name: str, arguments: Iterable[str], project_root_dir: Union[str, Path] = None, provider: Union[str, Provider] = 'Local') -> None:
    """Runs a resource with the given arguments and provider

    Args:
        name: the name of the resources to run
        arguments: the arguments to pass to the resource
        project_root_dir: the root directory to build out of
        provider: the provider to run the resource with
    """
    project_root_dir = get_project_root_dir() if project_root_dir is None else Path(project_root_dir)

    if isinstance(provider, str):
        provider = all_providers[provider.lower()](project_root_dir)

    collect.create_resources(project_root_dir)

    provider.run(name, arguments)

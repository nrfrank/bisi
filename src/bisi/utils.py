
import os
from pathlib import Path
from typing import Union

from git import Repo, NoSuchPathError, InvalidGitRepositoryError


def get_project_root_dir() -> Path:
    """Gets the current project root dir based on the current directory"""
    repo = get_git_repo()
    if repo is not None:
        return Path(repo.working_tree_dir).absolute()
    else:
        return Path(os.curdir).absolute()


def get_git_repo() -> Union[Repo, None]:
    """Gets the git repo based on current directory, returns none if can not get repo"""
    try:
        return Repo(path=os.curdir, search_parent_directories=True)
    except (NoSuchPathError, InvalidGitRepositoryError):
        return None


def get_git_branch() -> Union[str, None]:
    """Returns the current git branch, returns none if can not get repo"""
    repo = get_git_repo()
    if repo is not None:
        return get_git_repo().active_branch.name


def clean_string(string: str) -> str:
    return string.replace('/', '_')

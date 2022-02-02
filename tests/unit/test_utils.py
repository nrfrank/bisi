import pytest

from bisi.utils import get_project_root_dir, get_git_repo, get_git_branch


@pytest.mark.unit
class TestUtils:
    def test_git_repo(self):
        repo = get_git_repo()
        assert repo.git_dir.endswith('bisi/.git')

    def test_project_root_dir(self):
        assert get_project_root_dir().name == 'bisi'

    def test_git_branch(self):
        branch = get_git_branch()
        assert isinstance(branch, str)

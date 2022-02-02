
import os

import pytest
from bisi.resources import Resource
from bisi.interface import build


test_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))


@pytest.mark.integration
def test_build():
    Resource.clear_resources()
    build(project_root_dir=test_project_dir)


import os

import pytest

import bisi.resources.collect as collect
from bisi.resources import resource_types, Resource


@pytest.mark.unit
class TestCollect:

    def test_collect_python_resources(self):
        Resource.clear_resources()
        test_python_path = os.path.join(os.path.dirname(__file__), '../../data/bisi_resources.py')

        collect.create_python_resources(path=test_python_path)
        resources = Resource.get_resources()

        assert isinstance(resources, list)
        assert len(resources) == 4
        for r in resources:
            assert isinstance(r, resource_types)

    def test_collect_both_resources(self):
        Resource.clear_resources()
        test_project_path = os.path.join(os.path.dirname(__file__), '../../data')
        collect.create_resources(test_project_path)

        resources = Resource.get_resources()

        assert isinstance(resources, list)
        assert len(resources) == 4

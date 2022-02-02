import os
import subprocess

import pytest

from bisi import version

python_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src/bisi/cli/main.py"))


@pytest.mark.unit
def test_version():
    output = subprocess.run(['python', python_script_path, 'version'], capture_output=True)
    assert output.returncode == 0
    assert version in output.stdout.decode('utf-8')

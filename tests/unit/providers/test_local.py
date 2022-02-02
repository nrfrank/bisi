import pytest

from unittest.mock import patch, call

from bisi.providers import Local
from bisi.resources import Dockerfile, Job, Resource
from bisi.utils import get_git_branch, clean_string


@pytest.mark.unit
class TestLocalProvider:

    @pytest.mark.parametrize(
        argnames="resources, system_calls",
        argvalues=[
            ([], []),
            ([Dockerfile()], [call('docker build -f ./Dockerfile -t bisi:latest    . '),
                              call(f'docker tag bisi:latest bisi:{clean_string(get_git_branch())}')]),
            (
                    [Dockerfile(file='fake_dockerfile_one'), Dockerfile(file='fake_dockerfile_two'), Resource()],
                    [
                        call('docker build -f ./fake_dockerfile_one -t bisi:latest    . '),
                        call(f'docker tag bisi:latest bisi:{clean_string(get_git_branch())}'),
                        call('docker build -f ./fake_dockerfile_two -t bisi:latest    . '),
                        call(f'docker tag bisi:latest bisi:{clean_string(get_git_branch())}')
                    ]
            )
        ]
    )
    @patch('os.system')
    def test_build(self, os_patch, resources, system_calls):
        os_patch.return_value = 0
        local = Local('.')
        Resource.resources = resources
        local.build()
        assert os_patch.call_args_list == system_calls

    def test_run_no_exists(self):
        local = Local('.')
        with pytest.raises(Exception):
            local.run('my_job', ['my', 'args'])

    @pytest.mark.parametrize(
        argnames="resources, name, arguments, docker_call",
        argvalues=[
            ([
                Dockerfile(),
                Job(name='foo', entrypoint='my/script', dockerfile=Dockerfile())
             ],
             "foo",
             ["no args"],
             call(remove=True, image='bisi:latest', environment={}, command=['my/script', 'no args'], stream=True)
            ),
            ([
                Dockerfile(name='docker1', file='fake_dockerfile_one'),
                Dockerfile(name='docker2', file='fake_dockerfile_two'),
                Job(name='multi', entrypoint='my/script', dockerfile=Dockerfile(name='docker1', file='fake_dockerfile_one')),
                Resource()
             ],
             "multi",
             ["one", "two", "three"],
             call(remove=True, image='docker1:latest', environment={}, command=['my/script', 'one', 'two', 'three'], stream=True)
            )
        ]
    )
    @patch('bisi.providers.local.docker_client')
    def test_run(self, docker_patch, resources, name, arguments, docker_call):
        local = Local('.')
        Resource.resources = resources
        local.run(name, arguments)
        assert docker_patch.containers.run.call_args == docker_call

import pytest

from bisi.providers import Provider
from bisi.providers.provider import CloudMixin


def build(*args, **kwargs):
    pass


def deploy(*args, **kwargs):
    pass


def run(*args, **kwargs):
    pass


@pytest.mark.unit
class TestProvider:
    @pytest.fixture(scope="function")
    def foo(self):
        class Foo(Provider):
            def __init__(self):
                pass

        return Foo

    def test_nothing_implemented(self, foo):
        f = foo()
        with pytest.raises(NotImplementedError) as exec:
            f.run()

        assert "Child classes must implement the run method." in str(exec.value)

    def test_partial_implementation_build(self, foo):
        foo.build = build
        f = foo()
        f.build()
        with pytest.raises(NotImplementedError) as exec:
            f.run()

        assert "Child classes must implement the run method." in str(exec.value)

    def test_partial_implementation_run(self, foo):
        foo.run = run

        f = foo()
        with pytest.raises(NotImplementedError) as exec:
            f.build()

        assert "Child classes must implement the build method." in str(exec.value)
        f.run()

    def test_full_implementation(self, foo):
        foo.build = build
        foo.run = run


@pytest.mark.unit
class TestCloudMixin:
    @pytest.fixture(scope="function")
    def foo(self):
        class Foo(CloudMixin):
            def __init__(self):
                pass

        return Foo

    def test_nothing_implemented(self, foo):
        f = foo()
        with pytest.raises(NotImplementedError) as exec:
            f.deploy()

        assert "Child classes must implement the deploy method." in str(exec.value)

    def test_implemented(self, foo):
        foo.deploy = deploy
        f = foo()
        f.deploy()

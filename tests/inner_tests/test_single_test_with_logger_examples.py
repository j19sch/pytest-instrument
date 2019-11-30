import pytest


def test_passes(request):
    request.config.instrument["logger"].info("log record by test_passes")
    assert True


class TestClass:
    def test_in_class_passes(self, request):
        request.config.instrument["logger"].info("log record by TestClass test_passes")
        assert True


@pytest.fixture(scope="session")
def session_fixture(request):
    request.config.instrument["logger"].info("session fixture setup")
    yield
    request.config.instrument["logger"].info("session fixture teardown")


@pytest.fixture(scope="module")
def module_fixture(request):
    request.config.instrument["logger"].info("module fixture setup")
    yield
    request.config.instrument["logger"].info("module fixture teardown")


@pytest.fixture(scope="function")
def function_fixture(request):
    request.config.instrument["logger"].info("function fixture setup")
    yield
    request.config.instrument["logger"].info("function fixture teardown")


def test_with_all_fixtures_and_logger(
    request, session_fixture, module_fixture, function_fixture
):
    request.config.instrument["logger"].info("test itself")

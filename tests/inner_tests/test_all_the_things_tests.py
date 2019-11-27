import pytest


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


def test_passes(request, session_fixture, module_fixture, function_fixture):
    request.config.instrument["logger"].error("logging by the SECOND test")
    pass


def test_another_passes(request, session_fixture, module_fixture, function_fixture):
    request.config.instrument["logger"].error("logging by the FIRST test")
    pass

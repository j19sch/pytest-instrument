import pytest


@pytest.fixture(scope="function")
def setup_fixture_with_function_scope():
    pass


@pytest.fixture(scope="module")
def setup_fixture_with_module_scope():
    pass


@pytest.fixture(scope="session")
def setup_fixture_with_session_scope():
    pass


@pytest.fixture(scope="function")
def teardown_fixture_with_function_scope():
    yield
    pass


@pytest.fixture(scope="module")
def teardown_fixture_with_module_scope():
    yield
    pass


@pytest.fixture(scope="session")
def teardown_fixture_with_session_scope():
    yield
    pass


@pytest.fixture(scope="function", name="named_fixture")
def fixture_with_a_name():
    pass


@pytest.fixture(scope="function")
def parent_fixture():
    pass


@pytest.fixture(scope="function")
def child_fixture(parent_fixture):
    pass


def test_setup_fixture_function_scope(setup_fixture_with_function_scope):
    assert True


def test_setup_fixture_module_scope(setup_fixture_with_module_scope):
    assert True


def test_setup_fixture_session_scope(setup_fixture_with_session_scope):
    assert True


def test_teardown_fixture_function_scope(teardown_fixture_with_function_scope):
    assert True


def test_teardown_fixture_module_scope(teardown_fixture_with_module_scope):
    assert True


def test_teardown_fixture_session_scope(teardown_fixture_with_session_scope):
    assert True


def test_with_multiple_fixtures(
    setup_fixture_with_function_scope, teardown_fixture_with_function_scope
):
    assert True


def test_with_no_fixtures():
    assert True


def test_named_fixture(named_fixture):
    assert True


def test_with_child_fixture(child_fixture):
    assert True

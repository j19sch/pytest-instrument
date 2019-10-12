import pytest


@pytest.fixture
def setup_passes():
    pass


@pytest.fixture
def setup_fails():
    assert False


@pytest.fixture
def teardown_passes():
    yield
    pass


@pytest.fixture
def teardown_fails():
    yield
    assert False


def test_setup_passes(setup_passes):
    assert True


def test_passes():
    assert True


def test_teardown_passes(teardown_passes):
    assert True


def test_setup_fails(setup_fails):
    assert True


def test_fails():
    assert False


def test_teardown_fails(teardown_fails):
    assert True


def test_setup_and_teardown_fail(setup_fails, teardown_fails):
    assert True


@pytest.mark.skip
def test_skipped():
    assert True

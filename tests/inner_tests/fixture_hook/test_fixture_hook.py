import pytest


@pytest.fixture
def fixture_to_filter_out():
    pass


def test_using_fixture(fixture_to_filter_out):
    assert True

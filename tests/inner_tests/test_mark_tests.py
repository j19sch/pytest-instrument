import pytest


@pytest.mark.instrument("a_mark")
def test_mark():
    assert True

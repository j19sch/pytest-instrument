import pytest


@pytest.mark.instrument("a_mark")
def test_mark():
    assert True


@pytest.mark.instrument("a_mark", "another_mark")
def test_multiple_marks():
    assert True


def test_without_mark():
    assert True

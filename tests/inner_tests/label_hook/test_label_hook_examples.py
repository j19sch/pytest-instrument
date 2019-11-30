import pytest


def test_pass():
    assert True


@pytest.mark.instrument("a_mark")
def test_pass_with_label():
    assert True

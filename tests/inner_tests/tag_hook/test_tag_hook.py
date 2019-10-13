import pytest


def test_pass():
    assert True


@pytest.mark.instrument(my_mark="a_mark")
def test_pass_with_tag():
    assert True

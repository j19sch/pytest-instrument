import pytest


@pytest.mark.instrument("a_mark")
def test_single_arg_in_mark():
    assert True


@pytest.mark.instrument(my_mark="a_mark")
def test_single_kwarg_in_mark():
    assert True


@pytest.mark.instrument("a_mark", "another_mark")
def test_multiple_args_in_mark():
    assert True


@pytest.mark.instrument(my_mark="a_mark", my_other_mark="another_mark")
def test_multiple_kwargs_in_mark():
    assert True


@pytest.mark.instrument("a_mark", my_mark="a_mark")
def test_with_args_and_kwargs_in_mark():
    assert True


def test_without_mark():
    assert True

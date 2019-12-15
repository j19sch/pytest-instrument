import logging
import pytest


@pytest.fixture(scope="module")
def a_module_scoped_fixture():
    fxt_logger = logging.getLogger("instr.log").getChild("fxtlog")
    fxt_logger.info("fixture setup")

    yield fxt_logger

    fxt_logger.info("fixture teardown")


def test_first_test(a_module_scoped_fixture):
    a_module_scoped_fixture.info("first test")


def test_second_test(a_module_scoped_fixture):
    a_module_scoped_fixture.info("second test")

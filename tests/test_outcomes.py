import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_results_setup_teardown_call.py"
    testdir.copy_example(filename)
    return filename


def test_result_call_passes(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_passes")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::test_passes, call, passed, *"
    )


def test_result_call_fails(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_fails")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::test_fails, call, failed, *"
    )


def test_result_setup_passes(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_setup_passes")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::test_setup_passes, setup, passed, *"
    )


def test_result_setup_fails(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_setup_fails")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::test_setup_fails, setup, failed, *"
    )


def test_result_teardown_passes(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_teardown_passes")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::test_teardown_passes, teardown, passed, *"
    )


def test_result_teardown_fails(testdir, tests_filename):
    result = testdir.runpytest("-vs", "-k", "test_teardown_fails")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::test_teardown_fails, teardown, failed, *"
    )

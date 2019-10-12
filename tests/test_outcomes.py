import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_results_setup_teardown_call.py"
    testdir.copy_example(filename)
    return filename


def test_result_call_passes(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{test_to_run}, call, passed, *"
    )


def test_result_call_fails(testdir, tests_filename):
    test_to_run = "test_fails"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{test_to_run}, call, failed, *"
    )


def test_result_setup_passes(testdir, tests_filename):
    test_to_run = "test_setup_passes"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{test_to_run}, setup, passed, *"
    )


def test_result_setup_fails(testdir, tests_filename):
    test_to_run = "test_setup_fails"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{test_to_run}, setup, failed, *"
    )


def test_result_teardown_passes(testdir, tests_filename):
    test_to_run = "test_teardown_passes"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{test_to_run}, teardown, passed, *"
    )


def test_result_teardown_fails(testdir, tests_filename):
    test_to_run = "test_teardown_fails"
    result = testdir.runpytest("-vs", "-k", test_to_run)

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        f"---> result: {tests_filename}::{test_to_run}, teardown, failed, *"
    )

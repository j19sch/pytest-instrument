import pytest


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_metadata_tests.py"
    testdir.copy_example(filename)
    return filename


def test_record_id(testdir, tests_filename):
    test_to_run = "test_passes"
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}::{test_to_run}"
    )
    result.assert_outcomes(error=0, failed=0, passed=1)

    uuid4_regex = "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}"
    result.stdout.re_match_lines(f'.*"record_id": "{uuid4_regex}",.*')

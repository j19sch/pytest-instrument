import csv
import pytest
import re
from uuid import UUID

import tests.helpers


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

    pattern = re.compile(f'.*"record_id": "({uuid4_regex})",.*')
    record_ids = pattern.findall(result.stdout.str())

    assert len(record_ids) == len(set(record_ids))

    artifacts_dir = testdir.tmpdir.join("artifacts")
    csv_files = tests.helpers.get_files_in_testdir_by_extension(artifacts_dir, "csv")
    assert len(csv_files) == 1

    csv_data = []
    with open(artifacts_dir.join(csv_files[0])) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for record in csv_reader:
            try:
                UUID(record["record_id"], version=4)
            except (AttributeError, ValueError):
                assert False, f"Record id {record['record_id']} is not a valid v4 UUID."
            csv_data.append(dict(record))


def test_session_id(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument", f"{tests_filename}", "-k in_session"
    )
    result.assert_outcomes(error=0, failed=0, passed=2)

    uuid4_regex = "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}"
    result.stdout.re_match_lines(f'.*"session_id": "{uuid4_regex}",.*')

    pattern = re.compile(f'.*"session_id": "({uuid4_regex})",.*')
    session_id = pattern.search(result.stdout.str()).group(1)

    for line in [line for line in result.outlines if "---> record" in line]:
        assert f'"session_id": "{session_id}"' in line

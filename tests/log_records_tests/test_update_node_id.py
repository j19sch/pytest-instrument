import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_instr_logger_node_id_examples.py"
    testdir.copy_example(filename)
    return filename


def test_update_node_id(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json,log", "--log-cli-level=debug", f"{tests_filename}"
    )
    result.assert_outcomes(error=0, failed=0, passed=2)

    json_records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    json_records_instr_log = [
        record for record in json_records if record["name"].startswith("instr.log")
    ]
    assert len(json_records_instr_log) == 4
    helpers.json_validate_each_record(json_records)

    node_id_first_test = f"{tests_filename}::test_first_test"
    node_id_second_test = f"{tests_filename}::test_second_test"

    for record in json_records_instr_log:
        if record["message"] in ["fixture setup", "first test"]:
            assert record["node_id"] == node_id_first_test
        elif record["message"] in ["second test", "fixture teardown"]:
            assert record["node_id"] == node_id_second_test
        else:
            assert False, f"Unexpected message in record {record}"

    log_records = helpers.get_plain_log_file_from_artifacts_dir_and_return_records(
        testdir
    )
    assert len(log_records[1:]) == len(json_records)

    log_records_instr_log = [record for record in log_records if "instr.log" in record]
    assert len(log_records_instr_log) == len(json_records_instr_log)

    for record in log_records_instr_log:
        if "fixture setup" in record or "first test" in record:
            assert node_id_first_test in record
        elif "second test" in record or "fixture teardown" in record:
            assert node_id_second_test in record
        else:
            assert False, f"Unexpected message in record {record}"

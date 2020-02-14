import pytest

from tests import helpers


@pytest.fixture(scope="function")
def tests_filename(testdir):
    filename = "test_instr_logger_node_id_examples.py"
    testdir.copy_example(filename)
    return filename


def test_update_node_id(testdir, tests_filename):
    result = testdir.runpytest(
        "-vs", "--instrument=json", "--log-cli-level=debug", f"{tests_filename}"
    )
    result.assert_outcomes(error=0, failed=0, passed=2)

    records = helpers.get_json_log_file_from_artifacts_dir_and_return_records(testdir)
    log_records = [
        record for record in records if record["name"].startswith("instr.log")
    ]
    assert len(log_records) == 4
    helpers.json_validate_each_record(records)

    for record in log_records:
        if record["message"] in ["fixture setup", "first test"]:
            assert (
                record["node_id"]
                == "test_instr_logger_node_id_examples.py::test_first_test"
            )
        elif record["message"] in ["second test", "fixture teardown"]:
            assert (
                record["node_id"]
                == "test_instr_logger_node_id_examples.py::test_second_test"
            )
        else:
            assert False, f"Unexpected message in record {record}"

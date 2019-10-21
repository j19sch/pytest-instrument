import json
import os

ARTIFACTS_DIRNAME = "artifacts"
UUID4_REGEX = "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}"


def get_files_from_artifacts_dir_by_extension(testdir, extension):
    artifacts_dir = testdir.tmpdir.join(ARTIFACTS_DIRNAME)
    return [file for file in os.listdir(artifacts_dir) if f".{extension}" in file]


def get_records_from_json_file_in_artifacts_dir(testdir, filename):
    artifacts_dir = testdir.tmpdir.join(ARTIFACTS_DIRNAME)

    with open(artifacts_dir.join(filename)) as json_file:
        json_data = json.load(json_file)

    return json_data


def get_json_file_from_artifacts_dir_and_return_records(testdir):
    json_files = get_files_from_artifacts_dir_by_extension(testdir, "json")
    assert len(json_files) == 1

    return get_records_from_json_file_in_artifacts_dir(testdir, json_files[0])

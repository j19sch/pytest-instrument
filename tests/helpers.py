import json
import os

from jsonschema import validate

ARTIFACTS_DIRNAME = "artifacts"
UUID4_REGEX = "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$"
START_STOP_REGEX = "^[0-9]{10}\\.[0-9]{1,7}$"
DURATION_REGEX = "^[0-9]{1,}\\.[0-9]{1,12}$"

JSON_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "pattern": UUID4_REGEX},
            "record_id": {"type": "string", "pattern": UUID4_REGEX},
            "node_id": {"type": "string"},
            "when": {"type": "string", "enum": ["setup", "call", "teardown"]},
            "outcome": {"type": "string", "enum": ["passed", "failed", "skipped"]},
            "start": {"type": "string", "pattern": START_STOP_REGEX},
            "stop": {"type": "string", "pattern": START_STOP_REGEX},
            "duration": {"type": "string", "pattern": DURATION_REGEX},
            "labels": {"type": ["array", "null"]},
            "tags": {"type": ["object", "null"]},
            "fixtures": {"type": "array"},
        },
        "additionalProperties": False,
        "minProperties": 11,
        "uniqueItems": True,
    },
}


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


def validate_json(json__records):
    validate(instance=json__records, schema=JSON_SCHEMA)

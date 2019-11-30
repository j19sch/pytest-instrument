import json
import os
from datetime import datetime

from jsonschema import validate

ARTIFACTS_DIRNAME = "artifacts"
UUID4_REGEX = "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$"
START_STOP_REGEX = "^[0-9]{10}\\.[0-9]{1,7}$"
DURATION_REGEX = "^[0-9]{1,}\\.[0-9]{1,12}$"

SHARED_OBJECTS = {
    "type": "object",
    "properties": {
        "timestamp": {"type": "string"},
        "level": {"type": "string"},
        "name": {"type": "string"},
        "message": {"type": "string"},
        "filename": {"type": "string"},
        "funcName": {"type": ["string", "null"]},
        "lineno": {"type": "number"},
        "session_id": {"type": "string", "pattern": UUID4_REGEX},
        "record_id": {"type": "string", "pattern": UUID4_REGEX},
        "node_id": {"type": "string"},
    },
    "required": [
        "timestamp",
        "level",
        "name",
        "message",
        "filename",
        "funcName",
        "lineno",
        "session_id",
        "record_id",
        "node_id",
    ],
    "uniqueItems": True,
}

REPORT_SCHEMA = {
    "allOf": [
        SHARED_OBJECTS,
        {
            "type": "object",
            "properties": {
                "when": {"type": "string", "enum": ["setup", "call", "teardown"]},
                "outcome": {"type": "string", "enum": ["passed", "failed", "skipped"]},
                "start": {"type": "string", "pattern": START_STOP_REGEX},
                "stop": {"type": "string", "pattern": START_STOP_REGEX},
                "duration": {"type": "string", "pattern": DURATION_REGEX},
                "labels": {"type": ["array", "null"]},
                "tags": {"type": ["object", "null"]},
                "fixtures": {"type": ["array", "null"]},
            },
            "required": [
                "when",
                "outcome",
                "start",
                "stop",
                "duration",
                "labels",
                "tags",
                "fixtures",
            ],
            "uniqueItems": True,
        },
    ]
}

LOG_SCHEMA = {"allOf": [SHARED_OBJECTS]}


def get_files_from_artifacts_dir_by_extension(testdir, extension):
    artifacts_dir = testdir.tmpdir.join(ARTIFACTS_DIRNAME)
    try:
        files = [file for file in os.listdir(artifacts_dir) if f".{extension}" in file]
    except FileNotFoundError:
        files = []
    return files


def get_records_from_log_file_in_artifacts_dir(testdir, filename):
    artifacts_dir = testdir.tmpdir.join(ARTIFACTS_DIRNAME)

    with open(artifacts_dir.join(filename)) as log_file:
        all_records = log_file.readlines()
        parsed_records = [json.loads(record) for record in all_records]

    return parsed_records


def get_log_file_from_artifacts_dir_and_return_records(testdir):
    log_files = get_files_from_artifacts_dir_by_extension(testdir, "log")
    assert len(log_files) == 1

    return get_records_from_log_file_in_artifacts_dir(testdir, log_files[0])


def json_validate_each_record(records):
    for record in records:
        if record["name"].startswith("instr.report"):
            validate(instance=record, schema=REPORT_SCHEMA)
        elif record["name"].startswith("instr.log"):
            validate(instance=record, schema=LOG_SCHEMA)


def validate_timestamp(timestamp, format):
    try:
        if timestamp != datetime.strptime(timestamp, format).strftime(format):
            raise ValueError
        return True
    except ValueError:
        return False

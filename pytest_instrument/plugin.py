import csv
import os
import json
import uuid


def pytest_addoption(parser):
    parser.addoption(
        "--instrument",
        action="store_true",
        default=False,
        help="enable pytest-instrument",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")

    if config.getoption("--instrument") is True:
        session_id = str(uuid.uuid4())

        try:
            os.mkdir("./artifacts", mode=0o777)
        except FileExistsError:
            pass
        output_file = open(f"./artifacts/{session_id}.csv", "a")
        fieldnames = [
            "session_id",
            "record_id",
            "node_id",
            "when",
            "outcome",
            "start",
            "stop",
            "duration",
            "labels",
            "tags",
            "fixtures",
        ]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        config.instrument = {
            "session_id": session_id,
            "csv_writer": writer,
            "output_file": output_file,
        }


def pytest_unconfigure(config):
    if config.getoption("--instrument") is True:
        output_file = config.instrument["output_file"]
        output_file.close()

        session_id = config.instrument["session_id"]
        with open(f"./artifacts/{session_id}.csv", "r") as input_csv, open(
            f"./artifacts/{session_id}.json", "w"
        ) as output_json:
            reader = csv.DictReader(input_csv)
            json.dump([row for row in reader], output_json)


def pytest_addhooks(pluginmanager):
    from pytest_instrument import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_runtest_setup(item):
    if item.config.getoption("--instrument") is True:
        try:
            labels = list([_.args for _ in item.iter_markers("instrument")][0])
        except IndexError:
            labels = []

        item.config.hook.pytest_instrument_labels(config=item.config, labels=labels)

        try:
            tags = [_.kwargs for _ in item.iter_markers("instrument")][0]
        except IndexError:
            tags = {}

        item.config.hook.pytest_instrument_tags(config=item.config, tags=tags)

        labels_and_tags = {"labels": labels, "tags": tags}
        item.user_properties.append(("instrument", labels_and_tags))

        fixtures = item.fixturenames.copy()
        item.config.hook.pytest_instrument_fixtures(fixtures=fixtures)
        item.user_properties.append(("fixtures", fixtures))


def pytest_runtest_makereport(item, call):
    if item.config.getoption("--instrument") is True:
        item.user_properties.append(
            (call.when, {"start": call.start, "stop": call.stop})
        )


def pytest_report_teststatus(report, config):
    if config.getoption("--instrument") is True:
        labels_and_tags = {}
        for prop in (
            prop for prop in report.user_properties if prop[0] == "instrument"
        ):
            labels_and_tags = prop[1]

        timestamps = {}
        for prop in (prop for prop in report.user_properties if prop[0] == report.when):
            timestamps = prop[1]

        fixtures = []
        for prop in (prop for prop in report.user_properties if prop[0] == "fixtures"):
            fixtures = prop[1]

        record = {
            "session_id": config.instrument["session_id"],
            "record_id": str(uuid.uuid4()),
            "node_id": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "start": str(timestamps["start"]),
            "stop": str(timestamps["stop"]),
            "duration": str(report.duration),
            "labels": labels_and_tags.get("labels", None),
            "tags": labels_and_tags.get("tags", None),
            "fixtures": fixtures,
        }

        print(f"\n---> record: {json.dumps(record)}")
        writer = config.instrument["csv_writer"]
        writer.writerow(record)

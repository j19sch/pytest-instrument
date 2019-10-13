import json


def pytest_addoption(parser):
    parser.addoption(
        "--instrument",
        action="store_true",
        default=False,
        help="enable pytest-instrument",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_runtest_setup(item):
    if item.config.getoption("--instrument") is True:
        try:
            labels = [_.args for _ in item.iter_markers("instrument")][0]
        except IndexError:
            labels = ()

        try:
            tags = [_.kwargs for _ in item.iter_markers("instrument")][0]
        except IndexError:
            tags = {}

        labels_and_tags = {"labels": labels, "tags": tags}

        item.user_properties.append(("instrument", labels_and_tags))


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

        record = {
            "node_id": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "start": timestamps["start"],
            "stop": timestamps["stop"],
            "duration": report.duration,
            "labels": labels_and_tags.get("labels", None),
            "tags": labels_and_tags.get("tags", None),
        }

        print(f"\n---> record: {json.dumps(record)}")

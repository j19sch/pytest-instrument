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

    # ToDo: make it an attribute of session instead of config
    setattr(config, "_instrument", {})
    config.instrument = {"session_id": str(uuid.uuid4())}


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
            "start": timestamps["start"],
            "stop": timestamps["stop"],
            "duration": report.duration,
            "labels": labels_and_tags.get("labels", None),
            "tags": labels_and_tags.get("tags", None),
            "fixtures": fixtures,
        }

        print(f"\n---> record: {json.dumps(record)}")

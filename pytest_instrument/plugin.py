import json


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_runtest_setup(item):
    try:
        instrument_marks = next(_.args for _ in item.iter_markers("instrument"))
    except StopIteration:
        instrument_marks = ()

    item.user_properties.append(("instrument", instrument_marks))


def pytest_runtest_logreport(report):
    marks = ()
    for prop in (prop for prop in report.user_properties if prop[0] == "instrument"):
        marks = prop[1]

    record = {
        "node_id": report.nodeid,
        "when": report.when,
        "outcome": report.outcome,
        "duration": report.duration,
        "marks": marks,
    }

    print(f"\n---> record: {json.dumps(record)}")

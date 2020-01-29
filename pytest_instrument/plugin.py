import logging
import uuid
from datetime import datetime

import pytest

from pytest_instrument.backport_configurable_stacklevel import patch_logger
from pytest_instrument.logging_helpers import setup_log_file_handler, InstLogger


def pytest_addoption(parser):
    parser.addoption(
        "--instrument",
        action="store",
        default=None,
        type=lambda s: [item for item in s.split(",")],
        help="enable pytest-instrument output; comma-separated list; expected valued: json, log",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_sessionstart(session):
    session_id = str(uuid.uuid4())

    if session.config.getoption("instrument") is not None:
        if "json" in session.config.getoption("instrument"):
            filename = (
                f"{datetime.now().strftime('%Y%m%dT%H%M%S')}_{session_id[:8]}.log"
            )
            log_handler = setup_log_file_handler(filename, "json")
    else:
        log_handler = logging.NullHandler()

    logging.setLoggerClass(patch_logger(InstLogger))
    logger = logging.getLogger("instr.log")
    logger.setLevel("DEBUG")
    logger.addHandler(log_handler)

    logger.session_id = session_id

    session.config.instrument = {
        "session_id": session_id,
        "logger": logger,
        "logfile_handler": log_handler,
    }


def pytest_sessionfinish(session, exitstatus):
    session.config.instrument["logfile_handler"].close()
    session.config.instrument["logger"].removeHandler(
        session.config.instrument["logfile_handler"]
    )


def pytest_addhooks(pluginmanager):
    from pytest_instrument import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_runtest_setup(item):
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

    labels = None if not labels else labels
    tags = None if not tags else tags
    labels_and_tags = {"labels": labels, "tags": tags}
    item.user_properties.append(("instrument", labels_and_tags))

    fixtures = item.fixturenames.copy()
    item.config.hook.pytest_instrument_fixtures(fixtures=fixtures)
    fixtures = None if not fixtures else fixtures
    item.user_properties.append(("fixtures", fixtures))

    item.config.instrument["logger"].node_id = item._nodeid

    for logger in [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if "instr.log" in name
    ]:
        logger.node_id = item._nodeid


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    item.user_properties.append((call.when, {"start": call.start, "stop": call.stop}))

    outcome = yield

    report = outcome.get_result()
    _log_report(report, item.config)


def _log_report(report, config):
    if config.getoption("instrument") is not None:
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
            "name": "instr.report",
            # ToDo: set level based on passed, skipped, failed
            "level": "INFO",
            "msg": f"{report.nodeid} {report.when} {report.outcome}",
            "session_id": config.instrument["session_id"],
            "node_id": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "start": str(timestamps["start"]),
            "stop": str(timestamps["stop"]),
            "duration": f"{report.duration:.12f}",
            "labels": labels_and_tags.get("labels", None),
            "tags": labels_and_tags.get("tags", None),
            "fixtures": fixtures,
        }

        if "json" in config.getoption("instrument"):
            # Reason for makeLogRecord() and emit() instead of using a logger is to prevent
            # these records from being captured and thus sent to stdout by pytest.
            log_record = logging.makeLogRecord(record)
            config.instrument["logfile_handler"].emit(log_record)
    else:
        pass

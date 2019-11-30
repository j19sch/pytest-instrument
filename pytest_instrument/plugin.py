import logging
import uuid
from datetime import datetime

import pytest
import structlog

from pytest_instrument.logging_helpers import setup_log_file_handler


def pytest_addoption(parser):
    parser.addoption(
        "--instrument",
        action="store",
        default=None,
        help="enable pytest-instrument output: json",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_sessionstart(session):
    structlog.configure(
        processors=[
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    session_id = str(uuid.uuid4())

    if session.config.getoption("instrument") == "json":
        filename = f"{datetime.now().strftime('%Y%m%dT%H%M%S')}_{session_id}.log"
        log_handler = setup_log_file_handler(filename, "json")
    else:
        log_handler = logging.NullHandler()

    # logger = structlog.wrap_logger(logging.getLogger("instr.log"), processors=[
    #         structlog.stdlib.PositionalArgumentsFormatter(),
    #         structlog.processors.StackInfoRenderer(),
    #         structlog.processors.format_exc_info,
    #         structlog.processors.UnicodeDecoder(),
    #         structlog.stdlib.render_to_log_kwargs,
    #     ],
    #     wrapper_class=structlog.stdlib.BoundLogger,
    #     context_class=dict,
    #     cache_logger_on_first_use=True)

    logger = structlog.get_logger("instr.log")

    logger.setLevel("DEBUG")
    logger.addHandler(log_handler)

    session_bound_logger = logger.bind(session_id=session_id)

    session.config.instrument = {
        "session_id": session_id,
        "logger": session_bound_logger,
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

    try:
        logger = item.config.instrument["logger"].unbind("node_id")
    except KeyError:
        logger = item.config.instrument["logger"]

    item.config.instrument["logger"] = logger.bind(node_id=item._nodeid)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    item.user_properties.append((call.when, {"start": call.start, "stop": call.stop}))

    outcome = yield

    report = outcome.get_result()
    _log_report(report, item.config)


def _log_report(report, config):
    labels_and_tags = {}
    for prop in (prop for prop in report.user_properties if prop[0] == "instrument"):
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

    if config.getoption("instrument") == "json":
        # Reason for makeLogRecord() and emit() instead of using a logger is to prevent
        # these records from being captured and thus sent to stdout by pytest.
        log_record = logging.makeLogRecord(record)
        config.instrument["logfile_handler"].emit(log_record)

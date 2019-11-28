import logging
import os
import uuid

import pytest
import structlog

from pytest_instrument.logging_helpers import logfile_handler


def pytest_addoption(parser):
    parser.addoption(
        "--instrument",
        action="store_true",
        default=False,
        help="enable pytest-instrument",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_unconfigure(config):
    if config.getoption("--instrument") is True:
        config.instrument["logfile_handler"].close()
        config.instrument["logger"].removeHandler(config.instrument["logfile_handler"])


def pytest_sessionstart(session):
    if session.config.getoption("--instrument") is True:
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

        try:
            os.mkdir("./artifacts", mode=0o777)
        except FileExistsError:
            pass

        log_file = f"./artifacts/{session_id}.log"
        log_handler = logfile_handler(log_file)

        logger = structlog.get_logger("instr.log")
        logger.setLevel("DEBUG")
        logger.addHandler(log_handler)

        session_bound_logger = logger.bind(session_id=session_id)

        session.config.instrument = {
            "session_id": session_id,
            "logger": session_bound_logger,
            "logfile_handler": log_handler,
        }


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
            "name": "instr.report",
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

        # Reason for makeLogRecord() and emit() instead of using a logger is to prevent
        # these records from being captured and thus sent to stdout by pytest.
        log_record = logging.makeLogRecord(record)
        config.instrument["logfile_handler"].emit(log_record)


@pytest.fixture(scope="session")
def instr_logger(request):
    return request.config.instrument["logger"]

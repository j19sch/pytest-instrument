import logging

LOGGER = logging.getLogger("pytest-metrics")


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_runtest_setup(item):
    #     item.user_properties.append(('metrics', next(_.args for _ in item.iter_markers('metrics'))))
    try:
        instrument_mark = next(_.args for _ in item.iter_markers("instrument"))
    except StopIteration:
        instrument_mark = ()
    print(f"\n---> instrument mark: {instrument_mark}")


# def pytest_runtest_makereport(item, call):
# item.user_properties.append((call.when, "Buzz"))


def pytest_runtest_logreport(report):
    print(
        f"\n---> result: {report.nodeid}, {report.when}, {report.outcome}, {report.duration}"
    )

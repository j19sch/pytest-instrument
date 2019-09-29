import logging

LOGGER = logging.getLogger("pytest-metrics")


def pytest_configure(config):
    config.addinivalue_line("markers", "instrument: pytest-instrument mark")


def pytest_runtest_setup(item):
    try:
        instrument_mark = next(_.args for _ in item.iter_markers("instrument"))
    except StopIteration:
        instrument_mark = ()
    print(f"\n---> instrument mark: {instrument_mark}")


#
# def pytest_runtest_setup(item):
#     item.user_properties.append(('metrics', next(_.args for _ in item.iter_markers('metrics'))))
#     LOGGER.info(f"item: {item.__dict__}")
#
#
# def pytest_runtest_makereport(item, call):
#     LOGGER.info(f"item: {item.__dict__}")
# #     LOGGER.info(f"metrics: {next(_.args for _ in item.iter_markers('metrics'))}")
# #     if call.when == 'setup':
# #         item.user_properties.append(('metrics', next(_.args for _ in item.iter_markers('metrics'))))
# #
#     LOGGER.info(f"call: {call.__dict__}")
#
#
# def pytest_runtest_logreport(report):
#     LOGGER.info(f"report: {report.__dict__}")

def pytest_instrument_labels(config, labels):
    """Called in pytest_runtest_setup(item) after collecting labels from @pytest.mark.instrument"""


def pytest_instrument_tags(config, tags):
    """Called in pytest_runtest_setup(item) after collecting tags from @pytest.mark.instrument"""


def pytest_instrument_fixtures(fixtures):
    """Called in pytest_runtest_setup(item) after collecting fixturenames from item"""

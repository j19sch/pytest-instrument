def pytest_addoption(parser):
    parser.addoption("--env", action="store")


def pytest_instrument_tags(config, tags):
    tags["env"] = config.getoption("--env")

def pytest_addoption(parser):
    parser.addoption("--env", action="store")


def pytest_instrument_labels(config, labels):
    env = config.getoption("--env")
    labels.append(env)

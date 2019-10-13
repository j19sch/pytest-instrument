def pytest_instrument_fixtures(fixtures):
    fixtures.remove("fixture_to_filter_out")

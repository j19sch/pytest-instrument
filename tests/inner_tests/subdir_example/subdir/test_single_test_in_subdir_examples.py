def test_with_logger_passes_in_subdir(request):
    request.config.instrument["logger"].info("log record by test_passes in subdir")
    assert True

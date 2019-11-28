def test_passes(request):
    request.config.instrument["logger"].info("log record by test_passes")
    assert True


class TestClass:
    def test_in_class_passes(self, request):
        request.config.instrument["logger"].info("log record by TestClass test_passes")
        assert True

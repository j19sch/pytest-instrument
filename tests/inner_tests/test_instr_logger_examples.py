def test_passes(request):
    request.config.instrument["logger"].error("Oh no, there is an error!")


def test_sub_logger(request):
    sublogger = request.config.instrument["logger"].getChild("sublogger")
    sublogger.session_id = request.config.instrument["session_id"]
    sublogger.node_id = request.node.nodeid
    sublogger.info("this actually works")


def test_logger_with_extra(request):
    request.config.instrument["logger"].info(
        "This should have something extra.", extra={"a little": "a lot"}
    )

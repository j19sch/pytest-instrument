import structlog


def test_passes(request):
    request.config.instrument["logger"].error("Oh no, there is an error!")


def test_sub_logger(request):
    logger = structlog.get_logger("instr.log.sublogger").bind(
        session_id=request.config.instrument["session_id"], node_id=request.node.nodeid
    )
    logger.info("this actually works")


def test_logger_with_custom_bind(request):
    bound_logger = request.config.instrument["logger"].bind(custom="custom_bind")
    bound_logger.info("This should have a custom bind.")

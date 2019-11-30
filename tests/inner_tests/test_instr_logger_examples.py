import structlog


def test_passes(request):
    request.config.instrument["logger"].error("Oh no, there is an error!")


def test_sub_logger(request):
    logger = structlog.get_logger("instr.log.sublogger").bind(
        session_id=request.config.instrument["session_id"], node_id=request.node.nodeid
    )
    logger.info("this actually works")

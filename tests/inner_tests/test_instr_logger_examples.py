import logging


def test_passes(request):
    request.config.instrument["logger"].error("Oh no, there is an error!")


def test_sub_logger_from_request(request):
    sublogger = request.config.instrument["logger"].getChild("sublogger")
    sublogger.info("this actually works")


def test_sub_logger_from_getLogger():
    sublogger = logging.getLogger("instr.log").getChild("sublogger")
    sublogger.info("this actually works")


def test_logger_with_extra(request):
    logger = request.config.instrument["logger"]
    logger.info("This should have something extra.", extra={"a little": "a lot"})

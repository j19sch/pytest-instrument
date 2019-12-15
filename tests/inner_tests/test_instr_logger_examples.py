import logging


def test_logger_from_request(request):
    request.config.instrument["logger"].error("Oh no, there is an error!")


def test_logger_from_getLogger():
    logging.getLogger("instr.log").error("Oh no, there is an error!")


def test_sub_logger_from_request(request):
    sublogger = request.config.instrument["logger"].getChild("sublogger")
    sublogger.info("this actually works")


def test_sub_logger_from_getLogger():
    sublogger = logging.getLogger("instr.log").getChild("sublogger")
    sublogger.info("this actually works")


def test_logger_with_extra():
    logger = logging.getLogger("instr.log")
    logger.info("This should have something extra.", extra={"a little": "a lot"})

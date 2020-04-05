import logging


def log_warning_from_child():
    logging.getLogger("instr.log").getChild(__name__).warning("different module")

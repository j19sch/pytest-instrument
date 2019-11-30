def test_passes(instr_logger):
    instr_logger.info("log record for a test")


def test_first_test_in_session(instr_logger):
    instr_logger.info("log record for test one")


def test_second_test_in_session(instr_logger):
    instr_logger.info("log record for test two")

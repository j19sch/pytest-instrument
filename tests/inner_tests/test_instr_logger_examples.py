import logging

import structlog


def test_passes(request):
    request.config.instrument["logger"].error("Oh no, there is an error!")


def test_sub_logger(request):
    logger = logging.getLogger("instr.log.sublogger")

    struct_logger = structlog.wrap_logger(
        logger,
        processors=[
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        context_class=dict,
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    my_struct_logger = struct_logger.bind(
        session_id=request.config.instrument["session_id"], node_id=request.node.nodeid
    )
    my_struct_logger.info("this actually works")


def test_logger_with_custom_bind(request):
    bound_logger = request.config.instrument["logger"].bind(custom="custom_bind")
    bound_logger.info("This should have a custom bind.")

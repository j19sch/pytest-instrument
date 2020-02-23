import logging
import os
import uuid
from datetime import datetime

from pythonjsonlogger import jsonlogger


class InstLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.session_id = None
        self.node_id = None

    def getChild(self, suffix):
        child_logger = super().getChild(suffix)
        child_logger.session_id = self.session_id
        child_logger.node_id = self.node_id
        return child_logger

    def debug(self, msg, extra=None, *args, **kwargs):
        extra = {} if extra is None else extra
        y = {"session_id": self.session_id, "node_id": self.node_id}
        super().debug(msg, extra={**extra, **y}, stacklevel=2, *args, **kwargs)

    def info(self, msg, extra=None, *args, **kwargs):
        extra = {} if extra is None else extra
        y = {"session_id": self.session_id, "node_id": self.node_id}
        super().info(msg, extra={**extra, **y}, stacklevel=2, *args, **kwargs)

    def warning(self, msg, extra=None, *args, **kwargs):
        extra = {} if extra is None else extra
        y = {"session_id": self.session_id, "node_id": self.node_id}
        super().warning(msg, extra={**extra, **y}, stacklevel=2, *args, **kwargs)

    def critical(self, msg, extra=None, *args, **kwargs):
        extra = {} if extra is None else extra
        y = {"session_id": self.session_id, "node_id": self.node_id}
        super().critical(msg, extra={**extra, **y}, stacklevel=2, *args, **kwargs)

    def error(self, msg, extra=None, *args, **kwargs):
        extra = {} if extra is None else extra
        y = {"session_id": self.session_id, "node_id": self.node_id}
        super().error(msg, extra={**extra, **y}, stacklevel=2, *args, **kwargs)


def setup_log_file_handler(filename, output_format):
    try:
        os.mkdir("./artifacts", mode=0o777)
    except FileExistsError:
        pass
    log_file = f"./artifacts/{filename}.{output_format}"

    if output_format == "json":
        return json_logfile_handler(log_file)
    elif output_format == "log":
        return log_logfile_handler(log_file)


def json_logfile_handler(logfile):
    formatter = CustomJsonFormatter(
        "%(timestamp) %(level) %(name) %(message) %(filename)s %(funcName)s %(lineno)d"
    )
    log_handler = logging.FileHandler(logfile)
    log_handler.setFormatter(formatter)
    return log_handler


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
        if log_record.get("level"):
            log_record["level"] = log_record["level"].lower()
        else:
            log_record["level"] = record.levelname.lower()
        if not log_record.get("record_id"):
            log_record["record_id"] = str(uuid.uuid4())


def log_logfile_handler(logfile):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(node_id)s - %(message)s"
    )
    log_handler = logging.FileHandler(logfile)
    log_handler.setFormatter(formatter)
    return log_handler

import logging
import os
import uuid
from datetime import datetime

from pythonjsonlogger import jsonlogger


def setup_log_file_handler(filename, type):
    try:
        os.mkdir("./artifacts", mode=0o777)
    except FileExistsError:
        pass
    log_file = f"./artifacts/{filename}"

    if type == "json":
        return json_logfile_handler(log_file)
    # ToDo: add tests for log_logfile_handler and enable


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
    # ToDo: decide default format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_handler = logging.FileHandler(logfile)
    log_handler.setFormatter(formatter)
    return log_handler

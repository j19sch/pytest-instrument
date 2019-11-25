import logging
import uuid
from datetime import datetime

from pythonjsonlogger import jsonlogger


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


def logfile_handler(logfile):
    formatter = CustomJsonFormatter(
        "%(timestamp) %(level) %(name) %(message) %(filename)s %(funcName)s %(lineno)d"
    )
    # alt formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler = logging.FileHandler(logfile)
    log_handler.setFormatter(formatter)
    return log_handler

import datetime
import logging

from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()

logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.logger.level)

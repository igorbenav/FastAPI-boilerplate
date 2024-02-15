import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")


class SafeOtelFormatter(logging.Formatter):
    def format(self, record):
        # Default values if OpenTelemetry fields are not present
        record.otelTraceID = getattr(record, "otelTraceID", "none")
        record.otelSpanID = getattr(record, "otelSpanID", "none")
        record.otelServiceName = getattr(record, "otelServiceName", "none")
        return super().format(record)


LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s \
                span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"


logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)

# Create the formatter
formatter = SafeOtelFormatter(LOGGING_FORMAT)

# Apply the formatter to all handlers
for handler in logging.getLogger().handlers:
    handler.setFormatter(formatter)

file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
file_handler.setLevel(LOGGING_LEVEL)
file_handler.setFormatter(SafeOtelFormatter(LOGGING_FORMAT))

logging.getLogger("").addHandler(file_handler)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

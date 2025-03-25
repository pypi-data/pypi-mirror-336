import logging 
from datetime import datetime
import json 

class LogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'function': record.funcName,
            'arguments': getattr(record, 'arguments', None),
        }
        return json.dumps(log_record)
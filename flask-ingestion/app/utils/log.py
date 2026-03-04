from loguru import logger as loguru_logger 
import json
import uuid

class Logger:
    def __init__(self):
        self.logger = loguru_logger.patch(self.patching)
        self.logger.add(
            "logs/log-{time:YYYY-MM-DD}.log", 
            format="{output}", 
            retention="10 days",
            rotation="00:00"
        )
        
    def serialize(self, record):
        subset = {
            "timestamp": record["time"].strftime("%d/%m/%Y %H.%M.%S.%f WIB"),
            "id": str(uuid.uuid4()),
            "level": record["level"].name,
            "message": record["message"],
            "error": record["extra"].get("error",None),
            "request": {
                "method": record["extra"].get("method"),
                "url": str(record["extra"].get("url")) if record["extra"].get("url") else None
            },
            "response": {
                "status": record["extra"].get("status_code"),
                "body": record["extra"].get("response_body", None)
            },
            "user": {
                "id": record["extra"].get("user_id",None)
            }
        }
        return json.dumps(subset)
    
    def patching(self, record):
        record["output"] = self.serialize(record)
        
    def get_logger(self):
        return self.logger
    
    
logger = Logger().get_logger()
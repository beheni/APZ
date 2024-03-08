from fastapi import FastAPI
from pydantic import BaseModel
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOGGED_MESSAGES_MAP = dict() #{UUID: "msg"}

class LogEntity(BaseModel):
    UUID: str 
    message: str

@app.get("/log")
async def list_log():
    return {"messages": ", ".join(list(LOGGED_MESSAGES_MAP.values()))}

@app.post("/log")
async def log(log_entity: LogEntity):
    if log_entity.UUID in LOGGED_MESSAGES_MAP.keys():
        logger.warning(f"UUID {log_entity.UUID} already exists in the log map.")
    LOGGED_MESSAGES_MAP[log_entity.UUID] = log_entity.message
    logger.info("Message logged correctly")
    
    return {"status": "success"}
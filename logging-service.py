import logging
import hazelcast
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOGGED_MESSAGES_MAP = None #{UUID: "msg"}

async def lifespan(app: FastAPI):
    logger.log(logging.INFO, "Starting Hazelcast CLient")
    client = hazelcast.HazelcastClient()
    global LOGGED_MESSAGES_MAP
    LOGGED_MESSAGES_MAP = client.get_map("logged_messages").blocking()
    yield
    client.shutdown()

app = FastAPI(lifespan=lifespan)

class LogEntity(BaseModel):
    UUID: str 
    message: str

@app.get("/log")
async def list_log():
    return {"messages": ", ".join(list(LOGGED_MESSAGES_MAP.values()))}

@app.post("/log")
async def log(log_entity: LogEntity):
    if LOGGED_MESSAGES_MAP.contains_key(log_entity.UUID):
        logger.warning(f"UUID {log_entity.UUID} already exists in the log map.")
    LOGGED_MESSAGES_MAP.put(log_entity.UUID, log_entity.message)
    logger.info(f"Message with text {log_entity.message} logged correctly")
    return {"status": "success"}
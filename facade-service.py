from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import requests
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOGGING_SERVICE_URLS = ["http://localhost:8001", "http://localhost:8002", "http://localhost:8003"]
MESSAGES_SERVICE_URL = "http://localhost:8002"

def get_random_logging_client():
    return LOGGING_SERVICE_URLS[random.randint(0, 2)]

class Message(BaseModel):
    text: str

@app.get("/facade_service")
async def get_messages():
    logging_response = requests.get(f"{get_random_logging_client()}/log")
    if logging_response.status_code == 200:
        logger.info("Logging service responded correctly")
    else:
        logger.critical("Error in GET request the logging service")
    
    messages_response = requests.get(f"{MESSAGES_SERVICE_URL}/message")
    if messages_response.status_code == 200:
        logger.info("Message servise responded correctly")
    else:
        logger.critical("Error in GET request the message service")
    logging_response = logging_response.json()["messages"]
    messages_response = messages_response.json()["message"]
    return f"[{logging_response}]" + " " + messages_response

@app.post("/facade_service")
async def post_messages(msg: Message):
    UUID = str(uuid4())
    payload = {"UUID": UUID, "message": msg.text}
    response = requests.post(f"{get_random_logging_client()}/log", json=payload)
    
    if response.status_code == 200:
        logger.info(f"Message \"{msg.text}\" logged correctly with UUID {UUID}")
    else:
        logger.critical("Error in POST request the logging service")
    return {"status": "success"}


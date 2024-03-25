from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
import logging
import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MESSAGES_QUEUE = None
MESSAGES = []

def setup_client():
    logger.info("Setting up Hazelcast Client")
    client = hazelcast.HazelcastClient(cluster_members=["localhost:5701"])
    global MESSAGES_QUEUE
    MESSAGES_QUEUE = client.get_queue("messages_queue").blocking()
    logger.info("Connected to Hazelcast and initialized Message Queue")


async def check_map():
    global MESSAGES
    while True:
        message = MESSAGES_QUEUE.take() 
        logger.info("Processing message: %s", message)
        MESSAGES.append(message)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_client()
    await check_map()
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/message")
async def get_message():
    logger.info("Returning message list")
    return {"message": ", ".join(MESSAGES)}
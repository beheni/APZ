from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MESSAGES_QUEUE = None

def setup_client():
    logger.info("Setting up Hazelcast Client")
    client = hazelcast.HazelcastClient(cluster_members=["localhost:5701"])
    global MESSAGES_QUEUE
    MESSAGES_QUEUE = client.get_queue("messages_queue").blocking()
    logger.info("Connected to Hazelcast and initialized Message Queue")

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_client();    
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/message")
async def get_message():
    logger.info("Returning message queue")
    return {"message": MESSAGES_QUEUE.poll()}
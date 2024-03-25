from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
import logging
import hazelcast
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MESSAGES_QUEUE = None
MESSAGES = []

async def check_queue():
    global MESSAGES
    logger.info("Checking for messages in queue")
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, MESSAGES_QUEUE.take)
        logger.info(f"Processing message: {message}")
        MESSAGES.append(message)
        logger.info("Message added to the list")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Setting up Hazelcast Client")
    client = hazelcast.HazelcastClient(cluster_members=["localhost:5701"])

    global MESSAGES_QUEUE
    MESSAGES_QUEUE = client.get_queue("messages_queue").blocking()
    
    logger.info("Connected to Hazelcast and initialized Message Queue")
    asyncio.create_task(check_queue())
    yield
    client.shutdown()

    
app = FastAPI(lifespan=lifespan)

@app.get("/message")
async def get_message():
    logger.info("Returning message list")
    return {"message": ", ".join(MESSAGES)}
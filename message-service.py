from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_client():
    logger.info("Setting up Hazelcast Client")
    client = hazelcast.HazelcastClient(cluster_members=["localhost:5701"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_client();    
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/message")
async def get_message():
    return {"message": "not implemented yet"}
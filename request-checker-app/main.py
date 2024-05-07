from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from .crawler_utils.CrawlerCreator import populate_payloads
from .utils.RedisConnection import RedisConnection
from .crawler_utils.CrawlerService import CrawlerService
from fastapi_utilities import repeat_every


redis_client = RedisConnection.get_connection()

if(redis_client == None):
    redis_client = RedisConnection.set_connection()


@repeat_every(seconds=7*60*24)
async def cron_payloads() -> None:
    await populate_payloads(is_on_startup=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await populate_payloads(is_on_startup=True)
    yield
    await populate_payloads(is_on_startup=False)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    CrawlerService.count_payload_sizes()
    return {"message": 'Hello'}

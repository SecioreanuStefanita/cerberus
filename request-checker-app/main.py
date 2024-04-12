from fastapi import FastAPI
from .crawler_utils.CrawlerCreator import PoatfCrawlerFactory
import redis
from .utils.RedisConnection import RedisConnection

app = FastAPI()
redis_client = RedisConnection.get_connection()

if(redis_client == None):
    redis_client = RedisConnection.set_connection()


@app.get("/")
def root():
    f = PoatfCrawlerFactory()
    response = f.create_crawler().cron()
    return {"message": response}

from .crawlers.PoafCrawler import PoafCrawler
from .CrawlerFactory import CrawlerFactory
from .crawlers.FuzzdbCrawler import FuzzdbCrawler
from .crawlers.PayloadboxCrawler import PayloadboxCrawler
from .crawlers.BurpCrawler import BurpCrawler
from .crawlers.FoospidyCrawler import FoospidyCrawler
import msgpack
from ..utils.RedisConnection import RedisConnection


class PoatfCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return PoafCrawler()

class FuzzdbCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return FuzzdbCrawler()

class PayloadboxCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return PayloadboxCrawler()

class BurpCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return BurpCrawler()

class FoospidyCrawlerFactory(CrawlerFactory):
    def create_crawler(self):
        return FoospidyCrawler()

async def create_all_crawlers():
    return [FoospidyCrawlerFactory().create_crawler(), BurpCrawlerFactory().create_crawler(), PayloadboxCrawlerFactory().create_crawler(), FuzzdbCrawlerFactory().create_crawler(), PoatfCrawlerFactory().create_crawler()]

async def populate_payloads(is_on_startup):
    if is_on_startup:
        redis_client = RedisConnection.get_connection()
        existing_data = msgpack.unpackb(redis_client.get(f'payloads'))
        for data in existing_data:
            if len(existing_data[data]) == 0:
                crawlers = await create_all_crawlers()
                for crawler in crawlers:
                    crawler.cron()
                break
    else:
        crawlers = await create_all_crawlers()
        for crawler in crawlers:
            crawler.cron()
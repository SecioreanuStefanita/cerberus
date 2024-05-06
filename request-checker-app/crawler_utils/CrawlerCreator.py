from .crawlers.PoafCrawler import PoafCrawler
from .CrawlerFactory import CrawlerFactory
from .crawlers.FuzzdbCrawler import FuzzdbCrawler
from .crawlers.PayloadboxCrawler import PayloadboxCrawler
from .crawlers.BurpCrawler import BurpCrawler
from .crawlers.FoospidyCrawler import FoospidyCrawler



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

def create_all_crawlers():
    return [FoospidyCrawlerFactory().create_crawler(), BurpCrawlerFactory().create_crawler(), PayloadboxCrawlerFactory().create_crawler(), FuzzdbCrawlerFactory().create_crawler(), PoatfCrawlerFactory().create_crawler()]

def populate_payloads():
    crawlers = create_all_crawlers()
    for crawler in crawlers:
        crawler.cron()
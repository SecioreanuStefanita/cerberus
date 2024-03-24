from abc import ABC, abstractmethod


class CrawlerFactory(ABC):
    @abstractmethod
    def create_crawler(self):
        pass
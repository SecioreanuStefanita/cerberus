from abc import abstractmethod, ABC


class Crawler(ABC):
    @abstractmethod
    def crawl(self):
        pass
    @abstractmethod
    def map(self):
        pass
    @abstractmethod
    def cron(self):
        pass
    @abstractmethod
    def update(self):
        pass
from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
from ..CrawlerService import CrawlerService


class PoafCrawler(Crawler):
    crawlOptions = [CrawlerOptions.XSS, CrawlerOptions.SSTI, CrawlerOptions.SQLI, CrawlerOptions.XEE, CrawlerOptions.NOSQLI, CrawlerOptions.LFI, CrawlerOptions.CMDI]
   
    
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/XSS%20Injection/Intruders", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/Intruders", CrawlerOptions.XSS)
            case CrawlerOptions.SSTI:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/Server%20Side%20Template%20Injection/Intruder", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Server%20Side%20Template%20Injection/Intruder", CrawlerOptions.SSTI)
            case CrawlerOptions.SQLI:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/SQL%20Injection/Intruder", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/Intruder", CrawlerOptions.SQLI)
            case CrawlerOptions.XEE:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/XXE%20Injection/Intruders", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XXE%20Injection/Intruders", CrawlerOptions.XEE)
            case CrawlerOptions.NOSQLI:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/NoSQL%20Injection/Intruder", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/NoSQL%20Injection/Intruder", CrawlerOptions.NOSQLI)
            case CrawlerOptions.LFI:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/File%20Inclusion/Intruders", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/File%20Inclusion/Intruders", CrawlerOptions.LFI)
            case CrawlerOptions.CMDI:
                self.crawl_helper("https://github.com/swisskyrepo/PayloadsAllTheThings/tree-commit-info/master/Command%20Injection/Intruder", "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Command%20Injection/Intruder", CrawlerOptions.CMDI)



    def map(self):
        pass
    
    def cron(self):
        for option in self.crawlOptions:
            self.crawl(option)
        
    def update(self, option, values_list):
        CrawlerService.update_crawler_data(option, values_list)
        
    def crawl_helper(self, initial_route, content_route, option):
        data = []
        file_names = [ name for name in CrawlerService.get_page_content(initial_route, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'If-None-Match': '*', 'Accept': 'application/json'}, method='GET').json()]
        for file_name in file_names:
            response = CrawlerService.get_page_content(f"{content_route}/{file_name}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
            data.extend(response.text.split("\n"))
        self.update(option, data)
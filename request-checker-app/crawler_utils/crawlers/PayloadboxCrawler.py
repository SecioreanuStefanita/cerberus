from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
from ..CrawlerService import CrawlerService


class PayloadboxCrawler(Crawler):
    crawlOptions = [CrawlerOptions.XSS, CrawlerOptions.SSTI, CrawlerOptions.SQLI, CrawlerOptions.XEE, CrawlerOptions.CMDI]
   
    
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS:
                self.crawl_helper("https://github.com/payloadbox/xss-payload-list/tree-commit-info/master/Intruder", CrawlerOptions.XSS)
            case CrawlerOptions.SSTI:
                self.crawl_helper("https://github.com/payloadbox/ssti-payloads/tree-commit-info/master/Intruder", CrawlerOptions.SSTI)
            case CrawlerOptions.SQLI:
                self.crawl_helper("https://github.com/payloadbox/sql-injection-payload-list/tree-commit-info/master/Intruder", CrawlerOptions.SQLI)
            case CrawlerOptions.XEE:
                self.crawl_helper("https://github.com/payloadbox/xxe-injection-payload-list/tree-commit-info/master/Intruder", CrawlerOptions.XEE)
            case CrawlerOptions.CMDI:
                self.crawl_helper("https://raw.githubusercontent.com/payloadbox/command-injection-payload-list/master/README.md", CrawlerOptions.CMDI)



    def map(self):
        pass
    
    def cron(self):
        for option in self.crawlOptions:
            self.crawl(option)
        
    def update(self, option, values_list):
        CrawlerService.update_crawler_data(option, values_list)
        
    def crawl_helper(self, initial_route, option):
        data = []
        if '.md' in initial_route:
            response = CrawlerService.get_page_content(f"{initial_route}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
            data.extend(self.parse_page(response.text, option))
        else: 
            file_names = [ name for name in CrawlerService.get_page_content(initial_route, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'If-None-Match': '*', 'Accept': 'application/json'}, method='GET').json()]
            for file_name in file_names:
                if '.txt' not in file_name:
                    self.crawl_helper(initial_route+'/'+file_name, option);
                else:
                    content_url = initial_route.replace('https://github.com', 'https://raw.githubusercontent.com').replace('/tree-commit-info/','/')+'/'+file_name
                    response = CrawlerService.get_page_content(f"{content_url}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
                    if 'xxe' in initial_route:
                        data.extend(self.parse_page(response.text, option))
                    else:
                        data.extend(response.text.split("\n"))
        self.update(option, data)
    
    def parse_page(self, response, crawler_option):
        data = []
        match crawler_option:
            case CrawlerOptions.CMDI:
                data.extend(response.split("### Unix")[1].split('```')[1].strip().split('\n'))
                data.extend(response.split("### Windows")[1].split('```')[1].strip().split('\n'))
            case CrawlerOptions.XEE:
                content = response.split("* ")
                for entities in content:
                    keywords = ['<!DOCTYPE', '<soap:Body>' ,'<svg', '<?xml' , '<!--?xml']
                    entity = entities.split('\n\n')
                    data.extend([obj.replace('\n','') for obj in entity if any(map(obj.__contains__, keywords))])
        return data
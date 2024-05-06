from ..Crawler import Crawler
from ..CrawlerOptions import CrawlerOptions
from ..CrawlerService import CrawlerService

class FuzzdbCrawler(Crawler):
    
    crawlOptions = [CrawlerOptions.XSS, CrawlerOptions.SQLI, CrawlerOptions.XEE, CrawlerOptions.NOSQLI, CrawlerOptions.LFI, CrawlerOptions.CMDI]
   
    
    def crawl(self, option):
        match option:
            case CrawlerOptions.XSS:
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/xss", CrawlerOptions.XSS)
            case CrawlerOptions.LFI:
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/lfi", CrawlerOptions.LFI)
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/rfi", CrawlerOptions.LFI)
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/path-traversal", CrawlerOptions.LFI)
            case CrawlerOptions.XEE:
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/xml", CrawlerOptions.XEE)
            case CrawlerOptions.SQLI:
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/sql-injection", CrawlerOptions.SQLI)
            case CrawlerOptions.NOSQLI:
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/no-sql-injection", CrawlerOptions.NOSQLI)
            case CrawlerOptions.CMDI:
                self.crawl_helper("https://github.com/fuzzdb-project/fuzzdb/tree-commit-info/master/attack/os-cmd-execution", CrawlerOptions.CMDI)


          

    def map(self):
        pass
    
    def cron(self):
        for option in self.crawlOptions:
            self.crawl(option)
        
    def update(self, option, values_list):
        CrawlerService.update_crawler_data(option, values_list)
        
    def crawl_helper(self, initial_route, option):
        data = []
        file_names = [ name for name in CrawlerService.get_page_content(initial_route, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'If-None-Match': '*', 'Accept': 'application/json'}, method='GET').json()]
        for file_name in file_names:
            if '.md' in file_name:
                continue
            if '.txt' not in file_name and '.xxe' not in file_name :
                self.crawl_helper(initial_route+'/'+file_name, option)
            else:
                content_url = initial_route.replace('https://github.com', 'https://raw.githubusercontent.com').replace('/tree-commit-info/','/')+'/'+file_name
                response = CrawlerService.get_page_content(f"{content_url}", headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html', 'If-None-Match': '', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}, method='GET')
                data.extend(self.parse_page(response.text, content_url,  option))
          
        self.update(option, data)
        
    def parse_page(self, response, url,  crawler_option):
        data = []
        match crawler_option:
            case CrawlerOptions.XSS:
                banned_files = ['all-encodings-of-lt.txt', 'default-javascript-event-attributes.txt', 'html-event-attributes.txt']
                if any(sub in url for sub in banned_files) == True:
                    return []
                if 'JHADDIX' in url:
                    data.extend([payload.split('\n')[0] for payload in response.strip().split("Exploit String: ")[1:len(response.split("Exploit String: "))]])
                else:
                    data.extend(response.strip().split('\n'))
            case CrawlerOptions.LFI:
                data.extend(response.strip().split('\n'))
            case CrawlerOptions.XEE:
                data.extend([payload for payload in response.strip().split('\n') if 'xml' in payload or 'CDATA' in payload or 'DOCTYPE' in payload])
            case CrawlerOptions.SQLI:
                data.extend(response.strip().split('\n'))
            case CrawlerOptions.NOSQLI:
                data.extend(response.strip().split('\n'))
            case CrawlerOptions.CMDI:
                if 'command-execution-unix.txt' in url:
                    data.extend(response.strip().split('\n'))
        return data
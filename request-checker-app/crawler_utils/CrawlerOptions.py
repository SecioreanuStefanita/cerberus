from enum import Enum
class CrawlerOptions(Enum):
    XSS = 1
    SSTI = 2
    SQLI = 3
    XEE = 4
    NOSQLI = 7
    LFI = 8
    CMDI = 10
    
from enum import Enum
class RequestComponent(Enum):
    PATH = 'PATH'
    HEADERS = 'HEADERS'
    BODY = 'BODY'
import requests
import msgpack
from ..utils.RedisConnection import RedisConnection
import re
class CrawlerService:
    @staticmethod
    def get_page_content(url, headers, method, params=None, data=None):
        response = requests.request(method, url, headers=headers, params=params, data=data)
        return response;
    
    @staticmethod
    def update_crawler_data(option, values_list):
        redis_client = RedisConnection.get_connection()
        existing_data = msgpack.unpackb(redis_client.get(f'payloads'))[option.name]
        update_needed = False
        for value in values_list:
            if value not in existing_data:
                if CrawlerService.permitted_value(value):
                    existing_data.append(CrawlerService.transform_value(value))
                    update_needed = True
        if update_needed:
            redis_data = msgpack.unpackb(redis_client.get(f'payloads'))
            redis_data[option.name] = existing_data
            redis_client.set(f'payloads', msgpack.packb(redis_data)) # type: ignore
    
    @staticmethod
    def count_payload_sizes():
        redis_client = RedisConnection.get_connection()
        existing_data = msgpack.unpackb(redis_client.get(f'payloads'))
        for data in existing_data:
            print(f'got for {data} -> {len(existing_data[data])} payloads\n')
    
    @staticmethod
    def permitted_value(value):
        single_word_pattern = re.compile(r'^[a-zA-Z0-9]+$')
        word_dot_word_pattern = re.compile(r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')
        
        # Check if the string matches either of the patterns
        if single_word_pattern.match(value) or len(value) < 4 or word_dot_word_pattern.match(value):
            return False
        return True
    
    @staticmethod
    def transform_value(value):
        return value
        value = re.escape(value)
        # Define refined regex patterns
        ipv4_pattern = re.compile(r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
        ipv6_pattern = re.compile(r'\b([a-fA-F0-9:]+:+)+[a-fA-F0-9]+\b')
        operation_pattern = re.compile(r'\b(\d+)\s*([\+\-\*\/\%\&\|\^<>]+)\s*(\d+)\b')
        parenthesis_pattern = re.compile(r'\((0[xX][0-9a-fA-F]+|\d+)\)')
        file_pattern = re.compile(r'\{FILE\}')
        quoted_string_pattern = re.compile(r'"[^"\s]+"')
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        url_pattern = re.compile(r'\b(https?://\S+|www\.\S+)\b')
        number_pattern = re.compile(r'\b\d+\b')
        number_equals_pattern = re.compile(r'\b(\d+)\s*=\s*(\d+)\b')

        # Replace IPv4 addresses
        value = ipv4_pattern.sub(r'(\\d{1,3}\\.){3}\\d{1,3}', value)
        # Replace IPv6 addresses
        value = ipv6_pattern.sub(r'([a-fA-F0-9:]+:+)+[a-fA-F0-9]+', value)
        # Replace operations between numbers including bitwise and exponentiation
        value = operation_pattern.sub(r'\\d+\\s*[\\+\\-\\*\\/\\%\\&\\|\\^<>]+\\s*\\d+', value)
        # Replace numbers encased in parentheses
        value = parenthesis_pattern.sub(r'\\(\\d+\\)', value)
        # Replace {FILE} with any string
        value = file_pattern.sub(r'.+', value)
        # Replace strings encased in double quotes without spaces
        value = quoted_string_pattern.sub(r'"[^"\\s]+"', value)
        # Replace email addresses
        value = email_pattern.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}', value)
        # Replace URLs with a permissive regex
        value = url_pattern.sub(r'(https?://\\S+|www\\.\\S+)', value)
        # Replace any number separated by spaces
        value = number_pattern.sub(r'\\d+', value)
        # Replace number=number with optional spaces
        value = number_equals_pattern.sub(r'\\d+\\s*=\\s*\\d+', value)
        return value
        
   
    
    @staticmethod
    async def  check_payload(payload, input):
        
        if payload in input:
            return True
        return False
        
        compiled_value =  re.compile(payload)
        match = re.search(compiled_value ,input)
        answer = match is not None
        return answer
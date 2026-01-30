import json
import requests
from retry import retry
from loguru import logger


class HTTPClient:

    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}

    @retry(tries=3, delay=1)
    def request(self, request_json):
        """发起HTTP请求"""
        try:
            response = requests.post(self.url, headers=self.headers, json=request_json, timeout=self.timeout)
            if response.status_code != 200:
                logger.error(
                    f"[HTTPClient] code:{response.status_code}, reason:{response.reason}, url:{self.url}, request:{json.dumps(request_json, ensure_ascii=False)}")
                return None
            response_json = json.loads(response.text)
            return response_json
        except Exception as e:
            logger.error(f"[HTTPClient] request failed: {e}")
        return None

import requests
from requests import Response, exceptions

from webdriver_manager.core.config import ssl_verify
from webdriver_manager.core import logger

class HttpClient:
    def get(self, url, params=None, **kwargs) -> Response:
        raise NotImplementedError

    @staticmethod
    def validate_response(resp: requests.Response):
        status_code = resp.status_code
        if status_code == 404:
            raise ValueError(f"There is no such driver by url {resp.url}")
        elif status_code == 401:
            raise ValueError(f"API Rate limit exceeded. You have to add GH_TOKEN!!!")
        elif resp.status_code != 200:
            raise ValueError(
                f"response body:\n{resp.text}\n"
                f"request url:\n{resp.request.url}\n"
                f"response headers:\n{dict(resp.headers)}\n"
            )


class WDMHttpClient(HttpClient):
    def __init__(self):
        self._ssl_verify = ssl_verify()

    def get(self, url, **kwargs) -> Response:
        try:
            logger.log(f"Raw URL: {url}")
            if 'github' in url:
                # Convert URL to base64 for proxy
                import base64
                encoded_url = base64.b64encode(url.split('://')[-1].encode()).decode()
                url = f"https://reverse.sakurapuare.com/proxy/{encoded_url}"
                logger.log(f"Proxy URL: {url}")
            resp = requests.get(
                url=url, verify=self._ssl_verify, stream=True, **kwargs)
        except exceptions.ConnectionError:
            raise exceptions.ConnectionError(f"Could not reach host. Are you offline? {url}")
        self.validate_response(resp)
        return resp


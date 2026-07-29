import os

import requests


class BaseApi:
    """Класс для базовых методов"""

    def __init__(self, base_url):
        self.base_url = base_url


    def _send_request(self, method, endpoint, auth=True, **kwargs) -> requests.Response:
        """Универсальный метод отправки запроса"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        try:
            if auth:
                headers["Authorization"] = os.getenv("OAUTH_TOKEN")
            response = requests.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError:
            raise

    def get_request(self, endpoint: str, **kwargs) -> requests.Response:
        """Метод отправки GET-запроса"""
        return self._send_request("GET", endpoint, **kwargs)

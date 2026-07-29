import allure
from requests import HTTPError

from api.base_api import BaseApi
from api.endpoints import DISK_INFO_ENDPOINT


class DiskApi(BaseApi):
    @allure.step("Получить информацию о диске")
    def get_disk_info(self, **kwargs):
        """Метод получения информации о диске"""
        try:
           return self.get_request(DISK_INFO_ENDPOINT, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 401:
                return e.response
            raise

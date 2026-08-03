import allure
from requests import HTTPError

from api.base_api import BaseApi
from api.endpoints import DISK_INFO_ENDPOINT, RESOURCES_ENDPOINT, TRASH_ENDPOINT, RECOVER_ENDPOINT


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

    @allure.step("Добавить ресурс на диск")
    def add_resource(self, path: str, **kwargs):
        """Метод добавления ресурса на диск"""
        try:
            params = {"path": path}
            return self.put_request(RESOURCES_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 409:
                return e.response
            if e.response.status_code == 400:
                return e.response
            raise

    @allure.step("Получить информацию о ресурсе на диске")
    def get_resource_info(self, path: str, **kwargs):
        """Метод получения информации о ресурсе на диске"""
        try:
            params = {"path": path}
            return self.get_request(RESOURCES_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 404:
                return e.response
            raise
        
    @allure.step("Удалить ресурс навсегда")
    def delete_resource_permanently(self, path: str, **kwargs):
        """Метод удаления ресурса на диске"""
        params = {"path": path, "permanently": "true"}
        return self.delete_request(RESOURCES_ENDPOINT, params=params, **kwargs)

    @allure.step("Удалить ресурс в корзину")
    def delete_resource_to_trash(self, path: str, **kwargs):
        """Метод удаления ресурса на диске"""
        try:
            params = {"path": path}
            return self.delete_request(RESOURCES_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 404:
                return e.response
            raise

    @allure.step("Получить информацию о всех ресурсах в корзине")
    def get_all_trash_info(self, **kwargs):
        """Метод получения информации о ресурсе в корзине"""
        try:
            return self.get_request(TRASH_ENDPOINT, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 404:
                return e.response
            raise

    @allure.step("Восстановить ресурс из корзины")
    def recover_resource_from_trash(self, path: str, **kwargs):
        """Метод восстановления ресурса из корзины"""
        try:
            params = {"path": path}
            return self.put_request(RECOVER_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 405:
                return e.response
            raise

    @allure.step("Удалить ресурс навсегда из корзины")
    def delete_resource_permanently_from_trash(self, path: str, **kwargs):
        """Метод удаления ресурса из корзины"""
        params = {"path": path}
        return self.delete_request(TRASH_ENDPOINT, params=params, **kwargs)
import allure
from requests import HTTPError

from api.base_api import BaseApi
from api.endpoints import (COPY_ENDPOINT, DISK_INFO_ENDPOINT, DOWNLOAD_ENDPOINT, RECOVER_ENDPOINT,
                           RESOURCES_ENDPOINT, TRASH_ENDPOINT, UPLOAD_ENDPOINT)
from models import QueryModel


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
            params = QueryModel(path=path)
            return self.put_request(RESOURCES_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code in (409, 400):
                return e.response
            raise

    @allure.step("Получить информацию о ресурсе на диске")
    def get_resource_info(self, path: str, **kwargs):
        """Метод получения информации о ресурсе на диске"""
        try:
            params = QueryModel(path=path)
            return self.get_request(RESOURCES_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 404:
                return e.response
            raise

    @allure.step("Удалить ресурс навсегда")
    def delete_resource_permanently(self, path: str, **kwargs):
        """Метод удаления ресурса на диске"""
        params = QueryModel(path=path, permanently=True)
        return self.delete_request(RESOURCES_ENDPOINT, params=params, **kwargs)

    @allure.step("Удалить ресурс в корзину")
    def delete_resource_to_trash(self, path: str, **kwargs):
        """Метод удаления ресурса на диске"""
        try:
            params = QueryModel(path=path)
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
            params = QueryModel(path=path)
            return self.put_request(RECOVER_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 405:
                return e.response
            raise

    @allure.step("Удалить ресурс навсегда из корзины")
    def delete_resource_permanently_from_trash(self, path: str, **kwargs):
        """Метод удаления ресурса из корзины"""
        params = QueryModel(path=path)
        return self.delete_request(TRASH_ENDPOINT, params=params, **kwargs)

    @allure.step("Загрузить файл на диск {local_file_path} в {disk_path}")
    def upload_file(self, local_file_path: str, disk_path: str, **kwargs):
        """Метод загрузки файла на диск"""

        try:
            response = self.get_link_to_upload_file(disk_path)
            href = response.json()["href"]

            with open(local_file_path, "rb") as file:
                return self.put_request(href, data=file, **kwargs)

        except HTTPError as e:
            if e.response.status_code in (409, 400):
                return e.response
            raise

    @allure.step("Получить ссылку для загрузки файла на диск {path}")
    def get_link_to_upload_file(self, path: str, **kwargs):
        """Метод получения ссылки для загрузки файла на диск"""
        try:
            params = QueryModel(path=path)
            return self.get_request(UPLOAD_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code in (409, 400):
                return e.response
            raise

    @allure.step("Копирование ресурса {from_path} в {to_path}")
    def copy_resource(self, from_path: str, to_path: str, **kwargs):
        """Метод копирования ресурса на диске"""
        try:
            params = QueryModel(path=to_path, from_path=from_path).model_dump(
                by_alias=True, exclude_none=True
            )
            return self.post_request(COPY_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code in (409, 400):
                return e.response
            raise

    @allure.step("Получить ссылку для скачивания файла с диска {path}")
    def get_download_link(self, path: str, **kwargs):
        """Метод получения ссылки для скачивания файла с диска"""
        try:
            params = QueryModel(path=path)
            return self.get_request(DOWNLOAD_ENDPOINT, params=params, **kwargs)
        except HTTPError as e:
            if e.response.status_code in (409, 400):
                return e.response
            raise

    @allure.step("Скачивание файла с диска {path}")
    def download_file(self, path: str, **kwargs):
        """Метод скачивания файла с диска"""
        try:
            response = self.get_download_link(path)
            href = response.json()["href"]

            return self.get_request(href, **kwargs)
        except HTTPError as e:
            if e.response.status_code in (409, 400):
                return e.response
            raise
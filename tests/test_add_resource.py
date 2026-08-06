import allure
import pytest

from helpers.assertions import assert_status_code
from helpers.data import MAX_LENGTH_TITLE, TEST_FOLDER_NAME
from helpers.helper import validate_response
from models import ErrorResponse, OperationResponse


@allure.epic("Добавление ресурсов")
@allure.feature("Проверка добавления ресурсов")
class TestAddResource:
    """Тесты на добавление ресурсов"""

    @allure.story("Создание папки")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "folder_name",
        [TEST_FOLDER_NAME, "a" * MAX_LENGTH_TITLE],
        ids=["Обычное название", "Максимальная длина названия"],
    )
    def test_add_folder(self, disk_api, folder_name):
        """Тест на добавление папки"""
        response_add = disk_api.add_resource(path=folder_name)

        assert_status_code(response_add, 201)
        validate_response(OperationResponse, response_add)

        response_get = disk_api.get_resource_info(path=folder_name)
        assert_status_code(response_get, 200)

        disk_api.delete_resource_permanently(path=folder_name)

    @allure.story("Создание уже существующей папки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_existing_folder(self, disk_api, created_folder):
        """Тест на добавление уже существующей папки"""
        response = disk_api.add_resource(path=created_folder)

        assert_status_code(response, 409)
        validate_response(ErrorResponse, response)

    @allure.story("Создание подпапки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_sub_folder(self, disk_api, created_folder):
        """Тест на добавление подпапки"""
        response_add_sub = disk_api.add_resource(path=f"{created_folder}/sub-folder")

        assert_status_code(response_add_sub, 201)
        validate_response(OperationResponse, response_add_sub)

        response_get_sub = disk_api.get_resource_info(
            path=f"{created_folder}/sub-folder"
        )
        assert_status_code(response_get_sub, 200)

    @allure.story("Создание подпапки без существующей родительской папки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_sub_folder_without_parent(self, disk_api):
        """Тест на добавление подпапки без существующей родительской папки"""
        response = disk_api.add_resource(path="nonexist-parent/sub-folder")

        assert_status_code(response, 409)
        validate_response(ErrorResponse, response)

    @allure.story("Создание папки без названия")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_folder_without_title(self, disk_api):
        """Тест на добавление папки без названия"""
        response = disk_api.add_resource(path="")

        assert_status_code(response, 400)
        validate_response(ErrorResponse, response)

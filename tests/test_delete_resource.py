import allure

from helpers.assertions import (assert_required_fields,
                                assert_resource_in_trash, assert_status_code)
from helpers.helper import get_path_from_trash


@allure.epic("Удаление ресурсов")
@allure.feature("Проверка удаления ресурсов")
class TestDeleteResource:
    """Тесты на удаление ресурса"""

    @allure.story("Удаление ресурса в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_resource_to_trash(self, disk_api):
        """Тест на перемещение ресурса в корзину"""
        created_folder = "test_folder_delete"
        disk_api.add_resource(created_folder)
        response = disk_api.delete_resource_to_trash(created_folder)
        assert_status_code(response, 204)

        response_get = disk_api.get_resource_info(created_folder)
        assert_status_code(response_get, 404)

    @allure.story("Удаление несуществующего ресурса")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_nonexistent_resource(self, disk_api):
        """Тест на удаление несуществующего ресурса"""
        folder_path = "nonexistent_folder"

        response = disk_api.delete_resource_to_trash(folder_path)
        assert_status_code(response, 404)

    @allure.story("Удаление ресурса навсегда")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_resource_permanently(self, disk_api):
        """Тест на удаление ресурса навсегда"""
        created_folder = "test_folder_permanent_delete"
        disk_api.add_resource(created_folder)
        response = disk_api.delete_resource_permanently(created_folder)
        assert_status_code(response, 204)

        response_get = disk_api.get_resource_info(created_folder)
        assert_status_code(response_get, 404)

    @allure.story("Удаление ресурса из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_resource_from_trash(self, disk_api):
        """Тест на удаление ресурса из корзины"""
        created_folder = "test_folder_trash"
        disk_api.add_resource(created_folder)
        disk_api.delete_resource_to_trash(created_folder)

        response_get = disk_api.get_all_trash_info()
        assert_status_code(response_get, 200)
        response_data = response_get.json()
        assert_required_fields(response_data, ["_embedded"])
        assert_resource_in_trash(response_data, created_folder)
        path_in_trash = get_path_from_trash(response_data, created_folder)

        disk_api.delete_resource_permanently_from_trash(path=path_in_trash)

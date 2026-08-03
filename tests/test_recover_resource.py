import allure

from helpers.assertions import (
    assert_required_fields,
    assert_resource_in_trash,
    assert_status_code,
)
from helpers.helper import get_path_from_trash


@allure.epic("Восстановление ресурсов")
@allure.feature("Проверка восстановления ресурсов")
class TestRecoverResource:
    """Тесты на восстановление ресурса из корзины"""

    @allure.story("Восстановление ресурса из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_recover_resource(self, disk_api, created_folder):
        """Тест на восстановление ресурса из корзины"""
        disk_api.delete_resource_to_trash(created_folder)

        response_get = disk_api.get_all_trash_info()
        response_get_data = response_get.json()
        assert_status_code(response_get, 200)
        assert_required_fields(response_get_data, ["_embedded"])
        assert_resource_in_trash(response_get_data, created_folder)
        path_in_trash = get_path_from_trash(response_get_data, created_folder)
        response_recover = disk_api.recover_resource_from_trash(path_in_trash)
        assert_status_code(response_recover, 204, 201)

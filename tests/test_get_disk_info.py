import os

import allure

from helpers.assertions import (
    assert_field_value,
    assert_required_fields,
    assert_status_code,
)
from helpers.helper import validate_response
from models import ErrorResponse


@allure.epic("Авторизация")
@allure.feature("Проверка авторизации")
class TestAuth:
    """Класс для тестов авторизации"""

    @allure.story("Авторизация с валидным токеном")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_disk_info_auth(self, disk_api):
        """Проверка авторизации с валидным токеном"""
        response = disk_api.get_disk_info()
        response_data = response.json()

        assert_status_code(response, 200)

        assert_required_fields(response_data, ["user"])
        assert_field_value(response_data["user"], "login", os.getenv("LOGIN"))
        assert_field_value(
            response_data["user"], "display_name", os.getenv("DISPLAY_NAME")
        )

    @allure.story("Авторизация без токена")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_disk_info_no_auth(self, disk_api):
        """Проверка авторизации без токена"""
        response = disk_api.get_disk_info(auth=False)

        assert_status_code(response, 401)
        validate_response(ErrorResponse, response)

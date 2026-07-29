import allure


@allure.step("Проверить код статуса ответа")
def assert_status_code(response, expected_status_code):
    """Проверка кода статуса ответа"""
    assert response.status_code == expected_status_code, (
        f"Ожидался статус {expected_status_code}, получен {response.status_code}"
    )


@allure.step("Проверить наличие полей в теле ответа")
def assert_required_fields(response_data: dict, required_fields: list):
    """Проверка наличия требуемых полей в теле ответа"""
    for field in required_fields:
        assert field in response_data, f"Поле '{field}' отсутствует в ответе"


@allure.step("Проверить значение поля '{field}' в теле ответа")
def assert_field_value(response_data: dict, field: str, expected_value):
    """Проверка значения поля в теле ответа"""
    assert response_data.get(field) == expected_value, (
        f"Ожидалось значение '{expected_value}' для поля '{field}', получено '{response_data.get(field)}'"
    )

from pathlib import Path

import allure
import jsonschema
from pydantic import BaseModel, ValidationError


@allure.step("Получение пути ресурса в корзине")
def get_path_from_trash(response_data: dict, resource_title: str) -> str:
    """Получение пути ресурса в корзине"""
    items = items = response_data["_embedded"]["items"]
    return next(item["path"] for item in items if resource_title in item["path"])


@allure.step("Генерация текстового файла")
def generate_txt_file(text: str):
    """Генерация текстового файла"""
    file_path = Path("data.txt")
    with open(file_path, "w") as f:
        f.write(text)
    return file_path


@allure.step("Проверить тело ответа")
def validate_response(model: type[BaseModel], response):
    """Проверка тела ответа"""
    try:
        return model.model_validate(response.json())
    except ValidationError as e:
        raise AssertionError(f"Ошибка валидации: {e}")


@allure.step("Проверка JSON схемы")
def validate_json_schema(json_data: dict, schema: dict):
    """Проверка JSON схемы"""
    try:
        jsonschema.validate(json_data, schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Ошибка валидации: {e}")

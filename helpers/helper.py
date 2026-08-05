from pathlib import Path

import allure
from pydantic import BaseModel, ValidationError


def get_path_from_trash(response_data: dict, resource_title: str) -> str:
    """Получение пути ресурса в корзине"""
    items = items = response_data["_embedded"]["items"]
    return next(item["path"] for item in items if resource_title in item["path"])


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

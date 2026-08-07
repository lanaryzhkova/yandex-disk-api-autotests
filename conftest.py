import os
import uuid

import pytest
from dotenv import load_dotenv

from api.disk_api import DiskApi
from helpers.data import TEST_FOLDER_NAME

load_dotenv()


@pytest.fixture(scope="session")
def get_base_url():
    """Возвращает BASE_URL из переменной окружения"""
    return os.getenv("BASE_URL")


@pytest.fixture()
def disk_api(get_base_url):
    """Возвращает клиент для работы с API диска"""
    return DiskApi(get_base_url)


@pytest.fixture
def folder_name():
    """Возвращает уникальное название папки для тестов"""
    return f"{TEST_FOLDER_NAME}_{uuid.uuid4().hex}"


@pytest.fixture(scope="function")
def created_folder(disk_api, folder_name):
    """Создает папку перед тестом и удаляет ее после теста"""
    folder = folder_name
    disk_api.add_resource(folder)
    yield folder
    disk_api.delete_resource_permanently(folder)

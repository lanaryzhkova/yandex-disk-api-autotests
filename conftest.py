import os

import pytest
from dotenv import load_dotenv

from api.disk_api import DiskApi

load_dotenv()

@pytest.fixture(scope="session")
def get_base_url():
    """Возвращает BASE_URL из переменной окружения"""
    return os.getenv("BASE_URL")

@pytest.fixture()
def disk_api(get_base_url):
    """Возвращает клиент для работы с API диска"""
    return DiskApi(get_base_url)
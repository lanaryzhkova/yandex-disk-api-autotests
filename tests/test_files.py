import allure

from helpers.assertions import assert_status_code
from helpers.data import FILES_LIST_SCHEMA, TXT_FILE_CONTENT
from helpers.helper import generate_txt_file, validate_json_schema, validate_response
from models import ErrorResponse, OperationResponse


@allure.epic("Файлы")
@allure.feature("Проверка загрузки и копирования файла")
class TestFiles:
    """Тесты для проверки загрузки и копирования файла"""

    @allure.story("Проверка загрузки и копирования файла")
    @allure.severity(allure.severity_level.NORMAL)
    def test_upload_copy_file(self, disk_api):
        disk_api.add_resource(path="input_data")
        disk_api.add_resource(path="output_data")
        file_content = TXT_FILE_CONTENT
        file_path = generate_txt_file(file_content)
        response_upload = disk_api.upload_file(
            local_file_path=file_path, disk_path="input_data/data.txt"
        )

        assert_status_code(response_upload, 200, 201)

        response_copy = disk_api.copy_resource(
            from_path="input_data/data.txt", to_path="output_data/data.txt"
        )
        assert_status_code(response_copy, 201)
        validate_response(OperationResponse, response_copy)

        response_copy_2 = disk_api.copy_resource(
            from_path="input_data/data.txt", to_path="output_data/data.txt"
        )
        validate_response(ErrorResponse, response_copy_2)
        assert_status_code(response_copy_2, 409)

        disk_api.delete_resource_permanently(path="input_data")
        disk_api.delete_resource_permanently(path="output_data")

    @allure.story("Проверка загрузки и скачивания файла")
    @allure.severity(allure.severity_level.NORMAL)
    def test_download_file(self, disk_api):
        """Тест на проверку скачивания файла"""
        disk_path = "sdet_data"
        disk_api.add_resource(path=disk_path)
        file_content = TXT_FILE_CONTENT
        file_path = generate_txt_file(file_content)
        response_upload = disk_api.upload_file(
            local_file_path=file_path, disk_path=f"{disk_path}/data.txt"
        )
        assert_status_code(response_upload, 200, 201)

        response_download = disk_api.download_file(path=f"{disk_path}/data.txt")
        assert_status_code(response_download, 200)
        assert response_download.content == file_content.encode(), (
            f"Ожидалось содержимое '{file_content}', получено '{response_download.content}'"
        )

        disk_api.delete_resource_permanently(path=disk_path)

    @allure.story("Проверка получения списка файлов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_files_list(self, disk_api):
        """Тест на получение списка файлов"""
        response = disk_api.get_files_list()
        assert_status_code(response, 200)
        validate_json_schema(response.json(), FILES_LIST_SCHEMA)

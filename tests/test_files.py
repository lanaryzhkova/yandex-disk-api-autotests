import allure

from helpers.assertions import assert_status_code
from helpers.helper import generate_txt_file, validate_response
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

        file_path = generate_txt_file()
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

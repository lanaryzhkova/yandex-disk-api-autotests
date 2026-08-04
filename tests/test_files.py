from helpers.assertions import assert_required_fields, assert_status_code
from helpers.helper import generate_txt_file


class TestFiles:
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
        # assert_required_fields(response_copy_data, ["name", "mime_type", "media_type"]) - не соответствует документации

        response_copy_2 = disk_api.copy_resource(
                    from_path="input_data/data.txt", to_path="output_data/data.txt"
                )
        response_copy_data_2 = response_copy_2.json()
        assert_status_code(response_copy_2, 409)
        assert_required_fields(response_copy_data_2, ["error", "description", "message"])

        disk_api.delete_resource_permanently(path="input_data")
        disk_api.delete_resource_permanently(path="output_data")
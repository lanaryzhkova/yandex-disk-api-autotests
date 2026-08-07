MAX_LENGTH_TITLE = 255
TEST_FOLDER_NAME = "D4-test-catalog"
TXT_FILE_CONTENT = "username=SDET password=secret_key"

FILES_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "total": {"type": "number"},
        "limit": {"type": "number"},
        "offset": {"type": "number"},
        "items": {"type": "array", "items": {"$ref": "#/definitions/resource"}},
        "media_type": {"type": "string"},
        "file": {"type": "string"},
        "resource_id": {"type": "string"},
        "share": {"$ref": "#/definitions/share"},
        "revision": {"type": "number"},
        "comment_ids": {"$ref": "#/definitions/comment_ids"},
        "custom_properties": {"type": "object"},
        "exif": {"$ref": "#/definitions/exif"},
        "antivirus_status": {"type": "object"},
        "photoslice_time": {"type": "string", "format": "date-time"},
        "sizes": {"type": "array", "items": {"$ref": "#/definitions/size"}},
    },
    "definitions": {
        "resource": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "type": {"type": "string"},
                "name": {"type": "string"},
                "created": {"type": "string", "format": "date-time"},
                "modified": {"type": "string", "format": "date-time"},
                "size": {"type": "number"},
                "mime_type": {"type": "string"},
                "md5": {"type": "string"},
                "sha256": {"type": "string"},
                "preview": {"type": "string"},
                "public_key": {"type": "string"},
                "public_url": {"type": "string"},
                "_embedded": {
                    "total": {"type": "number"},
                    "limit": {"type": "number"},
                    "offset": {"type": "number"},
                    "path": {"type": "string"},
                    "sort": {"type": "string"},
                    "items": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/resource"},
                    },
                },
            },
            "required": [
                "path",
                "type",
                "name",
                "created",
                "modified",
            ],
        },
        "share": {
            "type": "object",
            "properties": {
                "is_owned": {"type": "boolean"},
                "is_root": {"type": "boolean"},
                "rights": {"type": "string"},
            },
            "required": ["rights"],
        },
        "comment_ids": {
            "type": "object",
            "properties": {
                "public_resource": {"type": "string"},
                "private_resource": {"type": "string"},
            },
            "exif": {
                "type": "object",
                "properties": {
                    "data_time": {"type": "string", "format": "date-time"},
                    "gps_latitude": {"type": "object"},
                    "gps_longitude": {"type": "object"},
                },
            },
            "size": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "name": {"type": "string"},
                },
            },
        },
    },
    "required": ["items"],
}

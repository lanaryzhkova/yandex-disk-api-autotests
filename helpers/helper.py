def get_path_from_trash(response_data: dict, resource_title: str) -> str:
    """Получение пути ресурса в корзине"""
    items = items = response_data["_embedded"]["items"]
    return next(item["path"] for item in items if resource_title in item["path"])

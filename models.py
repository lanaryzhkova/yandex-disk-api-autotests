from pydantic import BaseModel, ConfigDict, Field


class OperationResponse(BaseModel):
    """Класс для модели ответа на операцию"""

    method: str
    href: str
    templated: bool
    operation_id: str | None = None


class ErrorResponse(BaseModel):
    """Класс для модели ответа на ошибку"""

    error: str
    description: str
    message: str
    details: dict | None = None


class QueryModel(BaseModel):
    """Класс для модели запроса"""

    model_config = ConfigDict(populate_by_name=True)

    path: str
    url: str | None = None
    permanently: bool | None = None
    from_path: str | None = Field(default=None, alias="from")

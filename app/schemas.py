"""Pydantic-схемы для валидации входных и выходных данных."""
from pydantic import BaseModel


class PostCreate(BaseModel):
    """Схема запроса для создания публикации."""
    title: str
    content: str


class PostOut(BaseModel):
    """Схема ответа для публикации."""
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True

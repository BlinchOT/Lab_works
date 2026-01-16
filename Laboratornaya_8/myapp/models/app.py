"""Модель приложения."""

from dataclasses import dataclass
from typing import Optional
from .author import Author


@dataclass
class App:
    """Класс, представляющий приложение."""

    name: str
    version: str
    author: Optional[Author] = None

    def __post_init__(self):
        """Проверка корректности данных после инициализации."""
        if not isinstance(self.name, str) or len(self.name.strip()) < 2:
            raise ValueError("Название приложения должно быть строкой длиной не менее 2 символов")
        if not isinstance(self.version, str):
            raise ValueError("Версия должна быть строкой")

    def __str__(self) -> str:
        """Строковое представление приложения."""
        author_info = f", автор: {self.author.name}" if self.author else ""
        return f"{self.name} v{self.version}{author_info}"
"""Модель связи пользователь-валюта."""

from dataclasses import dataclass


@dataclass
class UserCurrency:
    """Класс, представляющий связь между пользователем и валютой."""

    id: int
    user_id: int
    currency_id: int

    def __post_init__(self):
        """Проверка корректности данных после инициализации."""
        if not all(isinstance(x, int) and x > 0
                   for x in [self.id, self.user_id, self.currency_id]):
            raise ValueError("Все ID должны быть положительными целыми числами")
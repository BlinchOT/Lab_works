"""Модель валюты."""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Currency:
    """Класс, представляющий валюту и её курс."""

    id: int
    num_code: str
    char_code: str
    name: str
    value: float
    nominal: int

    def __post_init__(self):
        """Проверка корректности данных после инициализации."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID должен быть положительным целым числом")
        if not isinstance(self.num_code, str) or len(self.num_code) != 3:
            raise ValueError("Цифровой код должен состоять из 3 символов")
        if not isinstance(self.char_code, str) or len(self.char_code) != 3:
            raise ValueError("Символьный код должен состоять из 3 символов")
        if not isinstance(self.value, (int, float)) or self.value <= 0:
            raise ValueError("Курс должен быть положительным числом")
        if not isinstance(self.nominal, int) or self.nominal <= 0:
            raise ValueError("Номинал должен быть положительным целым числом")

    @property
    def value_per_unit(self) -> float:
        """Получить курс за одну единицу валюты."""
        return self.value / self.nominal

    def __str__(self) -> str:
        """Строковое представление валюты."""
        return f"{self.char_code} ({self.name}): {self.value} за {self.nominal}"
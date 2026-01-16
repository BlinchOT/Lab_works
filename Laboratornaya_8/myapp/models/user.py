"""Модель пользователя."""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class User:
    """Класс, представляющий пользователя системы."""

    id: int
    name: str
    subscribed_currencies: List['Currency'] = field(default_factory=list)

    def __post_init__(self):
        """Проверка корректности данных после инициализации."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID должен быть положительным целым числом")
        if not isinstance(self.name, str) or len(self.name.strip()) < 2:
            raise ValueError("Имя должно быть строкой длиной не менее 2 символов")

    def subscribe_to_currency(self, currency: 'Currency') -> None:
        """Добавить валюту в список подписок пользователя."""
        if currency not in self.subscribed_currencies:
            self.subscribed_currencies.append(currency)

    def unsubscribe_from_currency(self, currency_id: int) -> None:
        """Удалить валюту из списка подписок."""
        self.subscribed_currencies = [
            c for c in self.subscribed_currencies
            if c.id != currency_id
        ]

    def get_subscription_ids(self) -> List[int]:
        """Получить список ID валют, на которые подписан пользователь."""
        return [c.id for c in self.subscribed_currencies]
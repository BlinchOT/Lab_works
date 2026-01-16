"""
Функция для получения курсов валют с API Центробанка России.
Без логирования - только бизнес-логика и исключения.
"""

import requests
from typing import Dict, List, Union
import json


def get_currencies(
        currency_codes: List[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Dict[str, Union[float, str]]:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes: Список символьных кодов валют (например, ['USD', 'EUR'])
        url: URL API Центробанка России

    Returns:
        Словарь, где ключи - символьные коды валют,
        а значения - их курсы (float) или сообщение об ошибке (str).

    Raises:
        requests.exceptions.RequestException: При ошибках сети или недоступности API
        ValueError: При некорректном JSON ответе
        KeyError: При отсутствии ключа "Valute" в ответе (только если JSON корректен)
        TypeError: При неверном типе курса валюты

    Примечание:
        - Если валюта не найдена в ответе, возвращает строку с сообщением об ошибке
        - Не выбрасывает исключение для отсутствующей валюты
    """

    # Валидация входных данных
    if not isinstance(currency_codes, list):
        raise TypeError("currency_codes должен быть списком")

    if not all(isinstance(code, str) for code in currency_codes):
        raise TypeError("Все коды валют должны быть строками")

    try:
        # Выполняем HTTP-запрос
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверяем HTTP ошибки

    except requests.exceptions.RequestException as e:
        # Все ошибки сети, таймауты, недоступность API
        # НЕ логируем здесь, только выбрасываем исключение
        raise requests.exceptions.RequestException(
            f"Ошибка при запросе к API: {type(e).__name__}: {str(e)}"
        )

    try:
        # Парсим JSON
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON ответ от API: {str(e)}")

    # Проверяем структуру JSON
    if "Valute" not in data:
        # Если структура изменилась, но запрос прошел успешно
        # Согласно подсказкам - НЕ выбрасываем исключение
        # Возвращаем сообщения об ошибке для всех запрошенных валют
        return {code: f"Ключ 'Valute' не найден в ответе API" for code in currency_codes}

    currencies = {}

    for code in currency_codes:
        if code not in data["Valute"]:
            # Валюта отсутствует в данных
            # Согласно подсказкам - НЕ выбрасываем исключение
            currencies[code] = f"Код валюты '{code}' не найден."
            continue

        try:
            value = data["Valute"][code]["Value"]

            # Проверяем тип курса валюты
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Курс валюты '{code}' имеет неверный тип: {type(value).__name__}"
                )

            currencies[code] = float(value)

        except KeyError:
            # Отсутствует нужное поле в структуре валюты
            currencies[code] = f"Некорректная структура данных для валюты '{code}'"
        except TypeError as e:
            # Пробрасываем TypeError как есть (требуется по заданию)
            raise
        except Exception as e:
            # Любая другая ошибка при обработке валюты
            currencies[code] = f"Ошибка обработки валюты '{code}': {str(e)}"

    return currencies


if __name__ == "__main__":
    # Примеры использования
    import sys

    print("=== Тестирование функции get_currencies ===")

    try:
        # Пример 1: Корректный запрос
        print("1. Корректный запрос (USD, EUR):")
        result = get_currencies(["USD", "EUR"])
        for code, value in result.items():
            print(f"  {code}: {value}")
        print()

        # Пример 2: Несуществующая валюта
        print("2. Запрос с несуществующей валютой:")
        result = get_currencies(["USD", "XYZ"])
        for code, value in result.items():
            print(f"  {code}: {value}")
        print()

        # Пример 3: Ошибка сети (закомментируйте для теста)
        # print("3. Запрос с неверным URL (должен вызвать RequestException):")
        # result = get_currencies(["USD"], url="https://invalid-url")

    except Exception as e:
        print(f"Поймано исключение: {type(e).__name__}: {str(e)}")
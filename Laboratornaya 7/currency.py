import functools
import requests
import sys
import io


def get_currencies(currency_codes: list, url:str = "https://www.cbr-xml-daily.ru/daily_json.js")->dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    response = requests.get(url)

    # print(response.status_code)
    response.raise_for_status()  # Проверка на ошибки HTTP
    data = response.json()
    # print(data)
    currencies = {}

    if "Valute" in data:
        for code in currency_codes:
            if code in data["Valute"]:
                currencies[code] = data["Valute"][code]["Value"]
            else:
                currencies[code] = f"Код валюты '{code}' не найден."
    return currencies
    # raise requests.exceptions.RequestException('Упали с исключением')


if __name__ == "__main__":
    # Пример использования функции:
    currency_list = ['USD', 'EUR', 'GBP', 'NNZ']

    currency_data = get_currencies(currency_list)
    if currency_data:
         print(currency_data)
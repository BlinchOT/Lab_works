"""
Демонстрационный файл для лабораторной работы 7.
"""

import sys
import io
import logging
from decorators import logger
from currency import get_currencies


# Импортируем если создали quadratic.py
# from quadratic import solve_quadratic


def demo_basic_logging():
    """Демонстрация базового логирования."""
    print("=== Базовое логирование ===")

    @logger
    def simple_func(x, y):
        return x + y

    print("Вызов simple_func(3, 4):")
    result = simple_func(3, 4)
    print(f"Результат: {result}")
    print()


def demo_stringio_logging():
    """Демонстрация логирования в StringIO."""
    print("=== Логирование в StringIO ===")

    stream = io.StringIO()

    @logger(handle=stream)
    def stringio_func(a, b):
        return a * b

    print("Вызов stringio_func(5, 6):")
    result = stringio_func(5, 6)
    print(f"Результат: {result}")
    print("Логи из StringIO:")
    print(stream.getvalue())
    print()


def demo_file_logging():
    """Демонстрация логирования в файл (самостоятельная часть)."""
    print("=== Логирование в файл ===")

    # Настройка файлового логгера
    file_logger = logging.getLogger("currency_file")
    file_logger.setLevel(logging.DEBUG)
    file_logger.handlers.clear()

    file_handler = logging.FileHandler("currency.log", mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    file_logger.addHandler(file_handler)

    @logger(handle=file_logger)
    def file_logged_func(values):
        return sum(values)

    print("Вызов file_logged_func([1, 2, 3, 4, 5]):")
    result = file_logged_func([1, 2, 3, 4, 5])
    print(f"Результат: {result}")
    print("Логи записаны в файл 'currency.log'")
    print()


def demo_get_currencies_with_logging():
    """Демонстрация get_currencies с логированием."""
    print("=== get_currencies с логированием ===")

    # Декорируем оригинальную функцию
    @logger
    def get_currencies_logged(codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
        return get_currencies(codes, url)

    print("1. Успешный запрос:")
    try:
        result = get_currencies_logged(["USD", "EUR"])
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")
    print()

    print("2. Запрос с несуществующей валютой:")
    try:
        result = get_currencies_logged(["USD", "XYZ"])
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")
    print()

    print("3. Запрос с неверным URL (ожидается ошибка):")
    try:
        result = get_currencies_logged(["USD"], url="https://invalid-url")
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Поймано исключение: {type(e).__name__}")
    print()


def main():
    """Основная демонстрационная функция."""
    print("ДЕМОНСТРАЦИЯ ЛАБОРАТОРНОЙ РАБОТЫ 7")
    print("=" * 50)

    demo_basic_logging()
    demo_stringio_logging()
    demo_file_logging()
    demo_get_currencies_with_logging()

    print("=" * 50)
    print("Демонстрация завершена!")
    print("Для запуска тестов выполните: python test_currency.py")


if __name__ == "__main__":
    main()
"""
Тесты для лабораторной работы 7.
"""

import unittest
import io
import sys
import logging
from unittest.mock import patch, Mock
import requests

# Импорт тестируемых модулей
from decorators import logger, trace
from currency import get_currencies


class TestGetCurrenciesFunction(unittest.TestCase):
    """Тесты функции get_currencies (без декоратора)."""

    def test_get_currencies_success(self):
        """Тест успешного получения курсов валют."""
        try:
            result = get_currencies(["USD", "EUR"])

            # Проверяем структуру результата
            self.assertIsInstance(result, dict)
            self.assertIn("USD", result)
            self.assertIn("EUR", result)

            # Проверяем типы значений
            self.assertIsInstance(result["USD"], float)
            self.assertIsInstance(result["EUR"], float)

            # Курсы должны быть положительными
            self.assertGreater(result["USD"], 0)
            self.assertGreater(result["EUR"], 0)

        except requests.exceptions.RequestException:
            self.skipTest("Нет интернет-соединения")

    def test_get_currencies_nonexistent_code(self):
        """Тест запроса несуществующей валюты."""
        try:
            result = get_currencies(["USD", "XYZ"])

            # USD должен существовать
            self.assertIsInstance(result["USD"], float)

            # XYZ не должен существовать
            self.assertIsInstance(result["XYZ"], str)
            self.assertIn("не найден", result["XYZ"])
            self.assertIn("XYZ", result["XYZ"])

        except requests.exceptions.RequestException:
            self.skipTest("Нет интернет-соединения")

    @patch('currency.requests.get')
    def test_get_currencies_connection_error(self, mock_get):
        """Тест обработки ошибки соединения."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Ошибка соединения")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            get_currencies(["USD"], url="https://invalid-url")

        self.assertIn("ConnectionError", str(context.exception))

    @patch('currency.requests.get')
    def test_get_currencies_invalid_json(self, mock_get):
        """Тест обработки некорректного JSON."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            get_currencies(["USD"])

        self.assertIn("Некорректный JSON", str(context.exception))

    @patch('currency.requests.get')
    def test_get_currencies_missing_valute_key(self, mock_get):
        """Тест обработки ответа без ключа 'Valute'."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"SomeOtherKey": "data"}
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "EUR"])

        # Должны получить сообщения об ошибке для всех валют
        self.assertEqual(len(result), 2)
        self.assertIn("Ключ 'Valute' не найден", result["USD"])
        self.assertIn("Ключ 'Valute' не найден", result["EUR"])

    @patch('currency.requests.get')
    def test_get_currencies_invalid_currency_type(self, mock_get):
        """Тест обработки неверного типа курса валюты."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": "not-a-number", "Nominal": 1}
            }
        }
        mock_get.return_value = mock_response

        with self.assertRaises(TypeError) as context:
            get_currencies(["USD"])

        self.assertIn("неверный тип", str(context.exception))
        self.assertIn("USD", str(context.exception))


class TestLoggerDecorator(unittest.TestCase):
    """Тесты декоратора logger."""

    def test_logger_with_stdout(self):
        """Тест логирования в sys.stdout."""
        import io
        from contextlib import redirect_stdout

        # Захватываем вывод stdout
        f = io.StringIO()

        @logger
        def test_func(x, y=2):
            return x * y

        with redirect_stdout(f):
            result = test_func(3, y=4)

        output = f.getvalue()

        # Проверяем результат
        self.assertEqual(result, 12)

        # Проверяем логирование
        self.assertIn("test_func", output)
        self.assertIn("INFO:", output)
        self.assertIn("3", output)
        self.assertIn("y=4", output)
        self.assertIn("12", output)

    def test_logger_with_stringio(self):
        """Тест логирования в io.StringIO."""
        stream = io.StringIO()

        @logger(handle=stream)
        def string_io_func(a, b):
            return a + b

        result = string_io_func("Hello, ", "World!")

        # Проверяем результат
        self.assertEqual(result, "Hello, World!")

        # Проверяем логи в StringIO
        logs = stream.getvalue()
        self.assertIn("string_io_func", logs)
        self.assertIn("Hello, ", logs)
        self.assertIn("World!", logs)
        self.assertIn("Hello, World!", logs)

    def test_logger_with_logging(self):
        """Тест логирование через logging.Logger."""
        # Создаем логгер с обработчиком в StringIO
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        test_logger = logging.getLogger("test_logger")
        test_logger.setLevel(logging.INFO)
        test_logger.handlers.clear()
        test_logger.addHandler(handler)

        @logger(handle=test_logger)
        def logging_func(x):
            if x < 0:
                raise ValueError("Отрицательное число")
            return x * 2

        # Тестируем успешный вызов
        result = logging_func(5)
        self.assertEqual(result, 10)

        # Проверяем логи
        logs = log_stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("logging_func", logs)
        self.assertIn("5", logs)
        self.assertIn("10", logs)

        # Тестируем вызов с ошибкой
        log_stream.truncate(0)
        log_stream.seek(0)

        with self.assertRaises(ValueError):
            logging_func(-3)

        # Проверяем логи ошибки
        logs = log_stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Отрицательное число", logs)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты декоратора и функции get_currencies."""

    def setUp(self):
        """Подготовка тестового окружения."""
        self.stream = io.StringIO()

        # Декорируем get_currencies
        @logger(handle=self.stream)
        def get_currencies_logged(codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
            return get_currencies(codes, url)

        self.get_currencies_logged = get_currencies_logged

    def test_logging_success_integration(self):
        """Тест логирования при успешном выполнении get_currencies."""
        try:
            result = self.get_currencies_logged(["USD"])

            # Проверяем результат
            self.assertIsInstance(result, dict)
            self.assertIn("USD", result)

            # Проверяем логи
            logs = self.stream.getvalue()
            self.assertIn("get_currencies_logged", logs)
            self.assertIn("INFO:", logs)
            self.assertIn("USD", logs)

        except requests.exceptions.RequestException:
            self.skipTest("Нет интернет-соединения")

    @patch('currency.requests.get')
    def test_logging_error_integration(self, mock_get):
        """Тест логирования при ошибке в get_currencies."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Ошибка соединения")

        with self.assertRaises(requests.exceptions.RequestException):
            self.get_currencies_logged(["USD"], url="https://invalid-url")

        # Проверяем логи ошибки
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
        self.assertIn("Ошибка при запросе к API", logs)


class TestStreamWrite(unittest.TestCase):
    """Тесты из исходного задания."""

    def setUp(self):
        self.stream = io.StringIO()

        # Декорируем функцию для тестирования
        @logger(handle=self.stream)
        def wrapped_func(codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
            return get_currencies(codes, url)

        self.wrapped_func = wrapped_func

    def test_logging_error_in_stream(self):
        """Тест записи ошибки в поток."""
        with self.assertRaises(requests.exceptions.RequestException):
            self.wrapped_func(['USD'], url="https://invalid-url")

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("RequestException", logs)


# Запуск тестов
if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
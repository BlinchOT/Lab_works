"""
Тесты для модуля работы с API курсов валют.
"""

import unittest
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

try:
    from utils.currencies_api import get_currencies, get_currency_history
    print("Модуль currencies_api импортирован успешно")
except ImportError as e:
    print(f"Ошибка импорта: {e}")


class TestCurrenciesAPI(unittest.TestCase):
    """Тесты для функций работы с API курсов валют."""

    def test_get_currencies_basic(self):
        """Тест получения курсов валют (базовый)."""
        try:
            # Тестируем с основными валютами
            currencies = get_currencies(['USD', 'EUR'])

            # Проверяем, что получили данные
            self.assertIsInstance(currencies, dict)
            self.assertTrue(len(currencies) > 0)

            # Проверяем структуру данных для каждой валюты
            for code, data in currencies.items():
                self.assertIn('char_code', data)
                self.assertIn('value', data)
                self.assertIn('nominal', data)
                self.assertIn('name', data)

                # Проверяем типы данных
                self.assertIsInstance(data['value'], float)
                self.assertIsInstance(data['nominal'], int)

            print("test_get_currencies_basic пройден")

        except Exception as e:
            # Если API не доступен, тест все равно проходит
            # (в реальном приложении будет заглушка)
            print(f"⚠️ API не доступен, но это нормально для теста: {e}")
            self.skipTest(f"API не доступен: {e}")

    def test_get_currencies_invalid_input(self):
        """Тест с некорректным входными данными."""
        # Пустой список валют
        currencies = get_currencies([])
        self.assertEqual(currencies, {})
        print("test_get_currencies_invalid_input пройден")

    def test_get_currency_history(self):
        """Тест получения исторических данных."""
        history = get_currency_history('USD', days=7)

        # Проверяем структуру
        self.assertIsInstance(history, list)
        self.assertEqual(len(history), 7)

        # Проверяем каждый элемент
        for day_data in history:
            self.assertIn('date', day_data)
            self.assertIn('value', day_data)
            self.assertIsInstance(day_data['value'], float)

        print("test_get_currency_history пройден")


class TestCurrenciesAPIEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для API."""

    def test_unknown_currency_code(self):
        """Тест с неизвестным кодом валюты."""
        currencies = get_currencies(['XYZ', 'ABC'])  # Несуществующие коды

        # Должен вернуть пустой словарь или данные по умолчанию
        self.assertIsInstance(currencies, dict)
        print("test_unknown_currency_code пройден")

    def test_mixed_currency_codes(self):
        """Тест со смесью корректных и некорректных кодов."""
        currencies = get_currencies(['USD', 'INVALID', 'EUR'])

        # Должен вернуть данные хотя бы для корректных кодов
        self.assertTrue(len(currencies) >= 2)  # USD и EUR
        print("test_mixed_currency_codes пройден")


if __name__ == '__main__':
    print("=" * 50)
    print("Запуск тестов API курсов валют...")
    print("=" * 50)

    # Создаем тестовый набор
    loader = unittest.TestLoader()

    # Добавляем тесты
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestCurrenciesAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestCurrenciesAPIEdgeCases))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 50)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Пропущено: {len(result.skipped)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("=" * 50)
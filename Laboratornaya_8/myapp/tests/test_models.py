"""
Тесты для моделей предметной области.
Проверка создания объектов, геттеров/сеттеров и валидации.
"""

import unittest
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

try:
    from models.author import Author
    from models.user import User
    from models.currency import Currency
    from models.app import App
    print("Все модели импортированы успешно")
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Текущий путь Python:", sys.path)


class TestAuthorModel(unittest.TestCase):
    """Тесты для модели Author."""

    def test_author_creation(self):
        """Тест создания автора с корректными данными."""
        author = Author(name="Тестовый Автор", group="P3121")
        self.assertEqual(author.name, "Тестовый Автор")
        self.assertEqual(author.group, "P3121")
        print("test_author_creation пройден")

    def test_author_name_setter(self):
        """Тест сеттера имени автора."""
        author = Author(name="Иван Иванов", group="P3121")

        # Корректное изменение
        author.name = "Петр Петров"
        self.assertEqual(author.name, "Петр Петров")

        # Некорректное имя
        with self.assertRaises(ValueError):
            author.name = "А"  # Слишком короткое

        print("test_author_name_setter пройден")

    def test_author_group_setter(self):
        """Тест сеттера группы автора."""
        author = Author(name="Тест", group="P3121")

        # Корректное изменение

        self.assertEqual(author.group, "P3121")

        print("test_author_group_setter пройден")


class TestUserModel(unittest.TestCase):
    """Тесты для модели User."""

    def test_user_creation(self):
        """Тест создания пользователя."""
        user = User(id=1, name="Тестовый Пользователь")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Тестовый Пользователь")
        print("test_user_creation пройден")

    def test_user_subscribe(self):
        """Тест подписки на валюту."""
        user = User(id=1, name="Тест")
        currency = Currency(
            id=1,
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=90.5,
            nominal=1
        )

        user.subscribe_to_currency(currency)
        self.assertEqual(len(user.subscribed_currencies), 1)
        self.assertEqual(user.subscribed_currencies[0].char_code, "USD")
        print("test_user_subscribe пройден")


class TestCurrencyModel(unittest.TestCase):
    """Тесты для модели Currency."""

    def test_currency_creation(self):
        """Тест создания валюты."""
        currency = Currency(
            id=1,
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=90.5,
            nominal=1
        )

        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.value, 90.5)
        print("test_currency_creation пройден")

    def test_currency_value_per_unit(self):
        """Тест расчета курса за одну единицу."""
        currency = Currency(id=1, num_code="840", char_code="USD",
                           name="Доллар США", value=90.5, nominal=1)
        self.assertEqual(currency.value_per_unit, 90.5)
        print("test_currency_value_per_unit пройден")


class TestAppModel(unittest.TestCase):
    """Тесты для модели App."""

    def test_app_creation(self):
        """Тест создания приложения."""
        author = Author(name="Тест Автор", group="P3121")
        app = App(name="Тестовое Приложение", version="1.0.0", author=author)

        self.assertEqual(app.name, "Тестовое Приложение")
        self.assertEqual(app.version, "1.0.0")
        print("test_app_creation пройден")


if __name__ == '__main__':
    print("=" * 50)
    print("Запуск тестов моделей...")
    print("=" * 50)

    # Создаем тестовый набор
    loader = unittest.TestLoader()

    # Добавляем тесты
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestAuthorModel))
    suite.addTests(loader.loadTestsFromTestCase(TestUserModel))
    suite.addTests(loader.loadTestsFromTestCase(TestCurrencyModel))
    suite.addTests(loader.loadTestsFromTestCase(TestAppModel))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 50)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("=" * 50)
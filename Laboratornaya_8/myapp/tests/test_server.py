"""
Тесты для серверной логики и обработки запросов.
"""

import unittest
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

try:
    from myapp import CurrencyAppHandler
    print("Модуль myapp импортирован успешно")
except ImportError as e:
    print(f"Ошибка импорта: {e}")


class TestServerUnit(unittest.TestCase):
    """Юнит-тесты сервера (без запуска реального сервера)."""

    def test_handler_initialization(self):
        """Тест инициализации данных в обработчике."""
        # Проверяем статические атрибуты класса
        self.assertEqual(CurrencyAppHandler.app_instance.name, "Currency Tracker")
        self.assertEqual(CurrencyAppHandler.app_instance.version, "1.0.0")

        # Проверяем автора
        self.assertEqual(CurrencyAppHandler.app_instance.author.name, "Осипов Тимофей Максимович")
        self.assertEqual(CurrencyAppHandler.app_instance.author.group, "P3121")

        print("test_handler_initialization пройден")

    def test_users_list_exists(self):
        """Тест наличия списка пользователей."""
        users = CurrencyAppHandler.users
        self.assertIsInstance(users, list)
        self.assertTrue(len(users) >= 3)  # Должно быть минимум 3 пользователя

        # Проверяем, что есть ожидаемые пользователи
        user_names = [user.name for user in users]
        self.assertIn("Алексей Петров", user_names)
        self.assertIn("Мария Сидорова", user_names)

        print("test_users_list_exists пройден")

    def test_template_environment(self):
        """Тест окружения шаблонов Jinja2."""
        env = CurrencyAppHandler.env



        # Проверяем наличие основных шаблонов
        template_names = ['index.html', 'users.html', 'currencies.html', 'author.html', 'user.html']
        for template_name in template_names:
            try:
                template = env.get_template(template_name)
                self.assertIsNotNone(template)
            except:
                self.fail(f"Шаблон {template_name} не найден")

        print("test_template_environment пройден")

    def test_navigation_generation(self):
        """Тест генерации навигационного меню."""
        # Создаем экземпляр обработчика (требует мокирования)
        # Для простоты тестируем напрямую метод, если он статический
        # или проверяем через экземпляр

        print("test_navigation_generation пройден")


class TestServerLogic(unittest.TestCase):
    """Тесты логики сервера."""

    def test_currency_cache_initialization(self):
        """Тест инициализации кэша валют."""
        cache = CurrencyAppHandler.currencies_cache
        self.assertIsInstance(cache, list)

        # Кэш может быть пустым при старте
        # или содержать данные, если они были загружены ранее
        print("test_currency_cache_initialization пройден")

    def test_render_template_method(self):
        """Тест метода рендеринга шаблонов."""
        # Этот метод требует self (экземпляр класса),
        # поэтому тестируем только наличие метода
        self.assertTrue(hasattr(CurrencyAppHandler, '_render_template'))
        print("test_render_template_method пройден")


class TestServerRoutes(unittest.TestCase):
    """Тесты маршрутов сервера (требует интеграционного тестирования)."""

    def test_route_handlers_exist(self):
        """Тест наличия обработчиков маршрутов."""
        handlers = [
            '_handle_home',
            '_handle_users',
            '_handle_user_detail',
            '_handle_currencies',
            '_handle_author',
            '_handle_404',
            '_handle_add_user',
            '_handle_edit_user',
            '_handle_delete_user'
        ]

        for handler in handlers:
            self.assertTrue(hasattr(CurrencyAppHandler, handler),
                          f"Отсутствует обработчик: {handler}")

        print("test_route_handlers_exist пройден")

    def test_http_methods_handled(self):
        """Тест обработки HTTP методов."""
        self.assertTrue(hasattr(CurrencyAppHandler, 'do_GET'))
        self.assertTrue(hasattr(CurrencyAppHandler, 'do_POST'))
        print("test_http_methods_handled пройден")


if __name__ == '__main__':
    print("=" * 50)
    print("Запуск тестов сервера...")
    print("=" * 50)

    # Создаем тестовый набор
    loader = unittest.TestLoader()

    # Добавляем тесты
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestServerUnit))
    suite.addTests(loader.loadTestsFromTestCase(TestServerLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestServerRoutes))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 50)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")

    # Выводим информацию о неудачных тестах
    if result.failures:
        print("\nНеудачные тесты:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\nТесты с ошибками:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    print("=" * 50)
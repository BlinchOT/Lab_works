"""Основной файл приложения - сервер и маршрутизация."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict, List, Optional

from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies


class CurrencyAppHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов для приложения валют."""

    # Общие данные для приложения
    app_instance = App(
        name="Currency Tracker",
        version="1.0.0",
        author=Author(name="Осипов Тимофей Максимович", group="P3121")
    )

    # Пример данных (в реальном приложении будут из БД)
    users = [
        User(id=1, name="Алексей Петров"),
        User(id=2, name="Мария Сидорова"),
        User(id=3, name="Дмитрий Козлов")
    ]

    # Кэш валют
    currencies_cache: List[Currency] = []

    # Инициализация Jinja2
    env = Environment(
        loader=PackageLoader("myapp"),
        autoescape=select_autoescape()
    )

    def do_POST(self):
        """Обработка POST-запросов."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        print(f"POST запрос на: {path}")

        if path == '/users':
            self._handle_add_user()
        elif path == '/edit-user':
            self._handle_edit_user()
        elif path == '/delete-user':
            self._handle_delete_user()
        else:
            self._send_error_response(405, "Метод не поддерживается")

    def _handle_add_user(self):
        """Обработка добавления пользователя."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            user_name = params.get('name', [''])[0].strip()

            if not user_name or len(user_name) < 2:
                template = self.env.get_template('users.html')
                html = template.render(
                    myapp=self.app_instance,
                    author=self.app_instance.author,
                    users=self.users,
                    error_message="Имя пользователя должно содержать минимум 2 символа",
                    title='Пользователи'
                )
                self._send_html_response(html)
                return

            if any(user.name == user_name for user in self.users):
                template = self.env.get_template('users.html')
                html = template.render(
                    myapp=self.app_instance,
                    author=self.app_instance.author,
                    users=self.users,
                    error_message=f"Пользователь '{user_name}' уже существует",
                    title='Пользователи'
                )
                self._send_html_response(html)
                return

            new_id = max([u.id for u in self.users]) + 1 if self.users else 1
            new_user = User(id=new_id, name=user_name)
            self.users.append(new_user)

            print(f"Добавлен пользователь: {user_name} (ID: {new_id})")

            template = self.env.get_template('users.html')
            html = template.render(
                myapp=self.app_instance,
                author=self.app_instance.author,
                users=self.users,
                success_message=f"Пользователь '{user_name}' успешно добавлен",
                title='Пользователи'
            )
            self._send_html_response(html)

        except Exception as e:
            print(f"Ошибка: {e}")
            self._send_error_response(500, f"Ошибка: {str(e)}")

    def _handle_edit_user(self):
        """Обработка редактирования пользователя."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            user_id = int(params.get('user_id', [0])[0])
            new_name = params.get('name', [''])[0].strip()

            if not new_name or len(new_name) < 2:
                template = self.env.get_template('users.html')
                html = template.render(
                    myapp=self.app_instance,
                    author=self.app_instance.author,
                    users=self.users,
                    error_message="Имя пользователя должно содержать минимум 2 символа",
                    title='Пользователи'
                )
                self._send_html_response(html)
                return

            user = next((u for u in self.users if u.id == user_id), None)
            if not user:
                template = self.env.get_template('users.html')
                html = template.render(
                    myapp=self.app_instance,
                    author=self.app_instance.author,
                    users=self.users,
                    error_message="Пользователь не найден",
                    title='Пользователи'
                )
                self._send_html_response(html)
                return

            if any(u.id != user_id and u.name == new_name for u in self.users):
                template = self.env.get_template('users.html')
                html = template.render(
                    myapp=self.app_instance,
                    author=self.app_instance.author,
                    users=self.users,
                    error_message=f"Пользователь '{new_name}' уже существует",
                    title='Пользователи'
                )
                self._send_html_response(html)
                return

            old_name = user.name
            user.name = new_name

            print(f"Пользователь изменен: {old_name} -> {new_name}")

            template = self.env.get_template('users.html')
            html = template.render(
                myapp=self.app_instance,
                author=self.app_instance.author,
                users=self.users,
                success_message=f"Пользователь '{old_name}' изменен на '{new_name}'",
                title='Пользователи'
            )
            self._send_html_response(html)

        except Exception as e:
            print(f"Ошибка: {e}")
            self._send_error_response(500, f"Ошибка: {str(e)}")

    def _handle_delete_user(self):
        """Обработка удаления пользователя."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            user_id = int(params.get('user_id', [0])[0])

            user_to_delete = next((u for u in self.users if u.id == user_id), None)
            if not user_to_delete:
                template = self.env.get_template('users.html')
                html = template.render(
                    myapp=self.app_instance,
                    author=self.app_instance.author,
                    users=self.users,
                    error_message="Пользователь не найден",
                    title='Пользователи'
                )
                self._send_html_response(html)
                return

            user_name = user_to_delete.name
            self.users = [u for u in self.users if u.id != user_id]

            print(f"Пользователь удален: {user_name}")

            template = self.env.get_template('users.html')
            html = template.render(
                myapp=self.app_instance,
                author=self.app_instance.author,
                users=self.users,
                success_message=f"Пользователь '{user_name}' удален",
                title='Пользователи'
            )
            self._send_html_response(html)

        except Exception as e:
            print(f"Ошибка: {e}")
            self._send_error_response(500, f"Ошибка: {str(e)}")

    def _get_navigation(self) -> List[Dict[str, str]]:
        """Получить меню навигации."""
        return [
            {'caption': 'Главная', 'href': '/'},
            {'caption': 'Пользователи', 'href': '/users'},
            {'caption': 'Валюты', 'href': '/currencies'},
            {'caption': 'Об авторе', 'href': '/author'}
        ]

    def _render_template(self, template_name: str, **context) -> str:
        """Рендерить шаблон с контекстом."""
        template = self.env.get_template(template_name)
        base_context = {
            'myapp': self.app_instance,
            'navigation': self._get_navigation(),
            'author': self.app_instance.author
        }
        base_context.update(context)
        return template.render(**base_context)

    def do_GET(self):
        """Обработка GET-запросов."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # Маршрутизация
        if path == '/':
            self._handle_home()
        elif path == '/users':
            self._handle_users()
        elif path == '/user':
            self._handle_user_detail(query_params)
        elif path == '/currencies':
            self._handle_currencies()
        elif path == '/author':
            self._handle_author()
        elif path.startswith('/static/'):
            self._handle_static()
        else:
            self._handle_404()

    def _handle_home(self):
        """Обработка главной страницы."""
        # Добавьте этот код перед рендерингом
        from datetime import datetime

        html_content = self._render_template(
            'index.html',
            title='Главная страница',
            welcome_message='Добро пожаловать в приложение для отслеживания валют!',
            users=self.users,  # Добавляем пользователей
            currencies=self.currencies_cache,  # Добавляем валюты
            last_updated=self._get_current_time(),  # Время обновления
            now=datetime.now()  # Текущее время для футера
        )
        self._send_html_response(html_content)

    def _handle_users(self):
        """Обработка страницы пользователей."""
        html_content = self._render_template(
            'users.html',
            title='Пользователи',
            users=self.users
        )
        self._send_html_response(html_content)

    def _handle_user_detail(self, query_params: Dict):
        """Обработка страницы конкретного пользователя."""
        user_id = int(query_params.get('id', [1])[0])
        user = next((u for u in self.users if u.id == user_id), None)

        if not user:
            self._send_error_response(404, "Пользователь не найден")
            return

        # Получаем валюты для пользователя (пример)
        user_currencies = self._get_user_currencies(user.id)

        html_content = self._render_template(
            'user.html',
            title=f'Пользователь: {user.name}',
            user=user,
            currencies=user_currencies
        )
        self._send_html_response(html_content)

    def _handle_currencies(self):
        """Обработка страницы валют."""
        try:
            # Инициализируем курсы, если они пустые
            if not self.currencies_cache:
                self._update_currencies()

            html_content = self._render_template(
                'currencies.html',
                title='Курсы валют',
                currencies=self.currencies_cache,
                last_updated=self._get_current_time()
            )
            self._send_html_response(html_content)
        except Exception as e:
            # Даже если ошибка, покажем страницу с сообщением
            html_content = f"""
            <html>
            <body>
                <h1>Ошибка загрузки курсов валют</h1>
                <p>{str(e)}</p>
                <a href="/">На главную</a>
            </body>
            </html>
            """
            self._send_html_response(html_content)

    def _handle_author(self):
        """Обработка страницы об авторе."""
        html_content = self._render_template(
            'author.html',
            title='Об авторе'
        )
        self._send_html_response(html_content)

    def _handle_static(self):
        """Обработка статических файлов."""
        # Реализация для статических файлов
        self._send_error_response(404, "Статические файлы не реализованы")

    def _handle_404(self):
        """Обработка 404 ошибки."""
        html_content = self._render_template(
            '404.html',
            title='Страница не найдена'
        )
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def _update_currencies(self):
        """Обновить кэш курсов валют."""
        try:
            # Получаем курсы через API
            currencies_data = get_currencies(['USD', 'EUR', 'GBP', 'CNY', 'JPY'])

            # Преобразуем в объекты Currency
            self.currencies_cache = []
            for idx, (code, data) in enumerate(currencies_data.items()):
                currency = Currency(
                    id=idx + 1,
                    num_code=data.get('num_code', '000'),
                    char_code=code,
                    name=data.get('name', code),
                    value=float(data.get('value', 0).replace(',', '.')),
                    nominal=int(data.get('nominal', 1))
                )
                self.currencies_cache.append(currency)
        except Exception:
            # Если API не работает, используем примерные данные
            self.currencies_cache = [
                Currency(1, '840', 'USD', 'Доллар США', 90.5, 1),
                Currency(2, '978', 'EUR', 'Евро', 99.8, 1),
                Currency(3, '826', 'GBP', 'Фунт стерлингов', 115.2, 1)
            ]

    def _get_user_currencies(self, user_id: int) -> List[Currency]:
        """Получить валюты пользователя (заглушка)."""
        return self.currencies_cache[:2]  # Пример

    def _get_current_time(self):
        """Получить текущее время (заглушка)."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _send_html_response(self, content: str):
        """Отправить HTML-ответ."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def _send_error_response(self, code: int, message: str):
        """Отправить ответ с ошибкой."""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response = {'error': message, 'code': code}
        self.wfile.write(json.dumps(response).encode('utf-8'))



def run_server():
    """Запустить сервер."""
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, CurrencyAppHandler)

    print(f"Сервер запущен на http://{server_address[0]}:{server_address[1]}")
    print(f"Приложение: {CurrencyAppHandler.app_instance}")
    print("Доступные маршруты:")
    print("  / - Главная страница")
    print("  /users - Список пользователей")
    print("  /user?id=<id> - Информация о пользователе")
    print("  /currencies - Курсы валют")
    print("  /author - Об авторе")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        httpd.server_close()



if __name__ == '__main__':
    run_server()
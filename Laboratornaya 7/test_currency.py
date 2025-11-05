import unittest
import io
import requests

from .currency import get_currencies
from .decorators import trace

# Тесты
MAX_R_VALUE=1000
class TestStreamWrite(unittest.TestCase):
    def test_currency_usd(self):
        """
          Проверяет наличие ключа в словаре и значения этого ключа
        """
        currency_list = ['USD']
        currency_data = get_currencies(currency_list)

        self.assertIn(currency_list[0], currency_data)
        self.assertIsInstance(currency_data['USD'], float)
        self.assertGreaterEqual(currency_data['USD'], 0)
        self.assertLessEqual(currency_data['USD'], MAX_R_VALUE)

    def test_nonexist_code(self):
        self.assertIn("Код валюты", get_currencies(['XYZ'])['XYZ'])
        self.assertIn("XYZ", get_currencies(['XYZ'])['XYZ'])
        self.assertIn("не найден", get_currencies(['XYZ'])['XYZ'])

    def test_get_currency_error(self):
        error_phrase_regex = "Ошибка при запросе к API"
        with self.assertRaises(requests.exceptions.RequestException):
            currency_data = get_currencies(currency_codes=['USD'], url="https://")

    def TestStreamWrite(self):
        super()
        self.raisedCounting = 0

    def setUp(self):
        self.nonstandardstream = io.StringIO()
        self.trace = trace(get_currencies, handle=self.nonstandardstream)

    def test_writing_stream(self):
        decorated_func = trace(get_currencies, handle=self.nonstandardstream)
        decorated_func(['USD'], url="https://")

    def tearDown(self):
        del self.nonstandardstream
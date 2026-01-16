"""
Декоратор для логирования с параметрами.
Поддерживает разные типы обработчиков: sys.stdout, io.StringIO, logging.Logger.
"""

import functools
import sys
import logging
from typing import Callable, Any, Optional, Union
import io


def logger(
        func: Optional[Callable] = None,
        *,
        handle: Union[io.IOBase, logging.Logger] = sys.stdout
) -> Callable:
    """
    Параметризованный декоратор для логирования вызовов функций.

    Args:
        func: Декорируемая функция (None при использовании с параметрами)
        handle: Объект для логирования. Может быть:
            - sys.stdout или io.StringIO (использует .write())
            - logging.Logger (использует .info(), .error())

    Returns:
        Декорированную функцию с логированием.

    Примеры использования:
        @logger
        def f(): ...

        @logger(handle=sys.stderr)
        def f(): ...

        @logger(handle=io.StringIO())
        def f(): ...

        @logger(handle=logging.getLogger("my_logger"))
        def f(): ...
    """

    def decorator(inner_func: Callable) -> Callable:
        @functools.wraps(inner_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем строку с аргументами
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            # Логирование начала вызова
            start_message = f"Вызов функции {inner_func.__name__}({signature})"

            # Определяем тип обработчика и логируем соответствующим образом
            if isinstance(handle, logging.Logger):
                # Логирование через logging.Logger
                handle.info(f"START: {start_message}")
            else:
                # Логирование через метод write()
                handle.write(f"INFO: {start_message}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()

            try:
                # Выполняем функцию
                result = inner_func(*args, **kwargs)

                # Логирование успешного завершения
                success_message = f"Функция {inner_func.__name__} завершилась успешно. Результат: {result!r}"

                if isinstance(handle, logging.Logger):
                    handle.info(f"SUCCESS: {success_message}")
                else:
                    handle.write(f"INFO: {success_message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()

                return result

            except Exception as e:
                # Логирование ошибки
                error_message = f"Ошибка в функции {inner_func.__name__}: {type(e).__name__}: {str(e)}"

                if isinstance(handle, logging.Logger):
                    handle.error(f"ERROR: {error_message}")
                else:
                    handle.write(f"ERROR: {error_message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()

                # Повторно выбрасываем исключение
                raise

        return wrapper

    # Обработка вызова декоратора с параметрами и без
    if func is None:
        # Вызвано как @logger(handle=...)
        return decorator
    else:
        # Вызвано как @logger
        return decorator(func)


# Для совместимости с существующим кодом
def trace(
        func: Optional[Callable] = None,
        *,
        handle: Union[io.IOBase, logging.Logger] = sys.stdout
) -> Callable:
    """Альтернативное имя для декоратора logger (совместимость с примерами)."""
    return logger(func, handle=handle)


if __name__ == "__main__":
    # Демонстрация работы декоратора
    import io

    print("=== Демонстрация декоратора logger/trace ===")


    # Пример 1: Логирование в stdout
    @logger
    def add(a: int, b: int) -> int:
        """Сложение двух чисел."""
        return a + b


    print("1. Логирование в stdout:")
    result = add(5, 3)
    print(f"Результат: {result}")
    print()

    # Пример 2: Логирование в StringIO
    stream = io.StringIO()


    @logger(handle=stream)
    def multiply(x: int, y: int) -> int:
        """Умножение двух чисел."""
        return x * y


    print("2. Логирование в StringIO:")
    multiply(4, 5)
    print("Логи из StringIO:")
    print(stream.getvalue())
    print()

    # Пример 3: Логирование через logging
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("demo")


    @logger(handle=log)
    def divide(a: int, b: int) -> float:
        """Деление двух чисел."""
        return a / b


    print("3. Логирование через logging (проверьте вывод):")
    try:
        divide(10, 2)
        divide(10, 0)  # Вызовет ошибку
    except ZeroDivisionError:
        print("Поймано исключение ZeroDivisionError")
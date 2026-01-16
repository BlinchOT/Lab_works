"""
Демонстрационная функция для решения квадратного уравнения.
Используется для демонстрации работы декоратора logger.
"""

import math
from typing import Optional, Tuple, Union


def solve_quadratic(
        a: Union[int, float],
        b: Union[int, float],
        c: Union[int, float]
) -> Optional[Union[float, Tuple[float, float]]]:
    """
    Решает квадратное уравнение вида ax² + bx + c = 0.

    Args:
        a: Коэффициент при x²
        b: Коэффициент при x
        c: Свободный член

    Returns:
        - None: если дискриминант < 0 (нет действительных корней)
        - float: если один корень (дискриминант = 0)
        - Tuple[float, float]: если два корня (дискриминант > 0)

    Raises:
        TypeError: если коэффициенты не числовые
        ValueError: если a = 0 (уравнение не квадратное)
    """
    # Валидация типов аргументов
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Коэффициент '{name}' должен быть числом, получено: {type(value).__name__}")

    # Проверка, что уравнение квадратное
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть равен 0 (уравнение не квадратное)")

    # Вычисление дискриминанта
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        # Нет действительных корней
        return None
    elif discriminant == 0:
        # Один корень
        root = -b / (2 * a)
        return root
    else:
        # Два корня
        sqrt_discriminant = math.sqrt(discriminant)
        root1 = (-b + sqrt_discriminant) / (2 * a)
        root2 = (-b - sqrt_discriminant) / (2 * a)
        return root1, root2


if __name__ == "__main__":
    # Демонстрация
    print("=== Демонстрация решения квадратных уравнений ===")

    test_cases = [
        (1, -5, 6),  # два корня
        (1, -4, 4),  # один корень
        (1, 2, 5),  # нет корней
        (0, 2, 3),  # a = 0
    ]

    for a, b, c in test_cases:
        print(f"\nУравнение: {a}x² + {b}x + {c} = 0")
        try:
            result = solve_quadratic(a, b, c)
            print(f"  Результат: {result}")
        except Exception as e:
            print(f"  Ошибка: {type(e).__name__}: {e}")
import timeit
import matplotlib.pyplot as plt
from typing import Callable
from functools import lru_cache

def factorial(n: int) -> int:
    """
    Факториал натурального числа через цикл
    """
    fct = 1
    while n > 1:
        fct *= n
        n -= 1
    return fct

def factorial_rec(n: int) -> int:
    """
    Факториал натурального числа через рекурсию
    """
    if n > 1:
        return n * factorial_rec(n - 1)
    return 1

@lru_cache(maxsize=1024)
def factorial_cached(n: int) -> int:
    fct = 1
    while n > 1:
        fct *= n
        n -= 1
    return fct

@lru_cache(maxsize=1024)
def factorial_rec_cached(n: int) -> int:
    if n > 1:
        return n * factorial_rec_cached(n - 1)
    return 1

def benchmark(func: Callable[[int], int], params: list[int], repeat: int = 5) -> list[float]:
    """
    Сравнение времени работ функций
    :param func: функция типа Callable[[int], int] для тестирования
    :param params: параметры функции, для которых проводится тестирование
        каждое число - очередной единственный параметр функции
    :param repeat: количество повторений работы функции на очередном числе
        время работы функции на числе n вычисляется как [t_1, t_2, ... t_repeat] / repeat,
        где t_j - очередное время работы на числе n
    """
    len_params = len(params)
    times = [0] * len_params
    for _ in range(repeat):
        for i in range(len_params):
            times[i] += timeit.repeat(lambda: func(params[i]), number=1, repeat=1)[0]
        if hasattr(func, 'cache_clear'):  # для 'честного' измерения времени работы при кэшировании
            func.cache_clear()
    return [(times[i] / repeat) * 1_000_000 for i in range(len_params)]

def make_subplot(x_params, y_params, ax, title, x_label, y_label, *labels):
    ax.ticklabel_format(style='plain', axis='both')
    ax.set_title(title, fontsize=11)
    ax.plot(x_params[0], y_params[0], label=labels[0], marker='o', linestyle='-')
    ax.plot(x_params[1], y_params[1], label=labels[1], marker='o', linestyle='-')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)
    ax.legend()

if __name__ == "__main__":
    nums = list(range(0, 350, 25))
    repeat = 25
    fact_times = benchmark(factorial, nums, repeat)
    rec_times = benchmark(factorial_rec, nums, repeat)
    fact_cached_times = benchmark(factorial_cached, nums, repeat)
    rec_cached_times = benchmark(factorial_rec_cached, nums, repeat)

    plt.style.use('Solarize_Light2')
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    fig.suptitle('Factorial computations comparison')

    x_params = (nums, nums)
    make_subplot(x_params, (fact_times, rec_times), axes[0, 0],
                 '1.1 factorial computation',
                 'num', 'time, μs',
                 'loop', 'recursion')
    make_subplot(x_params, (fact_cached_times, rec_cached_times), axes[0, 1],
                 '1.2 cached factorial computation',
                 'num','time, μs',
                 'loop', 'recursion')
    make_subplot(x_params, (rec_times, rec_cached_times), axes[1, 0],
                 '1.3 factorial via recursion',
                 'num', 'time, μs',
                 'non-cached', 'cached')
    make_subplot(x_params, (fact_times, fact_cached_times), axes[1, 1],
                 '1.4 factorial via loop',
                 'num', 'time, μs',
                 'non-cached', 'cached')
    plt.tight_layout()
    plt.show()
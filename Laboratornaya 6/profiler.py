import timeit
from typing import Callable
import matplotlib.pyplot as plt
from gen_bin_tree3 import gen_bin_tree as rec_bin_tree # файл с 3 лабораторной работы
from gen_bin_tree5 import gen_bin_tree as loop_bin_tree # файл с 5 лабораторной работы

def benchmark(func: Callable, params: list[int], repeat: int = 5) -> list[float]:
    times = []
    for n in params:
        curr_times = timeit.repeat(lambda: func(n), number=1, repeat=repeat)
        times.append(sum(curr_times) / repeat)
    return times

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


    heights = list(range(23))
    repeat = 1
    gen_bin_tree_custom_rec = lambda h: rec_bin_tree(
        {}, h, node=1,
        left_node_value=lambda x: x + x, right_node_value=lambda x: 2 * x)
    gen_bin_tree_custom_loop = lambda h: loop_bin_tree(
        h, root=1,
        left_node_value=lambda x: x + x, right_node_value=lambda x: 2 * x + 1)
    bin_tree_times = benchmark(gen_bin_tree_custom_loop, heights, repeat)
    bin_tree_rec_times = benchmark(gen_bin_tree_custom_rec, heights, repeat)

    plt.style.use('Solarize_Light2')
    fig, axes = plt.subplots(1, 1, figsize=(6, 6))
    fig.suptitle('Binary tree constructions comparison')
    x_params = (heights, heights)
    make_subplot(x_params, (bin_tree_times, bin_tree_rec_times), axes,
                 '',
                 'height', 'time, sec',
                 'loop', 'recursion')
    plt.tight_layout()
    plt.show()


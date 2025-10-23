from collections import deque
from typing import TypeAlias, Callable

def get_left_node_value(node: int) -> int: # Левый узел
    return node * 3 + 1

def get_right_node_value(node: int) -> int: # Правый узел
    return node * 3 + 1

binTree: TypeAlias = dict[int, list['binTree'] | list]
intToInt: TypeAlias = Callable[[int], int]
def gen_bin_tree(height: int = 5, root: int = 10,
                 left_node_value: intToInt = get_left_node_value,
                 right_node_value: intToInt = get_right_node_value) -> binTree:
    """
    Функция бинарного дерева
    :param height: высота дерева
    :param root: значение корня дерева
    :param left_node_value: функция значения левого потомка узла
    :param right_node_value: функция значения правого потомка узла
    :return: дерево типа binTree
    """
    if height == 0:
        return {root: []}
    tree = {}
    sub_trees = deque()
    sub_trees.append((tree, root, 0))
    while sub_trees:
        sub_tree, parent, height_curr = sub_trees.popleft()
        if height_curr >= height:
            continue
        left_node = left_node_value(parent)
        right_node = right_node_value(parent)
        sub_tree[parent] = [{left_node: []}, {right_node: []}]
        sub_trees.append((sub_tree[parent][0], left_node, height_curr + 1))
        sub_trees.append((sub_tree[parent][1], right_node, height_curr + 1))
    return tree



from typing import TypeAlias, Callable

def get_left_node_value(node: int) -> int: # Левый узел
    return node * 3 + 1

def get_right_node_value(node: int) -> int: # Правый узел
    return node * 3 - 1

binTree: TypeAlias = dict[int, list['binTree'] | list]
intToInt: TypeAlias = Callable[[int], int]
def gen_bin_tree(tree: binTree, height: int = 4, node: int = 12,
                 left_node_value: intToInt = get_left_node_value,
                 right_node_value: intToInt = get_right_node_value) -> None:
    """
    Функция бинарного дерева
    :param tree: поддерево текущей итерации
    :param height: высота дерева
    :param node: значение родителя поддерева
    :param left_node_value: функция значения левого потомка узла
    :param right_node_value: функция значения правого потомка узла
    :return: дерево типа binTree
    """
    if height == 0:
        tree[node] = []
    else:
        left_child, right_child = {}, {}
        gen_bin_tree(left_child, height - 1, left_node_value(node), left_node_value, right_node_value)
        gen_bin_tree(right_child, height - 1, right_node_value(node), left_node_value, right_node_value)
        tree[node] = [left_child, right_child]

def main():
    print(gen_bin_tree(1, 5, 4))

if __name__=="__main__":
    main()

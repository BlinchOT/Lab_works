def left_leaf(root: int) -> int:
    return root * 3 + 1


def right_leaf(root: int) -> int:
    return 3 * root - 1


def gen_bin_tree(height: int, root: int, l_l=left_leaf, l_r=right_leaf):
    if height <= 1:
        return {str(root): []}
    return {str(root): [gen_bin_tree(height - 1, l_l(root), l_l, l_r), gen_bin_tree(height - 1, l_r(root), l_l, l_r)]}


def main():
    print(gen_bin_tree(5, 10))

if __name__=="__main__":
    main()
import unittest
from .bin_tree import left_leaf
from .bin_tree import right_leaf
from .bin_tree import gen_bin_tree
from .bin_tree import main



# Тесты
class TestMath(unittest.TestCase):
    def test_gen_bin_tree(self):
        self.assertEqual(gen_bin_tree(5, 10), {'10': [{'31': [{'94': [{'283': [{'850': []}, {'848': []}]},
                        {'281': [{'844': []}, {'842': []}]}]},
                {'92': [{'277': [{'832': []}, {'830': []}]},
                        {'275': [{'826': []}, {'824': []}]}]}]},
        {'29': [{'88': [{'265': [{'796': []}, {'794': []}]},
                        {'263': [{'790': []}, {'788': []}]}]},
                {'86': [{'259': [{'778': []}, {'776': []}]},
                        {'257': [{'772': []}, {'770': []}]}]}]}]})
    def test_left_leaf(self):
        self.assertEqual(left_leaf(5), 16)

    def test_right_leaf(self):
        self.assertEqual(left_leaf(34), 103)




if __name__=="__main__":

# Запуск тестов
    unittest.main()
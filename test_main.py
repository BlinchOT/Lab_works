import unittest
from main import twoSum



# Тесты
class TestMath(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(twoSum([2,1,5], 3), [0,1])

    def test_add_negative(self):
        self.assertEqual(twoSum([-1,-2,-6], -8), [1,2])

    def test_add_zero(self):
        self.assertEqual(twoSum([0,2,5], 5), [0,2])

    def test_three_ones(self):
        self.assertEqual(twoSum([1,1,1], 2), [0,1])

    def test_zeroes(self):
        self.assertEqual(twoSum([0,0,0], 0), [0,1])

    def test_positive_and_negative(self):
        self.assertEqual(twoSum([5,-6,-5], -1), [0,1])

if __name__=="__main__":

# Запуск тестов
    unittest.main()
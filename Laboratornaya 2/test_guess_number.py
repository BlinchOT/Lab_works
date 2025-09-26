import unittest
from .guess_number import guess_number


# Тесты
class TestMath(unittest.TestCase):

    def test_seq(self):
        self.assertEqual(guess_number(3, [1,2,3,4,5],"seq"),[3,3])

    def test_bin(self):
        self.assertEqual(guess_number(3, [1,2,3,4,5],"bin"),[3,1])

    def test_seq_targetless(self):
        self.assertEqual(guess_number(0, [1,2,9,4,8],"seq"),None)

    def test_bin_targetless(self):
        self.assertEqual(guess_number(100, [101,102,1,4,88],"bin"),None)
        
    def test_negative_seq(self):
        self.assertEqual(guess_number(-5, [-1,-2,-3,-4,-5],"seq"),[-5,1])

    def test_negative_bin(self):
        self.assertEqual(guess_number(-3, [-1,-2,-3,-4,-5,-6],"bin"),[-3,3])
        
    def test_negative_seq_targetless(self):
        self.assertEqual(guess_number(0, [-1,-2,-100,-96,-5],"seq"),None)

    def test_negative_bin_targetless(self):
        self.assertEqual(guess_number(0, [-10000,-1,-11,-111,-1111],"bin"),None)



# Запуск тестов
if __name__=="__main__":
    unittest.main()
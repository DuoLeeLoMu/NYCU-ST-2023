import unittest
from calculator import Calculator

class ApplicationTest(unittest.TestCase):
    
    def test_add(self):
        param_list = [(1, 2, 3), (2, 3, 5), (3, 4, 7), (4, 5, 9), (5, 6, 11)]
        exception_case = (1, "1")
        for p1, p2, p3 in param_list:
            with self.subTest():
                self.assertEqual(p3, Calculator.add(p1, p2))

        self.assertRaises(TypeError, Calculator.add, exception_case[0], exception_case[1])

    def test_divide(self):
        param_list = [(2, 1, 2), (4, 2, 2), (15, 5, 3), (56, 7, 8), (77, 7, 11)]
        exception_case = (1, 0)
        for p1, p2, p3 in param_list:
            with self.subTest():
                self.assertEqual(p3, Calculator.divide(p1, p2))

        self.assertRaises(ZeroDivisionError, Calculator.divide, exception_case[0], exception_case[1])

    def test_sqrt(self):
        param_list = [(4, 2), (9, 3), (16, 4), (25, 5), (100, 10)]
        exception_case = -1
        for p1, p2 in param_list:
            with self.subTest():
                self.assertEqual(p2, Calculator.sqrt(p1))

        self.assertRaises(ValueError, Calculator.sqrt, exception_case)

    def test_exp(self):
        param_list = [(0, 1), (1, 2.718281828459045), (2, 7.38905609893065),
                       (3, 20.085536923187668), (4, 54.598150033144236)]
        exception_case = 1000
        for p1, p2 in param_list:
            with self.subTest():
                self.assertEqual(p2, Calculator.exp(p1))

        self.assertRaises(OverflowError, Calculator.exp, exception_case)

if __name__ == '__main__':
    unittest.main()
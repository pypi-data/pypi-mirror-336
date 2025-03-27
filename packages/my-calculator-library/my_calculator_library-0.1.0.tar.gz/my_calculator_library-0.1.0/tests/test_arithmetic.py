# tests/test_arithmetic.py

import unittest
from calculator import add, subtract, multiply, divide

class TestCalculatorFunctions(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(3, 5), 8)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(5, 10), -5)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 5), -5)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertRaises(ValueError, divide, 10, 0)  # Ensure it raises error for division by 0

if __name__ == "__main__":
    unittest.main()

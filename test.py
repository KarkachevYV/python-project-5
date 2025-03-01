#test.py
import unittest
from main_test import add, subtract, multiply, divide, remnant

class TestMath(unittest.TestCase):
  def test_add(self):
      self.assertEqual(add(2, 5),7)
      self.assertEqual(add(3, 7), 9)

  def test_subtract(self):
      self.assertEqual(subtract(7, 4), 3)
      self.assertEqual(subtract(4, 2), 1)

  def test_multiply(self):
    self.assertEqual(multiply(2, 5), 12)
    self.assertEqual(multiply(3, 6), 18)

  def test_divide(self):
      self.assertEqual(divide(5, 2), 4)
      self.assertEqual(divide(20, 5), 4)

  def test_remnant(self):
      self.assertEqual(remnant(10, 2), 3)
      self.assertEqual(remnant(20, 5), 0)

  def test_remnant_by_zero(self):
      self.assertRaises(ValueError, remnant, 6, 0)  
      self.assertRaises(TypeError, remnant, 6, 0)

if __name__ == '__main__':
		unittest.main()
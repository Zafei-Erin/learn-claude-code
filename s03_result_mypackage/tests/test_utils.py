"""
Tests for mypackage.utils module.
"""

import unittest
from mypackage.utils import greet, add_numbers, capitalize_words, reverse_string


class TestGreet(unittest.TestCase):
    """Test cases for the greet function."""
    
    def test_greet_basic(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")
    
    def test_greet_empty_string(self):
        self.assertEqual(greet(""), "Hello, !")
    
    def test_greet_with_numbers(self):
        self.assertEqual(greet("123"), "Hello, 123!")


class TestAddNumbers(unittest.TestCase):
    """Test cases for the add_numbers function."""
    
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(3, 5), 8)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-3, -5), -8)
    
    def test_add_mixed_numbers(self):
        self.assertEqual(add_numbers(-3, 5), 2)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(3.5, 2.1), 5.6)
    
    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 5), 5)


class TestCapitalizeWords(unittest.TestCase):
    """Test cases for the capitalize_words function."""
    
    def test_capitalize_single_word(self):
        self.assertEqual(capitalize_words("hello"), "Hello")
    
    def test_capitalize_multiple_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")
    
    def test_capitalize_mixed_case(self):
        self.assertEqual(capitalize_words("hELLo wORLd"), "Hello World")
    
    def test_capitalize_empty_string(self):
        self.assertEqual(capitalize_words(""), "")
    
    def test_capitalize_with_extra_spaces(self):
        self.assertEqual(capitalize_words("hello   world"), "Hello World")


class TestReverseString(unittest.TestCase):
    """Test cases for the reverse_string function."""
    
    def test_reverse_basic(self):
        self.assertEqual(reverse_string("hello"), "olleh")
    
    def test_reverse_empty_string(self):
        self.assertEqual(reverse_string(""), "")
    
    def test_reverse_single_char(self):
        self.assertEqual(reverse_string("a"), "a")
    
    def test_reverse_with_spaces(self):
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")


if __name__ == "__main__":
    unittest.main()

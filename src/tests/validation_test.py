import unittest
from util import validate_reference

class TestValidateReference(unittest.TestCase):

    def test_valid_input(self):
        # should not raise
        try:
            validate_reference("key1", "Title", 2020, "Publisher")
        except ValueError:
            self.fail("validate_reference raised ValueError unexpectedly!")

    def test_missing_cite_key(self):
        with self.assertRaises(ValueError) as context:
            validate_reference("", "Title", 2020, "Publisher")
        self.assertEqual(str(context.exception), "Cite key is required")

    def test_missing_title(self):
        with self.assertRaises(ValueError) as context:
            validate_reference("key1", "", 2020, "Publisher")
        self.assertEqual(str(context.exception), "Title is required")

    def test_invalid_year(self):
        with self.assertRaises(ValueError) as context:
            validate_reference("key1", "Title", "abcd", "Publisher")
        self.assertEqual(str(context.exception), "Year must be a valid number")

    def test_missing_publisher(self):
        with self.assertRaises(ValueError) as context:
            validate_reference("key1", "Title", 2020, "")
        self.assertEqual(str(context.exception), "Publisher is required")


if __name__ == "__main__":
    unittest.main()

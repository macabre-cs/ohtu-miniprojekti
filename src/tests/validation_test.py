import unittest
from util import validate_reference

class TestValidateReference(unittest.TestCase):

    def test_valid_input(self):
        # should not raise
        try:
            validate_reference({
                "reference_type": "book",
                "cite_key": "key1",
                "title": "Title",
                "authors_formatted": "Author",
                "year": 2020,
                "publisher": "Publisher",
            })
        except ValueError:
            self.fail("validate_reference raised ValueError unexpectedly!")

    def test_missing_cite_key(self):
        with self.assertRaises(ValueError) as context:
            validate_reference({
                "reference_type": "book",
                "cite_key": "",
                "title": "Title",
                "authors_formatted": "Author",
                "year": 2020,
                "publisher": "Publisher",
            })
        self.assertEqual(str(context.exception), "Cite key is required")

    def test_missing_title(self):
        with self.assertRaises(ValueError) as context:
            validate_reference({
                "reference_type": "book",
                "cite_key": "key1",
                "title": "",
                "authors_formatted": "Author",
                "year": 2020,
                "publisher": "Publisher",
            })
        self.assertEqual(str(context.exception), "Title is required")

    def test_missing_author(self):
        with self.assertRaises(ValueError) as context:
            validate_reference({
                "reference_type": "book",
                "cite_key": "key1",
                "title": "Title",
                "authors_formatted": "",
                "year": 2020,
                "publisher": "Publisher",
            })
        self.assertEqual(str(context.exception), "Author(s) is/are required")

    def test_invalid_year(self):
        with self.assertRaises(ValueError) as context:
            validate_reference({
                "reference_type": "book",
                "cite_key": "key1",
                "title": "Title",
                "authors_formatted": "Author",
                "year": "abcd",
                "publisher": "Publisher",
            })
        self.assertEqual(str(context.exception), "Year must be a valid number")

if __name__ == "__main__":
    unittest.main()

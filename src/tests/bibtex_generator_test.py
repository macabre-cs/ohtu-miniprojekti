import unittest
import bibtexparser
from bibtex_generator import format_authors, generate_bibtex
from entities.reference import Reference

class TestBibtexGenerator(unittest.TestCase):

    def test_format_single_author_with_comma(self):
        result = format_authors("Knuth, Donald")
        self.assertEqual(result, "Donald Knuth")

    def test_format_multiple_authors(self):
        result = format_authors("Knuth, Donald;Lamport, Leslie;Torvalds, Linus")
        self.assertEqual(result, "Donald Knuth and Leslie Lamport and Linus Torvalds")

    def test_bibtex_generation_with_one_reference(self):
        ref_dict = {
            'id': 1,
            'reference_type': 'article',
            'cite_key': 'knuth1984',
            'title': 'Literate Programming',
            'author': 'Knuth, Donald E.',
            'year': '1984',
            'journal': 'The Computer Journal',
            'volume': '27',
            'pages': '97-111'
        }
        reference = Reference(ref_dict)

        bibtex_output = generate_bibtex([reference])

        # Validate with bibtexparser
        bib_database = bibtexparser.loads(bibtex_output)

        # Check that parsing succeeded
        self.assertEqual(len(bib_database.entries), 1)

        # Verify the entry content
        entry = bib_database.entries[0]
        self.assertEqual(entry['ID'], 'knuth1984')
        self.assertEqual(entry['ENTRYTYPE'], 'article')
        self.assertEqual(entry['title'], 'Literate Programming')
        self.assertEqual(entry['author'], 'Donald E. Knuth')
        self.assertEqual(entry['year'], '1984')
        self.assertEqual(entry['journal'], 'The Computer Journal')
        self.assertEqual(entry['volume'], '27')
        self.assertEqual(entry['pages'], '97--111')


if __name__ == '__main__':
    unittest.main()

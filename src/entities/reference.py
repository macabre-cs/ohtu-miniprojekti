# pylint: disable=too-many-instance-attributes

class Reference:
    def __init__(self, reference_dict):
        self.id = reference_dict.get('id')
        self.reference_type = reference_dict.get('reference_type')
        self.cite_key = reference_dict.get('cite_key')
        self.title = reference_dict.get('title')
        self.author = reference_dict.get('authors_formatted') or reference_dict.get('author')
        self.authors_raw = reference_dict.get('authors_raw')
        self.year = reference_dict.get('year')
        if self.reference_type == 'book':
            self.publisher = reference_dict.get('publisher')
            self.chapter = reference_dict.get('chapter')
        elif self.reference_type == 'article':
            self.journal = reference_dict.get('journal')
            self.volume = reference_dict.get('volume')
            self.pages = reference_dict.get('pages')
        elif self.reference_type == 'inproceedings':
            self.booktitle = reference_dict.get('booktitle')

    def __str__(self):
        cite = self.cite_key or ""
        title = self.title or ""
        year = self.year or ""
        author = self.author or ""

        return f"{cite}: {title} ({year}), {author}"

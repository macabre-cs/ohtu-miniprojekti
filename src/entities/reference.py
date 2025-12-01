# pylint: disable=too-many-instance-attributes

class Reference:
    def __init__(self, reference_dict):
        self.id = reference_dict.get('id')
        self.reference_type = reference_dict.get('reference_type')
        self.cite_key = reference_dict.get('cite_key')
        self.title = reference_dict.get('title')
        self.author = reference_dict.get('authors_formatted') or reference_dict.get('author')
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
        elif self.reference_type == 'misc':
            self.url = reference_dict.get('url')

    def __str__(self):
        cite = self.cite_key or ""
        title = self.title or ""
        year = self.year or ""
        author = self.author or ""

        return f"{cite}: {title} ({year}), {author}"

    def __iter__(self):
        result = {
            'id': self.id,
            'reference_type': self.reference_type,
            'cite_key': self.cite_key,
            'title': self.title,
            'author': self.author,
            'year': self.year
        }

        if self.reference_type == 'book':
            result['publisher'] = self.publisher
            result['chapter'] = self.chapter
        elif self.reference_type == 'article':
            result['journal'] = self.journal
            result['volume'] = self.volume
            result['pages'] = self.pages
        elif self.reference_type == 'inproceedings':
            result['booktitle'] = self.booktitle
        elif self.reference_type == 'misc':
            result['url'] = self.url

        return iter(result.items())

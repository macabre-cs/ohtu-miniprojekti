class Reference:
    def __init__(self, reference_dict):
        self.id = reference_dict.get('id')
        self.cite_key = reference_dict.get('cite_key')
        self.title = reference_dict.get('title')
        self.author = reference_dict.get('author')
        self.year = reference_dict.get('year')
        self.publisher = reference_dict.get('publisher')

    def __str__(self):
        return f"{self.cite_key}: {self.title} ({self.year}), {self.author}, {self.publisher}"

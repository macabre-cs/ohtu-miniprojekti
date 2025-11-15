class Reference:
    def __init__(self, reference_id, cite_key, title, year, publisher):
        self.id = reference_id
        self.cite_key = cite_key
        self.title = title
        self.year = year
        self.publisher = publisher

    def __str__(self):
        return f"{self.cite_key}: {self.title} ({self.year}), {self.publisher}"

class Reference:
    def __init__(self, reference_id, content):
        self.id = reference_id
        self.content = content

    def __str__(self):
        return f"{self.content}"

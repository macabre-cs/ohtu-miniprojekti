from config import db
from entities.associations import reference_tags


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationship to references (many-to-many)
    references = db.relationship(
        "Reference",
        secondary=reference_tags,
        back_populates="tags",
        lazy="dynamic"
    )

    def __init__(self, name):
        """
        Initialize Tag with a name.
        """
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"<Tag {self.name}>"

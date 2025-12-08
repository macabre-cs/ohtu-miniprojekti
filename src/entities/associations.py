from config import db


reference_tags = db.Table(
    "reference_tags",

    db.Column(
        "reference_id", db.Integer,
        db.ForeignKey("references_table.id", ondelete="CASCADE"),
        primary_key=True
        ),

    db.Column(
        "tag_id", db.Integer,
        db.ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
        )
)

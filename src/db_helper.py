from config import db, app
from entities.reference import Reference


def reset_db():
    """Clear all references from the database."""
    print("Clearing contents from table references_table")
    Reference.query.delete()
    db.session.commit()


def setup_db():
    """
    Create the database tables.
    If database tables already exist, those are dropped before the creation.
    """
    print("Dropping existing tables (if any)")
    db.drop_all()
    
    print("Creating database tables")
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()


from backend.app.database.connection import Base, engine
from backend.app.model.case_model import Case


def init_database() -> None:
    """Create all database tables defined by SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database tables created successfully.")
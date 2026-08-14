from backend.app.database.connection import Base, engine
from backend.app.model.case_model import Case
from backend.app.model.analysis_model import AnalysisResult


def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()
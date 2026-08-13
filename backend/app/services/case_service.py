from sqlalchemy.orm import Session

from backend.app.model.case_model import Case
from backend.app.schemas.case import CaseCreate


def create_case(
    db: Session,
    case_data: CaseCreate,
) -> Case:
    case = Case(
        patient_name=case_data.patient_name,
        patient_age=case_data.patient_age,
        description=case_data.description,
        status="created",
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case


def get_case(
    db: Session,
    case_id: int,
) -> Case | None:
    return (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )


def get_all_cases(
    db: Session,
) -> list[Case]:
    return db.query(Case).all()


def update_case_status(
    db: Session,
    case_id: int,
    status: str,
) -> Case | None:
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        return None

    case.status = status

    db.commit()
    db.refresh(case)

    return case
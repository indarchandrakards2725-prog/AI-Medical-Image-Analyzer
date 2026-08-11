from sqlalchemy.orm import Session

from backend.app.model.case_model import Case
from backend.app.schemas.case import CaseCreate, CaseResponse


def create_case(
    db: Session,
    case_data: CaseCreate,
) -> CaseResponse:
    case = Case(
        patient_name=case_data.patient_name,
        patient_age=case_data.patient_age,
        description=case_data.description,
        status="created",
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return CaseResponse(
        id=case.id,
        patient_name=case.patient_name,
        patient_age=case.patient_age,
        description=case.description,
        status=case.status,
    )


def get_case(
    db: Session,
    case_id: int,
) -> CaseResponse | None:
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        return None

    return CaseResponse(
        id=case.id,
        patient_name=case.patient_name,
        patient_age=case.patient_age,
        description=case.description,
        status=case.status,
    )


def get_all_cases(
    db: Session,
) -> list[CaseResponse]:
    cases = db.query(Case).all()

    return [
        CaseResponse(
            id=case.id,
            patient_name=case.patient_name,
            patient_age=case.patient_age,
            description=case.description,
            status=case.status,
        )
        for case in cases
    ]


def update_case_status(
    db: Session,
    case_id: int,
    status: str,
) -> CaseResponse | None:
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        return None

    case.status = status

    db.commit()
    db.refresh(case)

    return CaseResponse(
        id=case.id,
        patient_name=case.patient_name,
        patient_age=case.patient_age,
        description=case.description,
        status=case.status,
    )
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.schemas.analysis_result import AnalysisResultResponse

from backend.app.database.connection import get_db

from backend.app.schemas.case import (
    CaseCreate,
    CaseResponse,
    CaseStatusUpdate,
)

from backend.app.schemas.analysis_result import AnalysisResultResponse

from backend.app.services.case_service import (
    create_case,
    get_case,
    get_all_cases,
    update_case_status,
)

from backend.app.services.analysis_service import analyze_xray

from backend.app.services.analysis_result_service import (
    get_analysis_result,
    save_analysis_result,
)


router = APIRouter(
    prefix="/api/v1/cases",
    tags=["Cases"],
)


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
) -> CaseResponse:

    return create_case(db, case_data)


@router.get(
    "",
    response_model=list[CaseResponse],
)
def get_all_cases_route(
    db: Session = Depends(get_db),
) -> list[CaseResponse]:

    return get_all_cases(db)


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_existing_case(
    case_id: int,
    db: Session = Depends(get_db),
) -> CaseResponse:

    case = get_case(db, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


@router.patch(
    "/{case_id}/status",
    response_model=CaseResponse,
)
def update_existing_case_status(
    case_id: int,
    status_data: CaseStatusUpdate,
    db: Session = Depends(get_db),
) -> CaseResponse:

    case = update_case_status(
        db,
        case_id,
        status_data.status,
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


@router.post(
    "/{case_id}/analyze",
    response_model=CaseResponse,
)
def analyze_case(
    case_id: int,
    db: Session = Depends(get_db),
) -> CaseResponse:

    case = get_case(db, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    if not case.image_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="X-ray image not uploaded for this case",
        )

    update_case_status(
        db,
        case_id,
        "analyzing",
    )

    result = analyze_xray(case.image_path)

    save_analysis_result(
        db,
        case_id,
        result,
    )

    if result["status"] == "error":

        update_case_status(
            db,
            case_id,
            "uploaded",
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"],
        )

    return update_case_status(
        db,
        case_id,
        "awaiting_review",
    )


@router.get(
    "/{case_id}/analysis",
    response_model=AnalysisResultResponse,
)
def get_case_analysis(
    case_id: int,
    db: Session = Depends(get_db),
) -> AnalysisResultResponse:

    case = get_case(db, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    analysis_result = get_analysis_result(
        db,
        case_id,
    )

    if analysis_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis result not found",
        )

    return analysis_result
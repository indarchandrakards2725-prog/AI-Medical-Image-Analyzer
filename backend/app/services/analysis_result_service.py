from sqlalchemy.orm import Session

from backend.app.model.analysis_result_model import AnalysisResult


def save_analysis_result(
    db: Session,
    case_id: int,
    result: dict,
) -> AnalysisResult:

    analysis_result = AnalysisResult(
        case_id=case_id,
        status=result.get("status", "success"),
        message=result.get(
            "message",
            "X-ray image processed successfully",
        ),
        result_data=result.get("analysis"),
    )

    db.add(analysis_result)
    db.commit()
    db.refresh(analysis_result)

    return analysis_result


def get_analysis_result(
    db: Session,
    case_id: int,
) -> AnalysisResult | None:

    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.case_id == case_id)
        .order_by(AnalysisResult.id.desc())
        .first()
    )
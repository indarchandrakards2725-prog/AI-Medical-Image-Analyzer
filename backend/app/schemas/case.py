from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    patient_name: str = Field(
        min_length=1,
        max_length=100,
    )

    patient_age: int = Field(
        ge=18,
        le=120,
    )

    description: str = Field(
        min_length=1,
        max_length=500,
    )


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_name: str
    patient_age: int
    description: str
    status: str
    image_filename: str | None = None
    image_path: str | None = None


class CaseStatusUpdate(BaseModel):
    status: Literal[
        "created",
        "uploaded",
        "analyzing",
        "awaiting_review",
        "approved",
        "rejected",
    ]


class AnalysisResultResponse(BaseModel):
    id: int
    case_id: int
    status: str
    message: str
    result_data: dict[str, Any] | None = None
    created_at: datetime
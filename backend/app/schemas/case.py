from typing import Literal

from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    patient_name: str = Field(min_length=1, max_length=100)
    patient_age: int = Field(ge=18, le=120)
    description: str = Field(min_length=1, max_length=500)


class CaseResponse(BaseModel):
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
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AnalysisResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int
    status: str
    message: str
    result_data: dict[str, Any] | None = None
    created_at: datetime
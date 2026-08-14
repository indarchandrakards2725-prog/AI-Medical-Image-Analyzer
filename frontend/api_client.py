from typing import Any

import httpx

from config import API_BASE_URL, REQUEST_TIMEOUT_SECONDS


class APIClientError(Exception):
    """Raised when the frontend cannot complete an API request."""


def _request(
    method: str,
    path: str,
    **kwargs: Any,
) -> Any:
    try:
        with httpx.Client(
            base_url=API_BASE_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = client.request(method, path, **kwargs)

    except httpx.RequestError as exc:
        raise APIClientError(
            "Cannot connect to the backend. Make sure FastAPI is running."
        ) from exc

    if response.is_error:
        try:
            error_body = response.json()
            detail = error_body.get("detail", error_body)
        except ValueError:
            detail = response.text or "Unknown backend error"

        raise APIClientError(
            f"Backend returned {response.status_code}: {detail}"
        )

    if not response.content:
        return None

    return response.json()


def check_backend_health() -> dict:
    return _request("GET", "/api/v1/system/health")


def create_case(
    patient_name: str,
    patient_age: int,
    description: str,
) -> dict:
    payload = {
        "patient_name": patient_name,
        "patient_age": patient_age,
        "description": description,
    }

    return _request(
        "POST",
        "/api/v1/cases",
        json=payload,
    )


def get_cases() -> list[dict]:
    return _request("GET", "/api/v1/cases")


def get_case(case_id: int) -> dict:
    return _request("GET", f"/api/v1/cases/{case_id}")


def update_case_status(
    case_id: int,
    new_status: str,
) -> dict:
    return _request(
        "PATCH",
        f"/api/v1/cases/{case_id}/status",
        json={"status": new_status},
    )


def upload_xray(
    case_id: int,
    filename: str,
    content: bytes,
    content_type: str,
) -> dict:
    files = {
        "image": (
            filename,
            content,
            content_type,
        )
    }

    return _request(
        "POST",
        f"/api/v1/cases/{case_id}/image",
        files=files,
    )


def analyze_case(case_id: int) -> dict:
    return _request(
        "POST",
        f"/api/v1/cases/{case_id}/analyze",
    )
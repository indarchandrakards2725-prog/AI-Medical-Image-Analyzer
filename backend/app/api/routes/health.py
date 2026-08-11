from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/system",
    tags=["System"],
)


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Medical Image Analyzer",
        "message": "Backend is running",
    }
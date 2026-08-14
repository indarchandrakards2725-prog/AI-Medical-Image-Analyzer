from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.services.case_service import get_case


router = APIRouter(
    prefix="/api/v1/cases",
    tags=["Images"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/{case_id}/image")
async def upload_xray_image(
    case_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Check whether case exists
    case = get_case(db, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    # Basic image type check
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed",
        )

    # Get safe original filename
    original_filename = Path(image.filename or "xray_image").name

    # Create unique filename
    filename = f"case_{case_id}_{original_filename}"

    file_path = UPLOAD_DIR / filename

    # Save image
    contents = await image.read()
    file_path.write_bytes(contents)

    # Save image information in database
    case.image_filename = original_filename
    case.image_path = str(file_path)
    case.status = "uploaded"

    db.commit()
    db.refresh(case)

    return {
        "case_id": case_id,
        "filename": original_filename,
        "saved_as": str(file_path),
        "status": "uploaded",
    }
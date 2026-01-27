from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.file import FileType
from app.schemas.file import UploadedFileResponse, FileListResponse
from app.services.file_storage import save_file, get_file_path, list_files

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/resume", response_model=UploadedFileResponse, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a resume file."""
    uploaded = await save_file(db, file, FileType.RESUME)
    return uploaded


@router.post("/cover-letter", response_model=UploadedFileResponse, status_code=201)
async def upload_cover_letter(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a cover letter file."""
    uploaded = await save_file(db, file, FileType.COVER_LETTER)
    return uploaded


@router.get("/resumes", response_model=FileListResponse)
def list_resumes(db: Session = Depends(get_db)):
    """List all uploaded resumes."""
    files = list_files(db, FileType.RESUME)
    return FileListResponse(files=files, total=len(files))


@router.get("/cover-letters", response_model=FileListResponse)
def list_cover_letters(db: Session = Depends(get_db)):
    """List all uploaded cover letters."""
    files = list_files(db, FileType.COVER_LETTER)
    return FileListResponse(files=files, total=len(files))


@router.get("/resumes/{filename}")
def get_resume(filename: str):
    """Download a resume file."""
    file_path = get_file_path(filename, FileType.RESUME)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


@router.get("/cover-letters/{filename}")
def get_cover_letter(filename: str):
    """Download a cover letter file."""
    file_path = get_file_path(filename, FileType.COVER_LETTER)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )

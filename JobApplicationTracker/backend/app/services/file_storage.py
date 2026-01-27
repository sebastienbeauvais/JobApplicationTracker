from __future__ import annotations

import hashlib
from pathlib import Path
from typing import List

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import UploadedFile, FileType


def get_file_hash(content: bytes) -> str:
    """Generate a hash of file content for deduplication."""
    return hashlib.sha256(content).hexdigest()[:16]


def get_storage_path(file_type: FileType) -> Path:
    """Get the storage directory for a file type."""
    if file_type == FileType.RESUME:
        return settings.upload_dir / "resumes"
    return settings.upload_dir / "cover_letters"


async def save_file(
    db: Session,
    file: UploadFile,
    file_type: FileType,
) -> UploadedFile:
    """
    Save an uploaded file with deduplication.
    If a file with the same name exists, return the existing record.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # Check file extension
    extension = Path(file.filename).suffix.lower()
    if extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {settings.allowed_extensions}",
        )

    # Read file content
    content = await file.read()

    # Check file size
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_file_size // (1024 * 1024)}MB",
        )

    # Check if file with same name already exists
    existing = db.query(UploadedFile).filter(
        UploadedFile.filename == file.filename,
        UploadedFile.file_type == file_type,
    ).first()

    if existing:
        return existing

    # Save file to disk
    storage_path = get_storage_path(file_type)
    file_path = storage_path / file.filename

    with open(file_path, "wb") as f:
        f.write(content)

    # Create database record
    uploaded_file = UploadedFile(
        filename=file.filename,
        file_type=file_type,
        original_filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        file_size=len(content),
    )

    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    return uploaded_file


def get_file_path(filename: str, file_type: FileType) -> Path:
    """Get the full path to a stored file."""
    storage_path = get_storage_path(file_type)
    file_path = storage_path / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return file_path


def list_files(db: Session, file_type: FileType) -> List[UploadedFile]:
    """List all files of a given type."""
    return db.query(UploadedFile).filter(
        UploadedFile.file_type == file_type
    ).order_by(UploadedFile.uploaded_at.desc()).all()

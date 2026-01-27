from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models.file import FileType


class UploadedFileResponse(BaseModel):
    id: int
    filename: str
    file_type: FileType
    original_filename: str
    content_type: str
    file_size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    files: List[UploadedFileResponse]
    total: int

"""Tests for service modules."""

import io
from pathlib import Path

import pytest
from fastapi import HTTPException
from starlette.datastructures import Headers, UploadFile

from app.models.file import FileType, UploadedFile
from app.services.file_storage import (
    get_storage_path,
    save_file,
    get_file_path,
    list_files,
)
from app.core.config import settings


def create_upload_file(filename: str, content: bytes, content_type: str) -> UploadFile:
    """Helper to create UploadFile with content_type for testing."""
    return UploadFile(
        filename=filename,
        file=io.BytesIO(content),
        headers=Headers({"content-type": content_type}),
    )


class TestFileStorageService:
    """Tests for file storage service."""

    def test_get_storage_path_resume(self, temp_upload_dir):
        """Test getting storage path for resumes."""
        path = get_storage_path(FileType.RESUME)
        assert path == temp_upload_dir / "resumes"

    def test_get_storage_path_cover_letter(self, temp_upload_dir):
        """Test getting storage path for cover letters."""
        path = get_storage_path(FileType.COVER_LETTER)
        assert path == temp_upload_dir / "cover_letters"

    @pytest.mark.asyncio
    async def test_save_file_success(self, db_session, temp_upload_dir):
        """Test saving a file successfully."""
        file_content = b"%PDF-1.4 test content"
        upload_file = create_upload_file("test.pdf", file_content, "application/pdf")

        result = await save_file(db_session, upload_file, FileType.RESUME)

        assert result.filename == "test.pdf"
        assert result.file_type == FileType.RESUME
        assert result.file_size == len(file_content)

        # Verify file was written to disk
        file_path = temp_upload_dir / "resumes" / "test.pdf"
        assert file_path.exists()
        assert file_path.read_bytes() == file_content

    @pytest.mark.asyncio
    async def test_save_file_deduplication(self, db_session, temp_upload_dir):
        """Test that saving same filename returns existing record."""
        file_content = b"%PDF-1.4 test content"

        # First save
        upload_file1 = create_upload_file("test.pdf", file_content, "application/pdf")
        result1 = await save_file(db_session, upload_file1, FileType.RESUME)

        # Second save with same filename
        upload_file2 = create_upload_file("test.pdf", file_content, "application/pdf")
        result2 = await save_file(db_session, upload_file2, FileType.RESUME)

        assert result1.id == result2.id

    @pytest.mark.asyncio
    async def test_save_file_invalid_extension(self, db_session, temp_upload_dir):
        """Test that invalid extensions are rejected."""
        file_content = b"fake content"
        upload_file = create_upload_file("test.txt", file_content, "text/plain")

        with pytest.raises(HTTPException) as exc_info:
            await save_file(db_session, upload_file, FileType.RESUME)

        assert exc_info.value.status_code == 400
        assert "not allowed" in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_save_file_no_filename(self, db_session, temp_upload_dir):
        """Test that missing filename is rejected."""
        file_content = b"fake content"
        upload_file = create_upload_file("", file_content, "application/pdf")

        with pytest.raises(HTTPException) as exc_info:
            await save_file(db_session, upload_file, FileType.RESUME)

        assert exc_info.value.status_code == 400

    def test_get_file_path_success(self, temp_upload_dir, sample_uploaded_resume):
        """Test getting file path for existing file."""
        path = get_file_path(sample_uploaded_resume.filename, FileType.RESUME)

        assert path.exists()
        assert path.name == sample_uploaded_resume.filename

    def test_get_file_path_not_found(self, temp_upload_dir):
        """Test getting file path for non-existent file."""
        with pytest.raises(HTTPException) as exc_info:
            get_file_path("nonexistent.pdf", FileType.RESUME)

        assert exc_info.value.status_code == 404

    def test_list_files_empty(self, db_session, temp_upload_dir):
        """Test listing files when none exist."""
        files = list_files(db_session, FileType.RESUME)
        assert files == []

    def test_list_files_with_data(self, db_session, temp_upload_dir, sample_uploaded_resume):
        """Test listing files with data."""
        files = list_files(db_session, FileType.RESUME)

        assert len(files) == 1
        assert files[0].filename == sample_uploaded_resume.filename

    def test_list_files_filters_by_type(self, db_session, temp_upload_dir):
        """Test that list_files filters by file type."""
        # Create resume
        resume = UploadedFile(
            filename="resume.pdf",
            file_type=FileType.RESUME,
            original_filename="resume.pdf",
            content_type="application/pdf",
            file_size=1024,
        )
        db_session.add(resume)

        # Create cover letter
        cover_letter = UploadedFile(
            filename="cover.pdf",
            file_type=FileType.COVER_LETTER,
            original_filename="cover.pdf",
            content_type="application/pdf",
            file_size=1024,
        )
        db_session.add(cover_letter)
        db_session.commit()

        # List only resumes
        resumes = list_files(db_session, FileType.RESUME)
        assert len(resumes) == 1
        assert resumes[0].filename == "resume.pdf"

        # List only cover letters
        cover_letters = list_files(db_session, FileType.COVER_LETTER)
        assert len(cover_letters) == 1
        assert cover_letters[0].filename == "cover.pdf"

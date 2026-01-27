"""Tests for uploads API endpoints."""

import io

import pytest


class TestUploadResume:
    """Tests for POST /api/uploads/resume endpoint."""

    def test_upload_resume_success(self, client):
        """Test successful resume upload."""
        file_content = b"%PDF-1.4 fake pdf content"
        files = {"file": ("resume.pdf", io.BytesIO(file_content), "application/pdf")}

        response = client.post("/api/uploads/resume", files=files)

        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "resume.pdf"
        assert data["file_type"] == "resume"
        assert data["file_size"] == len(file_content)

    def test_upload_resume_doc_format(self, client):
        """Test uploading .doc format."""
        file_content = b"fake doc content"
        files = {"file": ("resume.doc", io.BytesIO(file_content), "application/msword")}

        response = client.post("/api/uploads/resume", files=files)

        assert response.status_code == 201

    def test_upload_resume_docx_format(self, client):
        """Test uploading .docx format."""
        file_content = b"fake docx content"
        files = {
            "file": (
                "resume.docx",
                io.BytesIO(file_content),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }

        response = client.post("/api/uploads/resume", files=files)

        assert response.status_code == 201

    def test_upload_resume_invalid_extension(self, client):
        """Test uploading file with invalid extension."""
        file_content = b"fake content"
        files = {"file": ("resume.txt", io.BytesIO(file_content), "text/plain")}

        response = client.post("/api/uploads/resume", files=files)

        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"].lower()

    def test_upload_resume_deduplication(self, client):
        """Test that uploading same filename returns existing record."""
        file_content = b"%PDF-1.4 fake pdf content"
        files = {"file": ("resume.pdf", io.BytesIO(file_content), "application/pdf")}

        # First upload
        response1 = client.post("/api/uploads/resume", files=files)
        assert response1.status_code == 201
        id1 = response1.json()["id"]

        # Second upload with same filename
        files = {"file": ("resume.pdf", io.BytesIO(file_content), "application/pdf")}
        response2 = client.post("/api/uploads/resume", files=files)
        assert response2.status_code == 201
        id2 = response2.json()["id"]

        # Should return same record
        assert id1 == id2


class TestUploadCoverLetter:
    """Tests for POST /api/uploads/cover-letter endpoint."""

    def test_upload_cover_letter_success(self, client):
        """Test successful cover letter upload."""
        file_content = b"%PDF-1.4 fake pdf content"
        files = {
            "file": ("cover_letter.pdf", io.BytesIO(file_content), "application/pdf")
        }

        response = client.post("/api/uploads/cover-letter", files=files)

        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "cover_letter.pdf"
        assert data["file_type"] == "cover_letter"

    def test_upload_cover_letter_invalid_extension(self, client):
        """Test uploading file with invalid extension."""
        file_content = b"fake content"
        files = {"file": ("cover.jpg", io.BytesIO(file_content), "image/jpeg")}

        response = client.post("/api/uploads/cover-letter", files=files)

        assert response.status_code == 400


class TestListResumes:
    """Tests for GET /api/uploads/resumes endpoint."""

    def test_list_resumes_empty(self, client):
        """Test listing resumes when none exist."""
        response = client.get("/api/uploads/resumes")

        assert response.status_code == 200
        data = response.json()
        assert data["files"] == []
        assert data["total"] == 0

    def test_list_resumes_with_data(self, client):
        """Test listing resumes with data."""
        # Upload a resume
        file_content = b"%PDF-1.4 fake pdf"
        files = {"file": ("resume.pdf", io.BytesIO(file_content), "application/pdf")}
        client.post("/api/uploads/resume", files=files)

        response = client.get("/api/uploads/resumes")

        assert response.status_code == 200
        data = response.json()
        assert len(data["files"]) == 1
        assert data["total"] == 1
        assert data["files"][0]["filename"] == "resume.pdf"

    def test_list_resumes_multiple(self, client):
        """Test listing multiple resumes."""
        for i in range(3):
            file_content = b"%PDF-1.4 fake pdf"
            files = {
                "file": (f"resume_{i}.pdf", io.BytesIO(file_content), "application/pdf")
            }
            client.post("/api/uploads/resume", files=files)

        response = client.get("/api/uploads/resumes")

        assert response.status_code == 200
        data = response.json()
        assert len(data["files"]) == 3
        assert data["total"] == 3


class TestListCoverLetters:
    """Tests for GET /api/uploads/cover-letters endpoint."""

    def test_list_cover_letters_empty(self, client):
        """Test listing cover letters when none exist."""
        response = client.get("/api/uploads/cover-letters")

        assert response.status_code == 200
        data = response.json()
        assert data["files"] == []
        assert data["total"] == 0

    def test_list_cover_letters_with_data(self, client):
        """Test listing cover letters with data."""
        # Upload a cover letter
        file_content = b"%PDF-1.4 fake pdf"
        files = {
            "file": ("cover_letter.pdf", io.BytesIO(file_content), "application/pdf")
        }
        client.post("/api/uploads/cover-letter", files=files)

        response = client.get("/api/uploads/cover-letters")

        assert response.status_code == 200
        data = response.json()
        assert len(data["files"]) == 1
        assert data["files"][0]["filename"] == "cover_letter.pdf"


class TestGetResumeFile:
    """Tests for GET /api/uploads/resumes/{filename} endpoint."""

    def test_get_resume_file_success(self, client):
        """Test downloading a resume file."""
        file_content = b"%PDF-1.4 test resume content"
        files = {"file": ("resume.pdf", io.BytesIO(file_content), "application/pdf")}
        client.post("/api/uploads/resume", files=files)

        response = client.get("/api/uploads/resumes/resume.pdf")

        assert response.status_code == 200
        assert response.content == file_content

    def test_get_resume_file_not_found(self, client):
        """Test downloading non-existent resume."""
        response = client.get("/api/uploads/resumes/nonexistent.pdf")

        assert response.status_code == 404


class TestGetCoverLetterFile:
    """Tests for GET /api/uploads/cover-letters/{filename} endpoint."""

    def test_get_cover_letter_file_success(self, client):
        """Test downloading a cover letter file."""
        file_content = b"%PDF-1.4 test cover letter content"
        files = {
            "file": ("cover_letter.pdf", io.BytesIO(file_content), "application/pdf")
        }
        client.post("/api/uploads/cover-letter", files=files)

        response = client.get("/api/uploads/cover-letters/cover_letter.pdf")

        assert response.status_code == 200
        assert response.content == file_content

    def test_get_cover_letter_file_not_found(self, client):
        """Test downloading non-existent cover letter."""
        response = client.get("/api/uploads/cover-letters/nonexistent.pdf")

        assert response.status_code == 404

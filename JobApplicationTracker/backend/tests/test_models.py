"""Tests for SQLAlchemy models."""

from datetime import date, datetime

import pytest

from app.models.job import JobApplication, JobStatus, CompensationType
from app.models.file import UploadedFile, FileType


class TestJobApplicationModel:
    """Tests for JobApplication model."""

    def test_create_job_application(self, db_session):
        """Test creating a job application."""
        job = JobApplication(
            job_title="Software Engineer",
            company="Tech Corp",
            compensation_min=100000,
            compensation_max=150000,
            compensation_type=CompensationType.ANNUAL,
            application_date=date.today(),
            job_posting_url="https://example.com/job",
            resume_filename="resume.pdf",
        )

        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)

        assert job.id is not None
        assert job.job_title == "Software Engineer"
        assert job.company == "Tech Corp"
        assert job.status == JobStatus.APPLIED  # Default status
        assert job.got_interview is False  # Default value
        assert job.coding_question_link is None
        assert job.created_at is not None
        assert job.updated_at is not None

    def test_job_default_status_is_applied(self, db_session):
        """Test that default status is 'applied'."""
        job = JobApplication(
            job_title="Developer",
            company="Startup",
            compensation_min=80000,
            compensation_type=CompensationType.ANNUAL,
            application_date=date.today(),
            job_posting_url="https://example.com",
            resume_filename="resume.pdf",
        )

        db_session.add(job)
        db_session.commit()

        assert job.status == JobStatus.APPLIED

    def test_job_default_got_interview_is_false(self, db_session):
        """Test that default got_interview is False."""
        job = JobApplication(
            job_title="Developer",
            company="Startup",
            compensation_min=80000,
            compensation_type=CompensationType.ANNUAL,
            application_date=date.today(),
            job_posting_url="https://example.com",
            resume_filename="resume.pdf",
        )

        db_session.add(job)
        db_session.commit()

        assert job.got_interview is False

    def test_job_optional_fields(self, db_session):
        """Test job with optional fields as None."""
        job = JobApplication(
            job_title="Developer",
            company="Startup",
            compensation_min=80000,
            compensation_max=None,
            compensation_type=CompensationType.HOURLY,
            application_date=date.today(),
            job_posting_url="https://example.com",
            resume_filename="resume.pdf",
            cover_letter_filename=None,
        )

        db_session.add(job)
        db_session.commit()

        assert job.compensation_max is None
        assert job.cover_letter_filename is None

    def test_job_update_status(self, db_session, sample_job):
        """Test updating job status."""
        sample_job.status = JobStatus.INTERVIEWING
        db_session.commit()
        db_session.refresh(sample_job)

        assert sample_job.status == JobStatus.INTERVIEWING

    def test_job_update_got_interview(self, db_session, sample_job):
        """Test updating got_interview flag."""
        sample_job.got_interview = True
        db_session.commit()
        db_session.refresh(sample_job)

        assert sample_job.got_interview is True

    def test_job_update_coding_question_link(self, db_session, sample_job):
        """Test updating coding question link."""
        link = "https://github.com/user/coding-challenge"
        sample_job.coding_question_link = link
        db_session.commit()
        db_session.refresh(sample_job)

        assert sample_job.coding_question_link == link

    def test_compensation_type_enum_values(self):
        """Test CompensationType enum values."""
        assert CompensationType.HOURLY.value == "hourly"
        assert CompensationType.ANNUAL.value == "annual"

    def test_job_status_enum_values(self):
        """Test JobStatus enum values."""
        assert JobStatus.APPLIED.value == "applied"
        assert JobStatus.INTERVIEWING.value == "interviewing"
        assert JobStatus.OFFER_RECEIVED.value == "offer_received"
        assert JobStatus.ACCEPTED.value == "accepted"
        assert JobStatus.REJECTED.value == "rejected"
        assert JobStatus.WITHDRAWN.value == "withdrawn"


class TestUploadedFileModel:
    """Tests for UploadedFile model."""

    def test_create_uploaded_file(self, db_session):
        """Test creating an uploaded file record."""
        uploaded_file = UploadedFile(
            filename="resume.pdf",
            file_type=FileType.RESUME,
            original_filename="my_resume.pdf",
            content_type="application/pdf",
            file_size=1024,
        )

        db_session.add(uploaded_file)
        db_session.commit()
        db_session.refresh(uploaded_file)

        assert uploaded_file.id is not None
        assert uploaded_file.filename == "resume.pdf"
        assert uploaded_file.file_type == FileType.RESUME
        assert uploaded_file.uploaded_at is not None

    def test_file_type_enum_values(self):
        """Test FileType enum values."""
        assert FileType.RESUME.value == "resume"
        assert FileType.COVER_LETTER.value == "cover_letter"

    def test_uploaded_file_resume_type(self, db_session):
        """Test resume file type."""
        uploaded_file = UploadedFile(
            filename="resume.pdf",
            file_type=FileType.RESUME,
            original_filename="resume.pdf",
            content_type="application/pdf",
            file_size=2048,
        )

        db_session.add(uploaded_file)
        db_session.commit()

        assert uploaded_file.file_type == FileType.RESUME

    def test_uploaded_file_cover_letter_type(self, db_session):
        """Test cover letter file type."""
        uploaded_file = UploadedFile(
            filename="cover_letter.pdf",
            file_type=FileType.COVER_LETTER,
            original_filename="cover_letter.pdf",
            content_type="application/pdf",
            file_size=1024,
        )

        db_session.add(uploaded_file)
        db_session.commit()

        assert uploaded_file.file_type == FileType.COVER_LETTER

    def test_filename_uniqueness(self, db_session):
        """Test that filename must be unique."""
        file1 = UploadedFile(
            filename="resume.pdf",
            file_type=FileType.RESUME,
            original_filename="resume.pdf",
            content_type="application/pdf",
            file_size=1024,
        )

        db_session.add(file1)
        db_session.commit()

        file2 = UploadedFile(
            filename="resume.pdf",
            file_type=FileType.RESUME,
            original_filename="resume.pdf",
            content_type="application/pdf",
            file_size=1024,
        )

        db_session.add(file2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

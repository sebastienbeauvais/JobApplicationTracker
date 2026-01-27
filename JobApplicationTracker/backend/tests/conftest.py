import os
import tempfile
from pathlib import Path
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.config import settings
from app.main import app
from app.models.job import JobApplication, JobStatus, CompensationType
from app.models.file import UploadedFile, FileType


@pytest.fixture(scope="function")
def temp_upload_dir(tmp_path):
    """Create temporary upload directories for tests."""
    resumes_dir = tmp_path / "resumes"
    cover_letters_dir = tmp_path / "cover_letters"
    resumes_dir.mkdir()
    cover_letters_dir.mkdir()

    # Temporarily override settings
    original_upload_dir = settings.upload_dir
    settings.upload_dir = tmp_path

    yield tmp_path

    # Restore original settings
    settings.upload_dir = original_upload_dir


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session, temp_upload_dir):
    """Create a test client with overridden dependencies."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_job_data():
    """Sample job application data for testing."""
    return {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "compensation_min": 100000,
        "compensation_max": 150000,
        "compensation_type": "annual",
        "application_date": str(date.today()),
        "job_posting_url": "https://example.com/job",
        "resume_filename": "resume.pdf",
        "cover_letter_filename": "cover_letter.pdf",
    }


@pytest.fixture
def sample_job(db_session, sample_job_data):
    """Create a sample job in the database."""
    job = JobApplication(
        job_title=sample_job_data["job_title"],
        company=sample_job_data["company"],
        compensation_min=sample_job_data["compensation_min"],
        compensation_max=sample_job_data["compensation_max"],
        compensation_type=CompensationType.ANNUAL,
        application_date=date.today(),
        job_posting_url=sample_job_data["job_posting_url"],
        resume_filename=sample_job_data["resume_filename"],
        cover_letter_filename=sample_job_data["cover_letter_filename"],
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job


@pytest.fixture
def sample_resume_file():
    """Create a sample resume file content."""
    return b"%PDF-1.4 fake pdf content for testing"


@pytest.fixture
def sample_uploaded_resume(db_session, temp_upload_dir, sample_resume_file):
    """Create a sample uploaded resume in the database and filesystem."""
    filename = "test_resume.pdf"

    # Write file to disk
    file_path = temp_upload_dir / "resumes" / filename
    file_path.write_bytes(sample_resume_file)

    # Create database record
    uploaded_file = UploadedFile(
        filename=filename,
        file_type=FileType.RESUME,
        original_filename=filename,
        content_type="application/pdf",
        file_size=len(sample_resume_file),
    )
    db_session.add(uploaded_file)
    db_session.commit()
    db_session.refresh(uploaded_file)

    return uploaded_file

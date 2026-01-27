"""Tests for Pydantic schemas validation."""

from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.job import JobApplicationCreate, JobApplicationUpdate
from app.models.job import CompensationType, JobStatus


class TestJobApplicationCreateSchema:
    """Tests for JobApplicationCreate schema validation."""

    def test_valid_job_data(self, sample_job_data):
        """Test that valid job data passes validation."""
        job = JobApplicationCreate(**sample_job_data)
        assert job.job_title == sample_job_data["job_title"]
        assert job.company == sample_job_data["company"]
        assert job.compensation_min == sample_job_data["compensation_min"]

    def test_job_title_max_length(self, sample_job_data):
        """Test job title max length validation (100 chars)."""
        sample_job_data["job_title"] = "x" * 101
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "job_title" in str(exc_info.value)

    def test_job_title_min_length(self, sample_job_data):
        """Test job title min length validation."""
        sample_job_data["job_title"] = ""
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "job_title" in str(exc_info.value)

    def test_company_max_length(self, sample_job_data):
        """Test company max length validation (50 chars)."""
        sample_job_data["company"] = "x" * 51
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "company" in str(exc_info.value)

    def test_company_min_length(self, sample_job_data):
        """Test company min length validation."""
        sample_job_data["company"] = ""
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "company" in str(exc_info.value)

    def test_compensation_min_negative(self, sample_job_data):
        """Test that negative compensation is rejected."""
        sample_job_data["compensation_min"] = -1
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "compensation_min" in str(exc_info.value)

    def test_compensation_max_less_than_min(self, sample_job_data):
        """Test that max compensation must be >= min."""
        sample_job_data["compensation_min"] = 100000
        sample_job_data["compensation_max"] = 50000
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "compensation_max" in str(exc_info.value).lower() or "Maximum" in str(exc_info.value)

    def test_compensation_max_optional(self, sample_job_data):
        """Test that max compensation is optional."""
        sample_job_data["compensation_max"] = None
        job = JobApplicationCreate(**sample_job_data)
        assert job.compensation_max is None

    def test_application_date_future(self, sample_job_data):
        """Test that future application date is rejected."""
        sample_job_data["application_date"] = str(date.today() + timedelta(days=1))
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "future" in str(exc_info.value).lower()

    def test_application_date_today(self, sample_job_data):
        """Test that today's date is accepted."""
        sample_job_data["application_date"] = str(date.today())
        job = JobApplicationCreate(**sample_job_data)
        assert job.application_date == date.today()

    def test_application_date_past(self, sample_job_data):
        """Test that past dates are accepted."""
        past_date = date.today() - timedelta(days=30)
        sample_job_data["application_date"] = str(past_date)
        job = JobApplicationCreate(**sample_job_data)
        assert job.application_date == past_date

    def test_invalid_url_no_protocol(self, sample_job_data):
        """Test that URL without protocol is rejected."""
        sample_job_data["job_posting_url"] = "example.com/job"
        with pytest.raises(ValidationError) as exc_info:
            JobApplicationCreate(**sample_job_data)
        assert "url" in str(exc_info.value).lower() or "http" in str(exc_info.value).lower()

    def test_valid_url_https(self, sample_job_data):
        """Test that https URL is accepted."""
        sample_job_data["job_posting_url"] = "https://example.com/job"
        job = JobApplicationCreate(**sample_job_data)
        assert job.job_posting_url == "https://example.com/job"

    def test_valid_url_http(self, sample_job_data):
        """Test that http URL is accepted."""
        sample_job_data["job_posting_url"] = "http://example.com/job"
        job = JobApplicationCreate(**sample_job_data)
        assert job.job_posting_url == "http://example.com/job"

    def test_cover_letter_optional(self, sample_job_data):
        """Test that cover letter is optional."""
        sample_job_data["cover_letter_filename"] = None
        job = JobApplicationCreate(**sample_job_data)
        assert job.cover_letter_filename is None

    def test_compensation_type_hourly(self, sample_job_data):
        """Test hourly compensation type."""
        sample_job_data["compensation_type"] = "hourly"
        job = JobApplicationCreate(**sample_job_data)
        assert job.compensation_type == CompensationType.HOURLY

    def test_compensation_type_annual(self, sample_job_data):
        """Test annual compensation type."""
        sample_job_data["compensation_type"] = "annual"
        job = JobApplicationCreate(**sample_job_data)
        assert job.compensation_type == CompensationType.ANNUAL

    def test_invalid_compensation_type(self, sample_job_data):
        """Test invalid compensation type."""
        sample_job_data["compensation_type"] = "weekly"
        with pytest.raises(ValidationError):
            JobApplicationCreate(**sample_job_data)


class TestJobApplicationUpdateSchema:
    """Tests for JobApplicationUpdate schema validation."""

    def test_update_status_valid(self):
        """Test valid status update."""
        update = JobApplicationUpdate(status=JobStatus.INTERVIEWING)
        assert update.status == JobStatus.INTERVIEWING

    def test_update_got_interview(self):
        """Test got_interview update."""
        update = JobApplicationUpdate(got_interview=True)
        assert update.got_interview is True

    def test_update_coding_question_link_valid(self):
        """Test valid coding question link."""
        update = JobApplicationUpdate(
            coding_question_link="https://github.com/user/repo"
        )
        assert update.coding_question_link == "https://github.com/user/repo"

    def test_update_coding_question_link_invalid(self):
        """Test invalid coding question link (no protocol)."""
        with pytest.raises(ValidationError):
            JobApplicationUpdate(coding_question_link="github.com/user/repo")

    def test_update_coding_question_link_empty(self):
        """Test empty coding question link becomes None."""
        update = JobApplicationUpdate(coding_question_link="")
        assert update.coding_question_link is None

    def test_update_coding_question_link_whitespace(self):
        """Test whitespace-only coding question link becomes None."""
        update = JobApplicationUpdate(coding_question_link="   ")
        assert update.coding_question_link is None

    def test_update_partial(self):
        """Test partial update with only some fields."""
        update = JobApplicationUpdate(status=JobStatus.REJECTED)
        assert update.status == JobStatus.REJECTED
        assert update.got_interview is None
        assert update.coding_question_link is None

    def test_update_all_statuses(self):
        """Test all status enum values."""
        for status in JobStatus:
            update = JobApplicationUpdate(status=status)
            assert update.status == status

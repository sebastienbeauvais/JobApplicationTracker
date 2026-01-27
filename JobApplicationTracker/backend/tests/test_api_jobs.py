"""Tests for jobs API endpoints."""

from datetime import date, timedelta

import pytest


class TestCreateJob:
    """Tests for POST /api/jobs endpoint."""

    def test_create_job_success(self, client, sample_job_data):
        """Test successful job creation."""
        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 201
        data = response.json()
        assert data["job_title"] == sample_job_data["job_title"]
        assert data["company"] == sample_job_data["company"]
        assert data["compensation_min"] == sample_job_data["compensation_min"]
        assert data["status"] == "applied"  # Default status
        assert data["got_interview"] is False  # Default value
        assert "id" in data
        assert "created_at" in data

    def test_create_job_minimal_data(self, client):
        """Test job creation with minimal required fields."""
        minimal_data = {
            "job_title": "Developer",
            "company": "Startup",
            "compensation_min": 50000,
            "compensation_type": "annual",
            "application_date": str(date.today()),
            "job_posting_url": "https://example.com",
            "resume_filename": "resume.pdf",
        }

        response = client.post("/api/jobs", json=minimal_data)

        assert response.status_code == 201
        data = response.json()
        assert data["compensation_max"] is None
        assert data["cover_letter_filename"] is None

    def test_create_job_invalid_title_too_long(self, client, sample_job_data):
        """Test job creation fails with title > 100 chars."""
        sample_job_data["job_title"] = "x" * 101

        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 422

    def test_create_job_invalid_company_too_long(self, client, sample_job_data):
        """Test job creation fails with company > 50 chars."""
        sample_job_data["company"] = "x" * 51

        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 422

    def test_create_job_invalid_future_date(self, client, sample_job_data):
        """Test job creation fails with future date."""
        sample_job_data["application_date"] = str(date.today() + timedelta(days=1))

        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 422

    def test_create_job_invalid_url(self, client, sample_job_data):
        """Test job creation fails with invalid URL."""
        sample_job_data["job_posting_url"] = "not-a-valid-url"

        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 422

    def test_create_job_missing_required_field(self, client, sample_job_data):
        """Test job creation fails without required field."""
        del sample_job_data["job_title"]

        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 422

    def test_create_job_hourly_compensation(self, client, sample_job_data):
        """Test job creation with hourly compensation."""
        sample_job_data["compensation_type"] = "hourly"
        sample_job_data["compensation_min"] = 50
        sample_job_data["compensation_max"] = 75

        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == 201
        data = response.json()
        assert data["compensation_type"] == "hourly"


class TestListJobs:
    """Tests for GET /api/jobs endpoint."""

    def test_list_jobs_empty(self, client):
        """Test listing jobs when none exist."""
        response = client.get("/api/jobs")

        assert response.status_code == 200
        data = response.json()
        assert data["jobs"] == []
        assert data["total"] == 0

    def test_list_jobs_with_data(self, client, sample_job_data):
        """Test listing jobs with data."""
        # Create a job first
        client.post("/api/jobs", json=sample_job_data)

        response = client.get("/api/jobs")

        assert response.status_code == 200
        data = response.json()
        assert len(data["jobs"]) == 1
        assert data["total"] == 1
        assert data["jobs"][0]["job_title"] == sample_job_data["job_title"]

    def test_list_jobs_multiple(self, client, sample_job_data):
        """Test listing multiple jobs."""
        # Create multiple jobs
        for i in range(3):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            client.post("/api/jobs", json=job_data)

        response = client.get("/api/jobs")

        assert response.status_code == 200
        data = response.json()
        assert len(data["jobs"]) == 3
        assert data["total"] == 3

    def test_list_jobs_ordered_by_created_at_desc(self, client, sample_job_data):
        """Test that jobs are ordered by created_at descending."""
        # Create jobs
        for i in range(3):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            client.post("/api/jobs", json=job_data)

        response = client.get("/api/jobs")
        data = response.json()

        # Most recent should be first
        assert data["jobs"][0]["job_title"] == "Job 2"


class TestGetJob:
    """Tests for GET /api/jobs/{job_id} endpoint."""

    def test_get_job_success(self, client, sample_job_data):
        """Test getting a single job."""
        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        response = client.get(f"/api/jobs/{job_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["job_title"] == sample_job_data["job_title"]

    def test_get_job_not_found(self, client):
        """Test getting a non-existent job."""
        response = client.get("/api/jobs/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateJob:
    """Tests for PATCH /api/jobs/{job_id} endpoint."""

    def test_update_job_status(self, client, sample_job_data):
        """Test updating job status."""
        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        # Update status
        response = client.patch(
            f"/api/jobs/{job_id}",
            json={"status": "interviewing"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "interviewing"

    def test_update_job_got_interview(self, client, sample_job_data):
        """Test updating got_interview flag."""
        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        # Update got_interview
        response = client.patch(
            f"/api/jobs/{job_id}",
            json={"got_interview": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["got_interview"] is True

    def test_update_job_coding_question_link(self, client, sample_job_data):
        """Test updating coding question link."""
        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        # Update coding question link
        link = "https://github.com/user/challenge"
        response = client.patch(
            f"/api/jobs/{job_id}",
            json={"coding_question_link": link},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["coding_question_link"] == link

    def test_update_job_multiple_fields(self, client, sample_job_data):
        """Test updating multiple fields at once."""
        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        # Update multiple fields
        response = client.patch(
            f"/api/jobs/{job_id}",
            json={
                "status": "offer_received",
                "got_interview": True,
                "coding_question_link": "https://github.com/test/repo",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "offer_received"
        assert data["got_interview"] is True
        assert data["coding_question_link"] == "https://github.com/test/repo"

    def test_update_job_not_found(self, client):
        """Test updating a non-existent job."""
        response = client.patch(
            "/api/jobs/999",
            json={"status": "interviewing"},
        )

        assert response.status_code == 404

    def test_update_job_all_statuses(self, client, sample_job_data):
        """Test updating to all possible statuses."""
        statuses = [
            "applied",
            "interviewing",
            "offer_received",
            "accepted",
            "rejected",
            "withdrawn",
        ]

        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        for status in statuses:
            response = client.patch(
                f"/api/jobs/{job_id}",
                json={"status": status},
            )
            assert response.status_code == 200
            assert response.json()["status"] == status

    def test_update_job_invalid_status(self, client, sample_job_data):
        """Test updating with invalid status."""
        # Create a job
        create_response = client.post("/api/jobs", json=sample_job_data)
        job_id = create_response.json()["id"]

        response = client.patch(
            f"/api/jobs/{job_id}",
            json={"status": "invalid_status"},
        )

        assert response.status_code == 422

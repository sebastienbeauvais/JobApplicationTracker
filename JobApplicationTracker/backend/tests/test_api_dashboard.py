"""Tests for dashboard API endpoints."""

from datetime import date, timedelta

import pytest


class TestGetDashboard:
    """Tests for GET /api/dashboard endpoint."""

    def test_dashboard_empty(self, client):
        """Test dashboard with no data."""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_applications"] == 0
        assert data["interview_rate"] == 0.0
        assert data["recent_applications"] == []
        assert len(data["applications_by_status"]) == 6  # All statuses represented
        assert len(data["applications_over_time"]) == 31  # 30 days + today

    def test_dashboard_total_applications(self, client, sample_job_data):
        """Test total applications count."""
        # Create 3 jobs
        for i in range(3):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            client.post("/api/jobs", json=job_data)

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_applications"] == 3

    def test_dashboard_applications_by_status(self, client, sample_job_data):
        """Test applications by status breakdown."""
        # Create jobs with different statuses
        for i in range(3):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            create_resp = client.post("/api/jobs", json=job_data)
            job_id = create_resp.json()["id"]

            if i == 1:
                client.patch(f"/api/jobs/{job_id}", json={"status": "interviewing"})
            elif i == 2:
                client.patch(f"/api/jobs/{job_id}", json={"status": "rejected"})

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()

        status_map = {s["status"]: s["count"] for s in data["applications_by_status"]}
        assert status_map["applied"] == 1
        assert status_map["interviewing"] == 1
        assert status_map["rejected"] == 1
        assert status_map["accepted"] == 0

    def test_dashboard_interview_rate(self, client, sample_job_data):
        """Test interview rate calculation."""
        # Create 4 jobs, 2 with interviews
        for i in range(4):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            create_resp = client.post("/api/jobs", json=job_data)
            job_id = create_resp.json()["id"]

            if i < 2:
                client.patch(f"/api/jobs/{job_id}", json={"got_interview": True})

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["interview_rate"] == 50.0  # 2 out of 4 = 50%

    def test_dashboard_interview_rate_zero(self, client, sample_job_data):
        """Test interview rate when no interviews."""
        # Create jobs without interviews
        for i in range(3):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            client.post("/api/jobs", json=job_data)

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["interview_rate"] == 0.0

    def test_dashboard_recent_applications(self, client, sample_job_data):
        """Test recent applications list."""
        # Create jobs
        for i in range(15):
            job_data = sample_job_data.copy()
            job_data["job_title"] = f"Job {i}"
            client.post("/api/jobs", json=job_data)

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert len(data["recent_applications"]) == 10  # Max 10 recent

    def test_dashboard_recent_applications_fields(self, client, sample_job_data):
        """Test recent applications contain expected fields."""
        client.post("/api/jobs", json=sample_job_data)

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        recent = data["recent_applications"][0]

        assert "id" in recent
        assert "job_title" in recent
        assert "company" in recent
        assert "status" in recent
        assert "application_date" in recent

    def test_dashboard_applications_over_time(self, client, sample_job_data):
        """Test applications over time includes today."""
        # Create a job with today's date
        client.post("/api/jobs", json=sample_job_data)

        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()

        # Find today in the data
        today_str = str(date.today())
        today_count = None
        for entry in data["applications_over_time"]:
            if entry["date"] == today_str:
                today_count = entry["count"]
                break

        assert today_count == 1

    def test_dashboard_applications_over_time_length(self, client):
        """Test applications over time returns 31 days."""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()

        # Should have 31 entries (30 days + today)
        assert len(data["applications_over_time"]) == 31

    def test_dashboard_all_statuses_represented(self, client):
        """Test all statuses are in the response even with no data."""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()

        expected_statuses = {
            "applied",
            "interviewing",
            "offer_received",
            "accepted",
            "rejected",
            "withdrawn",
        }

        actual_statuses = {s["status"] for s in data["applications_by_status"]}
        assert actual_statuses == expected_statuses

    def test_dashboard_status_order(self, client):
        """Test statuses are in logical order."""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()

        status_order = [s["status"] for s in data["applications_by_status"]]
        expected_order = [
            "applied",
            "interviewing",
            "offer_received",
            "accepted",
            "rejected",
            "withdrawn",
        ]

        assert status_order == expected_order

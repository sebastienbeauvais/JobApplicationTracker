from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel

from app.models.job import JobStatus


class StatusCount(BaseModel):
    status: JobStatus
    count: int


class ApplicationOverTime(BaseModel):
    date: date
    count: int


class RecentApplication(BaseModel):
    id: int
    job_title: str
    company: str
    status: JobStatus
    application_date: date


class DashboardResponse(BaseModel):
    total_applications: int
    applications_by_status: List[StatusCount]
    interview_rate: float  # Percentage (0-100)
    applications_over_time: List[ApplicationOverTime]
    recent_applications: List[RecentApplication]

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.models.job import CompensationType, JobStatus


class JobApplicationCreate(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=100)
    company: str = Field(..., min_length=1, max_length=50)
    compensation_min: int = Field(..., ge=0)
    compensation_max: Optional[int] = Field(None, ge=0)
    compensation_type: CompensationType
    application_date: date
    job_posting_url: str
    resume_filename: str
    cover_letter_filename: Optional[str] = None

    @field_validator("application_date")
    @classmethod
    def date_not_in_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Application date cannot be in the future")
        return v

    @field_validator("compensation_max")
    @classmethod
    def max_greater_than_min(cls, v: Optional[int], info) -> Optional[int]:
        if v is not None and "compensation_min" in info.data:
            if v < info.data["compensation_min"]:
                raise ValueError("Maximum compensation must be >= minimum")
        return v

    @field_validator("job_posting_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        # Basic URL validation
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class JobApplicationUpdate(BaseModel):
    status: Optional[JobStatus] = None
    got_interview: Optional[bool] = None
    coding_question_link: Optional[str] = None

    @field_validator("coding_question_link")
    @classmethod
    def validate_github_url(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip():
            if not v.startswith(("http://", "https://")):
                raise ValueError("URL must start with http:// or https://")
        return v if v and v.strip() else None


class JobApplicationResponse(BaseModel):
    id: int
    job_title: str
    company: str
    compensation_min: int
    compensation_max: Optional[int]
    compensation_type: CompensationType
    application_date: date
    job_posting_url: str
    resume_filename: str
    cover_letter_filename: Optional[str]
    status: JobStatus
    got_interview: bool
    coding_question_link: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    jobs: List[JobApplicationResponse]
    total: int

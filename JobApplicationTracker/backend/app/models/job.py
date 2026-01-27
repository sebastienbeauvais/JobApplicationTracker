from __future__ import annotations

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Integer, Date, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CompensationType(str, enum.Enum):
    HOURLY = "hourly"
    ANNUAL = "annual"


class JobStatus(str, enum.Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFER_RECEIVED = "offer_received"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Fields set on creation
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    company: Mapped[str] = mapped_column(String(50), nullable=False)
    compensation_min: Mapped[int] = mapped_column(Integer, nullable=False)
    compensation_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    compensation_type: Mapped[CompensationType] = mapped_column(
        Enum(CompensationType), nullable=False
    )
    application_date: Mapped[date] = mapped_column(Date, nullable=False)
    job_posting_url: Mapped[str] = mapped_column(String, nullable=False)
    resume_filename: Mapped[str] = mapped_column(String, nullable=False)
    cover_letter_filename: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Fields set post-creation (inline edit)
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus), nullable=False, default=JobStatus.APPLIED
    )
    got_interview: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    coding_question_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

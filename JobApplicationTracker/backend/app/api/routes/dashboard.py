from datetime import date, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.job import JobApplication, JobStatus
from app.schemas.dashboard import (
    DashboardResponse,
    StatusCount,
    ApplicationOverTime,
    RecentApplication,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard metrics."""
    # Total applications
    total = db.query(func.count(JobApplication.id)).scalar() or 0

    # Applications by status
    status_counts = (
        db.query(JobApplication.status, func.count(JobApplication.id))
        .group_by(JobApplication.status)
        .all()
    )

    applications_by_status = [
        StatusCount(status=status, count=count)
        for status, count in status_counts
    ]

    # Ensure all statuses are represented
    existing_statuses = {s.status for s in applications_by_status}
    for status in JobStatus:
        if status not in existing_statuses:
            applications_by_status.append(StatusCount(status=status, count=0))

    # Sort by status order
    status_order = list(JobStatus)
    applications_by_status.sort(key=lambda x: status_order.index(x.status))

    # Interview rate
    interview_count = (
        db.query(func.count(JobApplication.id))
        .filter(JobApplication.got_interview == True)
        .scalar() or 0
    )

    interview_rate = (interview_count / total * 100) if total > 0 else 0.0

    # Applications over time (last 30 days)
    thirty_days_ago = date.today() - timedelta(days=30)

    daily_counts = (
        db.query(JobApplication.application_date, func.count(JobApplication.id))
        .filter(JobApplication.application_date >= thirty_days_ago)
        .group_by(JobApplication.application_date)
        .all()
    )

    # Fill in missing dates with zero counts
    date_counts = {d: c for d, c in daily_counts}
    applications_over_time = []

    current_date = thirty_days_ago
    while current_date <= date.today():
        applications_over_time.append(
            ApplicationOverTime(
                date=current_date,
                count=date_counts.get(current_date, 0),
            )
        )
        current_date += timedelta(days=1)

    # Recent applications (last 10)
    recent_jobs = (
        db.query(JobApplication)
        .order_by(JobApplication.created_at.desc())
        .limit(10)
        .all()
    )

    recent_applications = [
        RecentApplication(
            id=job.id,
            job_title=job.job_title,
            company=job.company,
            status=job.status,
            application_date=job.application_date,
        )
        for job in recent_jobs
    ]

    return DashboardResponse(
        total_applications=total,
        applications_by_status=applications_by_status,
        interview_rate=round(interview_rate, 1),
        applications_over_time=applications_over_time,
        recent_applications=recent_applications,
    )

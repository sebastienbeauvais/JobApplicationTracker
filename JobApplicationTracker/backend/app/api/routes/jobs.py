from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import JobApplication
from app.schemas.job import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    JobListResponse,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobApplicationResponse, status_code=201)
def create_job(job_data: JobApplicationCreate, db: Session = Depends(get_db)):
    """Create a new job application."""
    job = JobApplication(
        job_title=job_data.job_title,
        company=job_data.company,
        compensation_min=job_data.compensation_min,
        compensation_max=job_data.compensation_max,
        compensation_type=job_data.compensation_type,
        application_date=job_data.application_date,
        job_posting_url=job_data.job_posting_url,
        resume_filename=job_data.resume_filename,
        cover_letter_filename=job_data.cover_letter_filename,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("", response_model=JobListResponse)
def list_jobs(db: Session = Depends(get_db)):
    """List all job applications."""
    jobs = db.query(JobApplication).order_by(JobApplication.created_at.desc()).all()
    return JobListResponse(jobs=jobs, total=len(jobs))


@router.get("/{job_id}", response_model=JobApplicationResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a single job application by ID."""
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job application not found")

    return job


@router.patch("/{job_id}", response_model=JobApplicationResponse)
def update_job(
    job_id: int,
    job_data: JobApplicationUpdate,
    db: Session = Depends(get_db),
):
    """Update a job application (status, interview, coding question)."""
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job application not found")

    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job

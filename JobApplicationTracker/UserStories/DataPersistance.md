# Title
Store jobs applied to

# Description
As a user, I want to ensure that the details I enter for jobs I have applied to are stored and retrieved from data storage.

# Acceptance Criteria
- Details written to Add a job are written to a storage location
- Details can be retrieved from the storage location
- Uploading a resume or cover letter while adding a job should not create a new document reference
    - That is to say, If I upload MyResume.pdf for job application A and I upload the same resume for job application B there should only be one instance of MyResume saved to some storage location for retrieval.
- Via the front end we should be able to update applications and the updates need to write to the data storage. Fields that can be updated are
    - Status (Accepted/Rejected)
    - Got Interview? (True/False)
    - Coding Question Given (Link to a github repo)

# Logic

## Database
- SQLite database for job application data
- SQLAlchemy ORM for database operations
- Alembic for database migrations

## Job Application Schema

### Fields Set on Creation (Add Job Form)
| Field | Type | Required |
|-------|------|----------|
| Job Title | String (100 chars) | Yes |
| Company | String (50 chars) | Yes |
| Compensation Min | Integer | Yes |
| Compensation Max | Integer | No |
| Compensation Type | Enum (hourly/annual) | Yes |
| Application Date | Date | Yes |
| Job Posting URL | String (valid URL) | Yes |
| Resume | File reference | Yes |
| Cover Letter | File reference | No |

### Fields Set Post-Creation (Inline Edit)
| Field | Type | Default | Required |
|-------|------|---------|----------|
| Status | Enum | "Applied" | Yes |
| Got Interview | Boolean | false | Yes |
| Coding Question Link | String (GitHub URL) | null | No |

### Status Enum Values
1. Applied (default on creation)
2. Interviewing
3. Offer Received
4. Accepted
5. Rejected
6. Withdrawn

## File Storage

### Resume & Cover Letter Storage
- **Actual files stored on server** (not just references)
- Files stored in dedicated upload directory
- **Deduplication by filename**: If "MyResume.pdf" is uploaded for multiple applications, only one physical file is stored
- Files can be retrieved and viewed from the frontend

### File Storage Structure
```
uploads/
├── resumes/
│   └── {filename}
└── cover_letters/
    └── {filename}
```

## API Endpoints (Backend)
- `POST /api/jobs` - Create new job application
- `GET /api/jobs` - List all job applications
- `GET /api/jobs/{id}` - Get single job application
- `PATCH /api/jobs/{id}` - Update job application (status, interview, coding question)
- `POST /api/uploads/resume` - Upload resume file
- `POST /api/uploads/cover-letter` - Upload cover letter file
- `GET /api/uploads/resumes` - List uploaded resumes
- `GET /api/uploads/cover-letters` - List uploaded cover letters
- `GET /api/uploads/resumes/{filename}` - Retrieve resume file
- `GET /api/uploads/cover-letters/{filename}` - Retrieve cover letter file

## Authentication
- Single user application - no authentication required
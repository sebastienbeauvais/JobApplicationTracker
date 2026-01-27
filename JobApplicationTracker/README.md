# Job Application Tracker

A full-stack web application for tracking job applications through the hiring process. Features a clean, Apple-inspired UI with dark mode support.

## Features

- **Dashboard** - View metrics including total applications, status breakdown, interview rate, and recent activity
- **Job Tracking** - Add and manage job applications with details like company, compensation, dates, and attached documents
- **File Management** - Upload and reuse resumes and cover letters across applications
- **Dark Mode** - Toggle between light and dark themes

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React 18, TypeScript, Vite, React Router
- **Testing:** pytest (backend), Vitest (frontend)

## Project Structure

```
JobApplicationTracker/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/routes/   # API route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── core/         # Config, database setup
│   ├── tests/            # Backend tests
│   └── pyproject.toml
├── frontend/             # React frontend
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── pages/        # Page components
│       ├── services/     # API client
│       ├── hooks/        # Custom React hooks
│       ├── context/      # React context providers
│       └── types/        # TypeScript type definitions
├── UserStories/          # Feature requirements
└── CLAUDE.md             # Claude Code instructions
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

### Running Both Services

To start both the backend and frontend with a single command, use the provided shell script:

```bash
./RunApp.sh
```

This script starts both servers in the background and logs output to `backend.log` and `frontend.log`.

> **Note:** If you receive a "Permission denied" error, make the script executable first:
> ```bash
> chmod +x RunApp.sh
> ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/jobs` | List all job applications |
| POST | `/api/jobs` | Create a new job application |
| GET | `/api/jobs/{id}` | Get a specific job application |
| PATCH | `/api/jobs/{id}` | Update a job application |
| GET | `/api/dashboard/stats` | Get dashboard statistics |
| POST | `/api/uploads` | Upload a file (resume/cover letter) |
| GET | `/api/uploads` | List uploaded files |

## Running Tests

### Backend
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

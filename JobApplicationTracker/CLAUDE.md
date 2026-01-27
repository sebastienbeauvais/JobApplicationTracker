# CLAUDE.md

This file provides guidance for Claude Code when working on this project.

## Project Overview

Job Application Tracker - A full-stack web application for tracking job applications through the hiring process. Features a clean, Apple-inspired UI with dark mode support.

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, SQLite, Pydantic 2.0
- **Frontend:** React 18, TypeScript, Vite, React Router 6
- **Testing:** pytest (backend), Vitest (frontend)

## Project Structure

- `backend/` - FastAPI application
  - `app/api/routes/` - API route handlers (jobs.py, uploads.py, dashboard.py)
  - `app/models/` - SQLAlchemy models
  - `app/schemas/` - Pydantic schemas for request/response validation
  - `app/core/` - Database setup and configuration
  - `tests/` - pytest test files
- `frontend/` - React TypeScript application
  - `src/pages/` - Page components (DashboardPage, AddJobPage, JobsListPage)
  - `src/components/` - Reusable UI components
  - `src/hooks/` - Custom React hooks (useJobs, useDashboard, useTheme)
  - `src/context/` - React context providers (ThemeContext)
  - `src/services/` - API client
  - `src/types/` - TypeScript type definitions
- `UserStories/` - Feature requirement markdown files

## Development Commands

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload    # Run dev server (port 8000)
pytest                            # Run tests
pip install -e ".[dev]"          # Install with dev dependencies
```

### Frontend
```bash
cd frontend
npm run dev      # Run dev server (port 3000)
npm run build    # Production build
npm run test     # Run tests
npm run lint     # Lint code
```

## User Stories

User stories are located in `UserStories/`. Each story file contains requirements for a feature:
- `Dashboard.md` - Dashboard metrics and visualizations
- `AddJobs.md` - Job application form and validation
- `DataPersistance.md` - Data storage requirements
- `Ui.md` - UI/UX design guidelines (Apple-inspired aesthetic)

When implementing a story:
1. Read the full story file first
2. Implement backend changes (models, schemas, routes)
3. Implement frontend changes (components, pages, API calls)
4. Write tests for new functionality

## Code Conventions

### Backend (Python)
- Use type hints for all function parameters and return types
- Pydantic models for request/response schemas in `app/schemas/`
- SQLAlchemy models in `app/models/`
- API routes organized by resource in `app/api/routes/`
- All routes prefixed with `/api`

### Frontend (TypeScript)
- Functional components with hooks
- Types defined in `src/types/`
- API calls in `src/services/api.ts`
- Custom hooks in `src/hooks/` for data fetching
- React Context for global state (theme)
- Reusable components in `src/components/`
- Page components in `src/pages/`

## Database

SQLite database stored at `backend/app.db`. Tables are auto-created on startup. Use Alembic for migrations when modifying existing schemas.

## API Structure

Routes are mounted at `/api`:
- `/api/jobs` - CRUD operations for job applications
- `/api/uploads` - File upload/list for resumes and cover letters
- `/api/dashboard/stats` - Dashboard statistics
- `/api/health` - Health check endpoint

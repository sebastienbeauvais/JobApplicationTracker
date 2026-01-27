import {
  JobApplication,
  JobApplicationCreate,
  JobApplicationUpdate,
  UploadedFile,
  DashboardData,
} from '../types/job';

const API_BASE = '/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'An error occurred');
  }
  return response.json();
}

// Jobs API
export async function fetchJobs(): Promise<JobApplication[]> {
  const response = await fetch(`${API_BASE}/jobs`);
  const data = await handleResponse<{ jobs: JobApplication[]; total: number }>(response);
  return data.jobs;
}

export async function fetchJob(id: number): Promise<JobApplication> {
  const response = await fetch(`${API_BASE}/jobs/${id}`);
  return handleResponse<JobApplication>(response);
}

export async function createJob(job: JobApplicationCreate): Promise<JobApplication> {
  const response = await fetch(`${API_BASE}/jobs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(job),
  });
  return handleResponse<JobApplication>(response);
}

export async function updateJob(id: number, update: JobApplicationUpdate): Promise<JobApplication> {
  const response = await fetch(`${API_BASE}/jobs/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(update),
  });
  return handleResponse<JobApplication>(response);
}

// Uploads API
export async function fetchResumes(): Promise<UploadedFile[]> {
  const response = await fetch(`${API_BASE}/uploads/resumes`);
  const data = await handleResponse<{ files: UploadedFile[]; total: number }>(response);
  return data.files;
}

export async function fetchCoverLetters(): Promise<UploadedFile[]> {
  const response = await fetch(`${API_BASE}/uploads/cover-letters`);
  const data = await handleResponse<{ files: UploadedFile[]; total: number }>(response);
  return data.files;
}

export async function uploadResume(file: File): Promise<UploadedFile> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/uploads/resume`, {
    method: 'POST',
    body: formData,
  });
  return handleResponse<UploadedFile>(response);
}

export async function uploadCoverLetter(file: File): Promise<UploadedFile> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/uploads/cover-letter`, {
    method: 'POST',
    body: formData,
  });
  return handleResponse<UploadedFile>(response);
}

export function getResumeUrl(filename: string): string {
  return `${API_BASE}/uploads/resumes/${encodeURIComponent(filename)}`;
}

export function getCoverLetterUrl(filename: string): string {
  return `${API_BASE}/uploads/cover-letters/${encodeURIComponent(filename)}`;
}

// Dashboard API
export async function fetchDashboard(): Promise<DashboardData> {
  const response = await fetch(`${API_BASE}/dashboard`);
  return handleResponse<DashboardData>(response);
}

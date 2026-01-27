export type CompensationType = 'hourly' | 'annual';

export type JobStatus =
  | 'applied'
  | 'interviewing'
  | 'offer_received'
  | 'accepted'
  | 'rejected'
  | 'withdrawn';

export interface JobApplication {
  id: number;
  job_title: string;
  company: string;
  compensation_min: number;
  compensation_max?: number;
  compensation_type: CompensationType;
  application_date: string;
  job_posting_url: string;
  resume_filename: string;
  cover_letter_filename?: string;
  status: JobStatus;
  got_interview: boolean;
  coding_question_link?: string;
  created_at: string;
  updated_at: string;
}

export interface JobApplicationCreate {
  job_title: string;
  company: string;
  compensation_min: number;
  compensation_max?: number;
  compensation_type: CompensationType;
  application_date: string;
  job_posting_url: string;
  resume_filename: string;
  cover_letter_filename?: string;
}

export interface JobApplicationUpdate {
  status?: JobStatus;
  got_interview?: boolean;
  coding_question_link?: string;
}

export interface JobFormData {
  jobTitle: string;
  company: string;
  compensationMin: string;
  compensationMax: string;
  compensationType: CompensationType;
  applicationDate: string;
  jobPostingUrl: string;
  resumeFilename: string;
  coverLetterFilename: string;
}

export interface UploadedFile {
  id: number;
  filename: string;
  file_type: 'resume' | 'cover_letter';
  original_filename: string;
  content_type: string;
  file_size: number;
  uploaded_at: string;
}

export interface StatusCount {
  status: JobStatus;
  count: number;
}

export interface ApplicationOverTime {
  date: string;
  count: number;
}

export interface RecentApplication {
  id: number;
  job_title: string;
  company: string;
  status: JobStatus;
  application_date: string;
}

export interface DashboardData {
  total_applications: number;
  applications_by_status: StatusCount[];
  interview_rate: number;
  applications_over_time: ApplicationOverTime[];
  recent_applications: RecentApplication[];
}

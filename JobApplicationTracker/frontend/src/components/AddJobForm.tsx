import { useState, FormEvent } from 'react';
import {
  JobFormData,
  JobApplicationCreate,
  CompensationType,
  UploadedFile,
} from '../types/job';
import { FileUploadSelect } from './FileUploadSelect';

interface FormErrors {
  jobTitle?: string;
  company?: string;
  compensationMin?: string;
  compensationMax?: string;
  applicationDate?: string;
  jobPostingUrl?: string;
  resumeFilename?: string;
}

interface AddJobFormProps {
  resumes: UploadedFile[];
  coverLetters: UploadedFile[];
  onSubmit: (job: JobApplicationCreate) => Promise<void>;
  onResumeUpload: (file: File) => Promise<UploadedFile>;
  onCoverLetterUpload: (file: File) => Promise<UploadedFile>;
}

const initialFormData: JobFormData = {
  jobTitle: '',
  company: '',
  compensationMin: '',
  compensationMax: '',
  compensationType: 'annual',
  applicationDate: '',
  jobPostingUrl: '',
  resumeFilename: '',
  coverLetterFilename: '',
};

function isValidUrl(urlString: string): boolean {
  try {
    const url = new URL(urlString);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch {
    return false;
  }
}

function getTodayString(): string {
  return new Date().toISOString().split('T')[0];
}

export function AddJobForm({
  resumes,
  coverLetters,
  onSubmit,
  onResumeUpload,
  onCoverLetterUpload,
}: AddJobFormProps) {
  const [formData, setFormData] = useState<JobFormData>(initialFormData);
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitting, setSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.jobTitle.trim()) {
      newErrors.jobTitle = 'Job title is required';
    } else if (formData.jobTitle.length > 100) {
      newErrors.jobTitle = 'Job title must be 100 characters or less';
    }

    if (!formData.company.trim()) {
      newErrors.company = 'Company is required';
    } else if (formData.company.length > 50) {
      newErrors.company = 'Company must be 50 characters or less';
    }

    if (!formData.compensationMin.trim()) {
      newErrors.compensationMin = 'Minimum compensation is required';
    } else if (isNaN(Number(formData.compensationMin)) || Number(formData.compensationMin) < 0) {
      newErrors.compensationMin = 'Please enter a valid positive number';
    }

    if (formData.compensationMax.trim()) {
      const max = Number(formData.compensationMax);
      const min = Number(formData.compensationMin);
      if (isNaN(max) || max < 0) {
        newErrors.compensationMax = 'Please enter a valid positive number';
      } else if (max < min) {
        newErrors.compensationMax = 'Maximum must be greater than or equal to minimum';
      }
    }

    if (!formData.applicationDate) {
      newErrors.applicationDate = 'Application date is required';
    } else if (formData.applicationDate > getTodayString()) {
      newErrors.applicationDate = 'Application date cannot be in the future';
    }

    if (!formData.jobPostingUrl.trim()) {
      newErrors.jobPostingUrl = 'Job posting URL is required';
    } else if (!isValidUrl(formData.jobPostingUrl)) {
      newErrors.jobPostingUrl = 'Please enter a valid URL (e.g., https://example.com)';
    }

    if (!formData.resumeFilename) {
      newErrors.resumeFilename = 'Resume is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const jobData: JobApplicationCreate = {
      job_title: formData.jobTitle.trim(),
      company: formData.company.trim(),
      compensation_min: Number(formData.compensationMin),
      compensation_max: formData.compensationMax.trim()
        ? Number(formData.compensationMax)
        : undefined,
      compensation_type: formData.compensationType,
      application_date: formData.applicationDate,
      job_posting_url: formData.jobPostingUrl.trim(),
      resume_filename: formData.resumeFilename,
      cover_letter_filename: formData.coverLetterFilename || undefined,
    };

    try {
      setSubmitting(true);
      await onSubmit(jobData);
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (
    field: keyof JobFormData,
    value: string | CompensationType
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-job-form">
      <div className="form-group">
        <label htmlFor="jobTitle" className="form-label">
          Job Title<span className="required">*</span>
        </label>
        <input
          id="jobTitle"
          type="text"
          value={formData.jobTitle}
          onChange={(e) => handleInputChange('jobTitle', e.target.value)}
          maxLength={100}
          className={`form-input ${errors.jobTitle ? 'input-error' : ''}`}
          placeholder="e.g., Senior Software Engineer"
          disabled={submitting}
        />
        <div className="input-hint">{formData.jobTitle.length}/100 characters</div>
        {errors.jobTitle && <span className="error-message">{errors.jobTitle}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="company" className="form-label">
          Company<span className="required">*</span>
        </label>
        <input
          id="company"
          type="text"
          value={formData.company}
          onChange={(e) => handleInputChange('company', e.target.value)}
          maxLength={50}
          className={`form-input ${errors.company ? 'input-error' : ''}`}
          placeholder="e.g., Acme Corp"
          disabled={submitting}
        />
        <div className="input-hint">{formData.company.length}/50 characters</div>
        {errors.company && <span className="error-message">{errors.company}</span>}
      </div>

      <div className="form-group">
        <label className="form-label">
          Estimated Compensation (USD)<span className="required">*</span>
        </label>
        <div className="compensation-group">
          <div className="compensation-type">
            <label className="radio-label">
              <input
                type="radio"
                name="compensationType"
                value="annual"
                checked={formData.compensationType === 'annual'}
                onChange={(e) =>
                  handleInputChange('compensationType', e.target.value as CompensationType)
                }
                disabled={submitting}
              />
              Annual
            </label>
            <label className="radio-label">
              <input
                type="radio"
                name="compensationType"
                value="hourly"
                checked={formData.compensationType === 'hourly'}
                onChange={(e) =>
                  handleInputChange('compensationType', e.target.value as CompensationType)
                }
                disabled={submitting}
              />
              Hourly
            </label>
          </div>
          <div className="compensation-inputs">
            <div className="compensation-field">
              <label htmlFor="compensationMin" className="form-label-small">
                Minimum<span className="required">*</span>
              </label>
              <div className="input-with-prefix">
                <span className="input-prefix">$</span>
                <input
                  id="compensationMin"
                  type="number"
                  min="0"
                  value={formData.compensationMin}
                  onChange={(e) => handleInputChange('compensationMin', e.target.value)}
                  className={`form-input ${errors.compensationMin ? 'input-error' : ''}`}
                  placeholder="0"
                  disabled={submitting}
                />
              </div>
              {errors.compensationMin && (
                <span className="error-message">{errors.compensationMin}</span>
              )}
            </div>
            <div className="compensation-field">
              <label htmlFor="compensationMax" className="form-label-small">
                Maximum (optional)
              </label>
              <div className="input-with-prefix">
                <span className="input-prefix">$</span>
                <input
                  id="compensationMax"
                  type="number"
                  min="0"
                  value={formData.compensationMax}
                  onChange={(e) => handleInputChange('compensationMax', e.target.value)}
                  className={`form-input ${errors.compensationMax ? 'input-error' : ''}`}
                  placeholder="0"
                  disabled={submitting}
                />
              </div>
              {errors.compensationMax && (
                <span className="error-message">{errors.compensationMax}</span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="applicationDate" className="form-label">
          Application Date<span className="required">*</span>
        </label>
        <input
          id="applicationDate"
          type="date"
          value={formData.applicationDate}
          onChange={(e) => handleInputChange('applicationDate', e.target.value)}
          max={getTodayString()}
          className={`form-input ${errors.applicationDate ? 'input-error' : ''}`}
          disabled={submitting}
        />
        {errors.applicationDate && (
          <span className="error-message">{errors.applicationDate}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="jobPostingUrl" className="form-label">
          Job Posting URL<span className="required">*</span>
        </label>
        <input
          id="jobPostingUrl"
          type="url"
          value={formData.jobPostingUrl}
          onChange={(e) => handleInputChange('jobPostingUrl', e.target.value)}
          className={`form-input ${errors.jobPostingUrl ? 'input-error' : ''}`}
          placeholder="https://example.com/job-posting"
          disabled={submitting}
        />
        {errors.jobPostingUrl && (
          <span className="error-message">{errors.jobPostingUrl}</span>
        )}
      </div>

      <FileUploadSelect
        label="Resume"
        value={formData.resumeFilename}
        onChange={(filename) => handleInputChange('resumeFilename', filename)}
        onFileUpload={onResumeUpload}
        uploadedFiles={resumes}
        required
        error={errors.resumeFilename}
      />

      <FileUploadSelect
        label="Cover Letter"
        value={formData.coverLetterFilename}
        onChange={(filename) => handleInputChange('coverLetterFilename', filename)}
        onFileUpload={onCoverLetterUpload}
        uploadedFiles={coverLetters}
      />

      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Adding...' : 'Add Job Application'}
        </button>
      </div>
    </form>
  );
}

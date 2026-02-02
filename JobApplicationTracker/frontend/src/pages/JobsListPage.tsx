import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useJobs } from '../hooks/useJobs';
import { JobApplication, JobStatus, JobApplicationUpdate } from '../types/job';

const STATUS_OPTIONS: { value: JobStatus; label: string }[] = [
  { value: 'applied', label: 'Applied' },
  { value: 'interviewing', label: 'Interviewing' },
  { value: 'offer_received', label: 'Offer Received' },
  { value: 'accepted', label: 'Accepted' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'withdrawn', label: 'Withdrawn' },
];

const STATUS_COLORS: Record<JobStatus, string> = {
  applied: 'status-applied',
  interviewing: 'status-interviewing',
  offer_received: 'status-offer',
  accepted: 'status-accepted',
  rejected: 'status-rejected',
  withdrawn: 'status-withdrawn',
};

function formatCompensation(
  min: number,
  max: number | undefined,
  type: 'hourly' | 'annual'
): string {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  });

  const suffix = type === 'hourly' ? '/hr' : '/yr';

  if (max && max !== min) {
    return `${formatter.format(min)} - ${formatter.format(max)}${suffix}`;
  }
  return `${formatter.format(min)}${suffix}`;
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

interface JobRowProps {
  job: JobApplication;
  onUpdate: (id: number, update: JobApplicationUpdate) => Promise<void>;
}

function JobRow({ job, onUpdate }: JobRowProps) {
  const [updating, setUpdating] = useState(false);
  const [codingLink, setCodingLink] = useState(job.coding_question_link || '');
  const [editingLink, setEditingLink] = useState(false);

  const handleStatusChange = async (status: JobStatus) => {
    setUpdating(true);
    try {
      await onUpdate(job.id, { status });
    } finally {
      setUpdating(false);
    }
  };

  const handleInterviewToggle = async () => {
    setUpdating(true);
    try {
      await onUpdate(job.id, { got_interview: !job.got_interview });
    } finally {
      setUpdating(false);
    }
  };

  const handleLinkSave = async () => {
    setUpdating(true);
    try {
      await onUpdate(job.id, { coding_question_link: codingLink || undefined });
      setEditingLink(false);
    } finally {
      setUpdating(false);
    }
  };

  return (
    <tr className={updating ? 'updating' : ''}>
      <td className="job-title-cell">{job.job_title}</td>
      <td>{job.company}</td>
      <td>
        {formatCompensation(
          job.compensation_min,
          job.compensation_max,
          job.compensation_type
        )}
      </td>
      <td>{job.application_date}</td>
      <td>
        <select
          value={job.status}
          onChange={(e) => handleStatusChange(e.target.value as JobStatus)}
          className={`status-select ${STATUS_COLORS[job.status]}`}
          disabled={updating}
        >
          {STATUS_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </td>
      <td>
        <label className="toggle-label">
          <input
            type="checkbox"
            checked={job.got_interview}
            onChange={handleInterviewToggle}
            disabled={updating}
          />
          <span className="toggle-text">{job.got_interview ? 'Yes' : 'No'}</span>
        </label>
      </td>
      <td>
        {editingLink ? (
          <div className="inline-edit">
            <input
              type="url"
              value={codingLink}
              onChange={(e) => setCodingLink(e.target.value)}
              placeholder="https://github.com/..."
              className="form-input form-input-small"
            />
            <button
              onClick={handleLinkSave}
              className="btn btn-small btn-primary"
              disabled={updating}
            >
              Save
            </button>
            <button
              onClick={() => {
                setCodingLink(job.coding_question_link || '');
                setEditingLink(false);
              }}
              className="btn btn-small btn-secondary"
            >
              Cancel
            </button>
          </div>
        ) : (
          <div className="link-cell">
            {job.coding_question_link ? (
              <a
                href={job.coding_question_link}
                target="_blank"
                rel="noopener noreferrer"
                className="link"
              >
                View
              </a>
            ) : (
              <span className="text-muted">-</span>
            )}
            <button
              onClick={() => setEditingLink(true)}
              className="btn btn-small btn-text"
            >
              Edit
            </button>
          </div>
        )}
      </td>
      <td>
        <a
          href={job.job_posting_url}
          target="_blank"
          rel="noopener noreferrer"
          className="link"
        >
          View
        </a>
      </td>
    </tr>
  );
}

export function JobsListPage() {
  const { jobs, loading, error, updateJob } = useJobs();

  const handleUpdate = async (id: number, update: JobApplicationUpdate) => {
    await updateJob(id, update);
  };

  if (loading) {
    return (
      <div className="page jobs-list-page">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="page jobs-list-page">
      <div className="page-header">
        <h1>My Job Applications</h1>
        <Link to="/add-job" className="btn btn-primary">
          + Add New Application
        </Link>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {jobs.length === 0 ? (
        <div className="empty-state">
          <p>You haven't tracked any job applications yet.</p>
          <Link to="/add-job" className="btn btn-primary">
            Add Your First Application
          </Link>
        </div>
      ) : (
        <div className="jobs-table-container">
          <table className="jobs-table">
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Company</th>
                <th>Compensation</th>
                <th>Applied On</th>
                <th>Status</th>
                <th>Interview</th>
                <th>Coding Question</th>
                <th>Posting</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <JobRow key={job.id} job={job} onUpdate={handleUpdate} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AddJobForm } from '../components/AddJobForm';
import { useJobs } from '../hooks/useJobs';
import { JobApplicationCreate } from '../types/job';

export function AddJobPage() {
  const navigate = useNavigate();
  const { resumes, coverLetters, loading, error, addJob, uploadResume, uploadCoverLetter } =
    useJobs();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const handleSubmit = async (jobData: JobApplicationCreate) => {
    try {
      setSubmitError(null);
      await addJob(jobData);
      setSuccessMessage('Job application added successfully!');

      setTimeout(() => {
        navigate('/jobs');
      }, 1500);
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Failed to add job');
    }
  };

  if (loading) {
    return (
      <div className="page add-job-page">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="page add-job-page">
      <div className="page-header">
        <h1>Add Job Application</h1>
        <p className="page-description">
          Track a new job application by filling out the details below.
        </p>
      </div>

      {successMessage && <div className="alert alert-success">{successMessage}</div>}

      {(error || submitError) && (
        <div className="alert alert-error">{error || submitError}</div>
      )}

      <div className="page-content">
        <AddJobForm
          resumes={resumes}
          coverLetters={coverLetters}
          onSubmit={handleSubmit}
          onResumeUpload={uploadResume}
          onCoverLetterUpload={uploadCoverLetter}
        />
      </div>
    </div>
  );
}

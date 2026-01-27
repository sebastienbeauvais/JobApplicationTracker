import { useState, useEffect, useCallback } from 'react';
import {
  JobApplication,
  JobApplicationCreate,
  JobApplicationUpdate,
  UploadedFile,
} from '../types/job';
import * as api from '../services/api';

export function useJobs() {
  const [jobs, setJobs] = useState<JobApplication[]>([]);
  const [resumes, setResumes] = useState<UploadedFile[]>([]);
  const [coverLetters, setCoverLetters] = useState<UploadedFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [jobsData, resumesData, coverLettersData] = await Promise.all([
        api.fetchJobs(),
        api.fetchResumes(),
        api.fetchCoverLetters(),
      ]);
      setJobs(jobsData);
      setResumes(resumesData);
      setCoverLetters(coverLettersData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const addJob = async (jobData: JobApplicationCreate): Promise<JobApplication> => {
    const newJob = await api.createJob(jobData);
    setJobs((prev) => [newJob, ...prev]);
    return newJob;
  };

  const updateJob = async (
    id: number,
    update: JobApplicationUpdate
  ): Promise<JobApplication> => {
    const updatedJob = await api.updateJob(id, update);
    setJobs((prev) =>
      prev.map((job) => (job.id === id ? updatedJob : job))
    );
    return updatedJob;
  };

  const uploadResume = async (file: File): Promise<UploadedFile> => {
    const uploaded = await api.uploadResume(file);
    // Check if already in list (deduplication)
    if (!resumes.find((r) => r.filename === uploaded.filename)) {
      setResumes((prev) => [uploaded, ...prev]);
    }
    return uploaded;
  };

  const uploadCoverLetter = async (file: File): Promise<UploadedFile> => {
    const uploaded = await api.uploadCoverLetter(file);
    // Check if already in list (deduplication)
    if (!coverLetters.find((c) => c.filename === uploaded.filename)) {
      setCoverLetters((prev) => [uploaded, ...prev]);
    }
    return uploaded;
  };

  return {
    jobs,
    resumes,
    coverLetters,
    loading,
    error,
    addJob,
    updateJob,
    uploadResume,
    uploadCoverLetter,
    refresh: loadData,
  };
}

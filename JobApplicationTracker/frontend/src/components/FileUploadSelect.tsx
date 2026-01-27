import { useRef, useState, ChangeEvent } from 'react';
import { UploadedFile } from '../types/job';

interface FileUploadSelectProps {
  label: string;
  value: string;
  onChange: (filename: string) => void;
  onFileUpload: (file: File) => Promise<UploadedFile>;
  uploadedFiles: UploadedFile[];
  required?: boolean;
  accept?: string;
  error?: string;
}

export function FileUploadSelect({
  label,
  value,
  onChange,
  onFileUpload,
  uploadedFiles,
  required = false,
  accept = '.pdf,.doc,.docx',
  error,
}: FileUploadSelectProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const handleFileChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        setUploading(true);
        setUploadError(null);
        const uploaded = await onFileUpload(file);
        onChange(uploaded.filename);
      } catch (err) {
        setUploadError(err instanceof Error ? err.message : 'Upload failed');
      } finally {
        setUploading(false);
      }
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {
    onChange(e.target.value);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="form-group">
      <label className="form-label">
        {label}
        {required && <span className="required">*</span>}
      </label>
      <div className="file-upload-select">
        <select
          value={value}
          onChange={handleSelectChange}
          className={`form-select ${error ? 'input-error' : ''}`}
          disabled={uploading}
        >
          <option value="">
            {uploadedFiles.length > 0
              ? '-- Select from uploaded files --'
              : '-- No files uploaded yet --'}
          </option>
          {uploadedFiles.map((file) => (
            <option key={file.filename} value={file.filename}>
              {file.filename}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={handleUploadClick}
          className="btn btn-secondary"
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Upload New'}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          onChange={handleFileChange}
          className="hidden-file-input"
        />
      </div>
      {(error || uploadError) && (
        <span className="error-message">{error || uploadError}</span>
      )}
    </div>
  );
}

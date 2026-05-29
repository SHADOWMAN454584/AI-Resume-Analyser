import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './FileUpload.css';

export default function FileUpload({ onFileSelect, uploading, progress }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) return;
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      if (onFileSelect) onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    disabled: uploading,
  });

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const removeFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
  };

  return (
    <div className="file-upload-wrapper">
      <div
        {...getRootProps()}
        className={`file-dropzone ${isDragActive ? 'dropzone-active' : ''} ${isDragReject ? 'dropzone-reject' : ''} ${uploading ? 'dropzone-uploading' : ''} ${selectedFile ? 'dropzone-has-file' : ''}`}
      >
        <input {...getInputProps()} />

        {uploading ? (
          <div className="upload-progress-container">
            <div className="upload-spinner">
              <div className="spinner"></div>
            </div>
            <p className="upload-status-text">Uploading & Analyzing...</p>
            <div className="upload-progress-bar">
              <div className="upload-progress-fill" style={{ width: `${progress || 0}%` }}></div>
            </div>
            <span className="upload-progress-pct">{progress || 0}%</span>
          </div>
        ) : selectedFile ? (
          <div className="file-preview">
            <div className="file-preview-icon">📄</div>
            <div className="file-preview-info">
              <p className="file-preview-name">{selectedFile.name}</p>
              <p className="file-preview-size">{formatSize(selectedFile.size)}</p>
            </div>
            <button className="file-remove-btn" onClick={removeFile} title="Remove file">✕</button>
          </div>
        ) : (
          <div className="dropzone-content">
            <div className="dropzone-icon">
              {isDragActive ? '📥' : '📄'}
            </div>
            <p className="dropzone-title">
              {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
            </p>
            <p className="dropzone-subtitle">
              or <span className="dropzone-browse">browse files</span>
            </p>
            <p className="dropzone-hint">PDF files only, up to 10MB</p>
          </div>
        )}
      </div>
    </div>
  );
}

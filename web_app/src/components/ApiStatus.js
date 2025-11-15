import React from 'react';

const ApiStatus = ({ status, onRefresh }) => {
  if (!status) {
    return (
      <div className="text-end">
        <span className="badge bg-secondary">
          <i className="fas fa-question-circle me-2"></i>
          Checking...
        </span>
      </div>
    );
  }

  const isOnline = status.status === 'healthy';
  const modelLoaded = status.model_loaded;

  return (
    <div className="text-end">
      <div className="d-flex justify-content-end align-items-center gap-2 flex-wrap">
        {/* API Status */}
        <span className={`badge ${isOnline ? 'bg-success' : 'bg-danger'}`}>
          <i className={`fas ${isOnline ? 'fa-check-circle' : 'fa-times-circle'} me-2`}></i>
          API {isOnline ? 'Online' : 'Offline'}
        </span>

        {/* Model Status */}
        {isOnline && (
          <span className={`badge ${modelLoaded ? 'bg-success' : 'bg-warning text-dark'}`}>
            <i className={`fas ${modelLoaded ? 'fa-brain' : 'fa-exclamation-triangle'} me-2`}></i>
            Model {modelLoaded ? 'Ready' : 'Not Loaded'}
          </span>
        )}

        {/* Refresh Button */}
        <button
          className="btn btn-outline-light btn-sm"
          onClick={onRefresh}
          title="Refresh API Status"
        >
          <i className="fas fa-sync-alt"></i>
        </button>
      </div>

      {/* Additional Info */}
      {status.timestamp && (
        <small className="text-light opacity-75 d-block mt-1">
          Last checked: {new Date(status.timestamp).toLocaleTimeString()}
        </small>
      )}

      {/* Error Message */}
      {!isOnline && (
        <small className="text-warning d-block mt-1">
          <i className="fas fa-exclamation-triangle me-1"></i>
          Make sure API server is running on port 5000
        </small>
      )}

      {/* Model Warning */}
      {isOnline && !modelLoaded && (
        <small className="text-warning d-block mt-1">
          <i className="fas fa-info-circle me-1"></i>
          Run 'python train.py' to train the model
        </small>
      )}
    </div>
  );
};

export default ApiStatus;
import React from 'react';

const ResultDisplay = ({ result }) => {
  if (!result || !result.success) {
    return null;
  }

  const { prediction, input_data, metadata } = result;
  const { is_phishing, confidence, label, risk_level } = prediction;

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'HIGH':
        return 'danger';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'info';
      case 'SAFE':
        return 'success';
      default:
        return 'secondary';
    }
  };

  const getConfidenceColor = (conf) => {
    if (conf >= 90) return 'success';
    if (conf >= 70) return 'warning';
    return 'danger';
  };

  const getIcon = (isPhishing) => {
    return isPhishing ? 'fas fa-exclamation-triangle' : 'fas fa-shield-check';
  };

  return (
    <div className="result-animation mt-4">
      {/* Main Result Card */}
      <div className={`alert alert-${getRiskColor(risk_level)} result-card`}>
        <div className="row align-items-center">
          <div className="col-md-8">
            <h4 className="alert-heading mb-2">
              <i className={`${getIcon(is_phishing)} me-3`}></i>
              {label} Email
            </h4>
            <p className="mb-0">
              {is_phishing 
                ? "⚠️ This email shows characteristics of a phishing attempt"
                : "✅ This email appears to be legitimate"
              }
            </p>
          </div>
          <div className="col-md-4 text-md-end">
            <span className={`badge bg-${getRiskColor(risk_level)} risk-badge`}>
              {risk_level} RISK
            </span>
          </div>
        </div>
      </div>

      {/* Detailed Analysis */}
      <div className="card mt-3">
        <div className="card-header">
          <h5 className="mb-0">
            <i className="fas fa-chart-line me-2"></i>
            Detailed Analysis
          </h5>
        </div>
        <div className="card-body">
          <div className="row">
            {/* Confidence Score */}
            <div className="col-md-6 mb-3">
              <label className="form-label fw-bold">Confidence Score</label>
              <div className="confidence-meter">
                <div 
                  className={`progress-bar bg-${getConfidenceColor(confidence)}`}
                  style={{ width: `${confidence}%` }}
                ></div>
              </div>
              <div className="d-flex justify-content-between small text-muted">
                <span>0%</span>
                <span className="fw-bold">{confidence.toFixed(1)}%</span>
                <span>100%</span>
              </div>
            </div>

            {/* Risk Assessment */}
            <div className="col-md-6 mb-3">
              <label className="form-label fw-bold">Risk Assessment</label>
              <div className="mt-2">
                <span className={`badge bg-${getRiskColor(risk_level)} risk-badge`}>
                  <i className="fas fa-shield-alt me-2"></i>
                  {risk_level} RISK
                </span>
              </div>
              <small className="text-muted d-block mt-1">
                {risk_level === 'HIGH' && 'Immediate attention required'}
                {risk_level === 'MEDIUM' && 'Exercise caution'}
                {risk_level === 'LOW' && 'Low threat detected'}
                {risk_level === 'SAFE' && 'No threat detected'}
              </small>
            </div>
          </div>

          {/* Analysis Details */}
          <div className="row mt-3">
            <div className="col-12">
              <h6 className="fw-bold">Analysis Summary:</h6>
              <div className="row">
                <div className="col-md-4 mb-2">
                  <small className="text-muted">Classification:</small>
                  <div className="fw-bold">{label}</div>
                </div>
                <div className="col-md-4 mb-2">
                  <small className="text-muted">Features Analyzed:</small>
                  <div className="fw-bold">{metadata.feature_count}</div>
                </div>
                <div className="col-md-4 mb-2">
                  <small className="text-muted">Model Version:</small>
                  <div className="fw-bold">{metadata.model_version}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Input Summary */}
          <div className="mt-4 p-3 bg-light rounded">
            <h6 className="fw-bold mb-3">
              <i className="fas fa-info-circle me-2"></i>
              Analyzed Content:
            </h6>
            <div className="row">
              <div className="col-md-6 mb-2">
                <small className="text-muted">Subject:</small>
                <div className="small">{input_data.subject || <em>No subject provided</em>}</div>
              </div>
              <div className="col-md-6 mb-2">
                <small className="text-muted">Sender:</small>
                <div className="small">{input_data.sender || <em>No sender provided</em>}</div>
              </div>
              <div className="col-12 mt-2">
                <small className="text-muted">Content Preview:</small>
                <div className="small font-monospace bg-white p-2 rounded border">
                  {input_data.email_text}
                </div>
              </div>
            </div>
          </div>

          {/* Action Recommendations */}
          <div className="mt-4">
            <h6 className="fw-bold">
              <i className="fas fa-lightbulb me-2"></i>
              Recommendations:
            </h6>
            {is_phishing ? (
              <ul className="list-unstyled">
                <li className="text-danger mb-1">
                  <i className="fas fa-times-circle me-2"></i>
                  Do not click any links in this email
                </li>
                <li className="text-danger mb-1">
                  <i className="fas fa-times-circle me-2"></i>
                  Do not provide personal information
                </li>
                <li className="text-warning mb-1">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  Verify sender through alternative means
                </li>
                <li className="text-info mb-1">
                  <i className="fas fa-flag me-2"></i>
                  Report this email as spam/phishing
                </li>
              </ul>
            ) : (
              <ul className="list-unstyled">
                <li className="text-success mb-1">
                  <i className="fas fa-check-circle me-2"></i>
                  Email appears safe to read
                </li>
                <li className="text-info mb-1">
                  <i className="fas fa-eye me-2"></i>
                  Still verify links before clicking
                </li>
                <li className="text-info mb-1">
                  <i className="fas fa-shield-alt me-2"></i>
                  Trust your instincts if something feels off
                </li>
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
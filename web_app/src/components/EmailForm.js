import React, { useState } from 'react';

const EmailForm = ({ onSubmit, loading, onExampleSelect }) => {
  const [emailText, setEmailText] = useState('');
  const [subject, setSubject] = useState('');
  const [sender, setSender] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!emailText.trim()) {
      alert('Please enter email content to analyze');
      return;
    }

    onSubmit({
      email_text: emailText,
      subject: subject,
      sender: sender
    });
  };

  const handleClear = () => {
    setEmailText('');
    setSubject('');
    setSender('');
  };

  const fillExample = (example) => {
    setEmailText(example.email_text);
    setSubject(example.subject);
    setSender(example.sender);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Email Content */}
      <div className="mb-3">
        <label htmlFor="emailText" className="form-label">
          <i className="fas fa-envelope me-2"></i>
          Email Content *
        </label>
        <textarea
          id="emailText"
          className="form-control"
          rows="6"
          value={emailText}
          onChange={(e) => setEmailText(e.target.value)}
          placeholder="Paste the email content here to analyze for phishing indicators..."
          required
        />
        <div className="form-text">
          The main body content of the email you want to analyze
        </div>
      </div>

      {/* Subject */}
      <div className="mb-3">
        <label htmlFor="subject" className="form-label">
          <i className="fas fa-tag me-2"></i>
          Email Subject (Optional)
        </label>
        <input
          type="text"
          id="subject"
          className="form-control"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Email subject line..."
        />
      </div>

      {/* Sender */}
      <div className="mb-3">
        <label htmlFor="sender" className="form-label">
          <i className="fas fa-user me-2"></i>
          Sender Email (Optional)
        </label>
        <input
          type="email"
          id="sender"
          className="form-control"
          value={sender}
          onChange={(e) => setSender(e.target.value)}
          placeholder="sender@example.com"
        />
      </div>

      {/* Buttons */}
      <div className="d-flex gap-2 flex-wrap">
        <button
          type="submit"
          className="btn btn-primary btn-analyze flex-grow-1"
          disabled={loading || !emailText.trim()}
        >
          {loading ? (
            <>
              <i className="fas fa-spinner fa-spin me-2"></i>
              Analyzing...
            </>
          ) : (
            <>
              <i className="fas fa-search me-2"></i>
              Analyze Email
            </>
          )}
        </button>
        
        <button
          type="button"
          className="btn btn-outline-secondary"
          onClick={handleClear}
          disabled={loading}
        >
          <i className="fas fa-eraser me-2"></i>
          Clear
        </button>
      </div>

      {/* Quick Examples */}
      <div className="mt-4">
        <h6 className="text-muted mb-3">
          <i className="fas fa-zap me-2"></i>
          Quick Test Examples:
        </h6>
        <div className="row">
          <div className="col-md-6 mb-2">
            <button
              type="button"
              className="btn btn-outline-danger btn-sm w-100"
              onClick={() => fillExample({
                email_text: "URGENT! Your account has been compromised. Click here to secure it immediately!",
                subject: "Account Security Alert",
                sender: "security@fake-bank.net"
              })}
              disabled={loading}
            >
              <i className="fas fa-exclamation-triangle me-1"></i>
              Test Phishing Email
            </button>
          </div>
          <div className="col-md-6 mb-2">
            <button
              type="button"
              className="btn btn-outline-success btn-sm w-100"
              onClick={() => fillExample({
                email_text: "Meeting reminder for tomorrow at 2 PM in conference room A. Please bring your quarterly reports.",
                subject: "Team Meeting Tomorrow",
                sender: "sarah.johnson@company.com"
              })}
              disabled={loading}
            >
              <i className="fas fa-check-circle me-1"></i>
              Test Safe Email
            </button>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="alert alert-info mt-3">
        <h6 className="alert-heading">
          <i className="fas fa-info-circle me-2"></i>
          How to Use:
        </h6>
        <ul className="mb-0 small">
          <li>Paste any email content into the text area above</li>
          <li>Add the subject and sender for better accuracy (optional)</li>
          <li>Click "Analyze Email" to get instant phishing detection results</li>
          <li>Use the example buttons for quick testing</li>
        </ul>
      </div>
    </form>
  );
};

export default EmailForm;
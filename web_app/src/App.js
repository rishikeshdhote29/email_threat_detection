import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EmailForm from './components/EmailForm';
import ResultDisplay from './components/ResultDisplay';
import ExampleEmails from './components/ExampleEmails';
import ApiStatus from './components/ApiStatus';
import './App.css';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [apiStatus, setApiStatus] = useState(null);

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setApiStatus(response.data);
    } catch (err) {
      setApiStatus({ status: 'offline', model_loaded: false });
    }
  };

  const analyzeEmail = async (emailData) => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, emailData);
      
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'Analysis failed');
      }
    } catch (err) {
      if (err.response) {
        setError(err.response.data.error || 'Server error occurred');
      } else if (err.request) {
        setError('Cannot connect to API server. Make sure the API is running on http://localhost:5000');
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExampleSelect = (example) => {
    // This will be passed to EmailForm to populate fields
    return example;
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="gradient-bg py-4 mb-4">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h1 className="mb-1">
                <i className="fas fa-shield-alt me-3"></i>
                Email Phishing Detector
              </h1>
              <p className="mb-0 opacity-75">
                Protect yourself from phishing attacks with AI-powered email analysis
              </p>
            </div>
            <div className="col-md-4">
              <ApiStatus status={apiStatus} onRefresh={checkApiStatus} />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container main-container">
        <div className="row">
          {/* Email Analysis Form */}
          <div className="col-lg-8 mb-4">
            <div className="card">
              <div className="card-header bg-primary text-white">
                <h3 className="card-title mb-0">
                  <i className="fas fa-envelope-open-text me-2"></i>
                  Analyze Email
                </h3>
              </div>
              <div className="card-body">
                <EmailForm 
                  onSubmit={analyzeEmail}
                  loading={loading}
                  onExampleSelect={handleExampleSelect}
                />
                
                {/* Error Display */}
                {error && (
                  <div className="alert alert-danger mt-3" role="alert">
                    <i className="fas fa-exclamation-triangle me-2"></i>
                    {error}
                  </div>
                )}

                {/* Result Display */}
                {result && (
                  <ResultDisplay result={result} />
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="col-lg-4">
            {/* Example Emails */}
            <ExampleEmails onExampleSelect={handleExampleSelect} />

            {/* Features Card */}
            <div className="card mt-4">
              <div className="card-header bg-info text-white">
                <h5 className="mb-0">
                  <i className="fas fa-cogs me-2"></i>
                  Detection Features
                </h5>
              </div>
              <div className="card-body">
                <div className="row text-center">
                  <div className="col-6 mb-3">
                    <div className="feature-icon">
                      <i className="fas fa-search"></i>
                    </div>
                    <small>Keyword Analysis</small>
                  </div>
                  <div className="col-6 mb-3">
                    <div className="feature-icon">
                      <i className="fas fa-link"></i>
                    </div>
                    <small>URL Detection</small>
                  </div>
                  <div className="col-6 mb-3">
                    <div className="feature-icon">
                      <i className="fas fa-user-shield"></i>
                    </div>
                    <small>Sender Analysis</small>
                  </div>
                  <div className="col-6 mb-3">
                    <div className="feature-icon">
                      <i className="fas fa-brain"></i>
                    </div>
                    <small>AI Learning</small>
                  </div>
                </div>
              </div>
            </div>

            {/* Tips Card */}
            <div className="card mt-4">
              <div className="card-header bg-warning text-dark">
                <h5 className="mb-0">
                  <i className="fas fa-lightbulb me-2"></i>
                  Security Tips
                </h5>
              </div>
              <div className="card-body">
                <ul className="list-unstyled mb-0">
                  <li className="mb-2">
                    <i className="fas fa-check-circle text-success me-2"></i>
                    Verify sender addresses
                  </li>
                  <li className="mb-2">
                    <i className="fas fa-check-circle text-success me-2"></i>
                    Check for urgency tactics
                  </li>
                  <li className="mb-2">
                    <i className="fas fa-check-circle text-success me-2"></i>
                    Hover over links before clicking
                  </li>
                  <li className="mb-2">
                    <i className="fas fa-check-circle text-success me-2"></i>
                    Look for spelling errors
                  </li>
                  <li className="mb-0">
                    <i className="fas fa-check-circle text-success me-2"></i>
                    Trust your instincts
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="gradient-bg text-white py-4 mt-5">
        <div className="container text-center">
          <div className="row">
            <div className="col-md-6">
              <p className="mb-0">
                <i className="fas fa-shield-alt me-2"></i>
                Email Phishing Detector - Stay Safe Online
              </p>
            </div>
            <div className="col-md-6">
              <p className="mb-0">
                <i className="fas fa-robot me-2"></i>
                Powered by Machine Learning
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
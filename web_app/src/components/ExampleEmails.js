import React from 'react';

const ExampleEmails = ({ onExampleSelect }) => {
  const examples = [
    {
      type: 'phishing',
      title: 'Prize Scam',
      email_text: "Click here to claim your prize! You've won $1000!",
      subject: "Congratulations Winner!",
      sender: "winner@suspicious-site.com",
      icon: 'fas fa-gift'
    },
    {
      type: 'phishing',
      title: 'Account Alert',
      email_text: "Your account has been compromised. Click link to secure it immediately.",
      subject: "Urgent: Account Security Alert",
      sender: "security@fake-bank.net",
      icon: 'fas fa-exclamation-triangle'
    },
    {
      type: 'phishing',
      title: 'Urgent Offer',
      email_text: "ACT NOW! Limited time offer expires in 24 hours!",
      subject: "URGENT OFFER",
      sender: "promotions@spammail.com",
      icon: 'fas fa-clock'
    },
    {
      type: 'legitimate',
      title: 'Meeting Reminder',
      email_text: "Meeting reminder for tomorrow at 2 PM in conference room A",
      subject: "Team Meeting Tomorrow",
      sender: "sarah.johnson@company.com",
      icon: 'fas fa-calendar'
    },
    {
      type: 'legitimate',
      title: 'Work Report',
      email_text: "Please review the attached quarterly report and provide feedback",
      subject: "Q3 Report Review",
      sender: "finance@company.com",
      icon: 'fas fa-file-alt'
    },
    {
      type: 'legitimate',
      title: 'Team Lunch',
      email_text: "Don't forget about the team lunch tomorrow at 12:30 PM",
      subject: "Team Lunch Reminder",
      sender: "hr@company.com",
      icon: 'fas fa-utensils'
    }
  ];

  const phishingExamples = examples.filter(e => e.type === 'phishing');
  const legitimateExamples = examples.filter(e => e.type === 'legitimate');

  const handleExampleClick = (example) => {
    // Trigger the parent callback which should populate the form
    if (onExampleSelect) {
      onExampleSelect(example);
    }
    
    // Scroll to form
    const form = document.querySelector('form');
    if (form) {
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const ExampleCard = ({ examples, title, bgClass, textClass }) => (
    <div className="card mb-3">
      <div className={`card-header ${bgClass} ${textClass}`}>
        <h6 className="mb-0">
          <i className={`${examples[0]?.type === 'phishing' ? 'fas fa-exclamation-triangle' : 'fas fa-shield-check'} me-2`}></i>
          {title}
        </h6>
      </div>
      <div className="card-body p-2">
        {examples.map((example, index) => (
          <div
            key={index}
            className="example-email border rounded p-2 mb-2"
            onClick={() => handleExampleClick(example)}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                handleExampleClick(example);
              }
            }}
          >
            <div className="d-flex align-items-center">
              <i className={`${example.icon} me-2 text-${example.type === 'phishing' ? 'danger' : 'success'}`}></i>
              <div className="flex-grow-1">
                <div className="fw-bold small">{example.title}</div>
                <div className="text-muted" style={{ fontSize: '0.75rem' }}>
                  {example.subject}
                </div>
                <div className="text-truncate" style={{ fontSize: '0.7rem', maxWidth: '200px' }}>
                  {example.email_text}
                </div>
              </div>
              <i className="fas fa-chevron-right text-muted"></i>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div>
      <ExampleCard
        examples={phishingExamples}
        title="Phishing Examples"
        bgClass="bg-danger"
        textClass="text-white"
      />
      
      <ExampleCard
        examples={legitimateExamples}
        title="Legitimate Examples"
        bgClass="bg-success"
        textClass="text-white"
      />

      <div className="card">
        <div className="card-body text-center">
          <i className="fas fa-mouse-pointer text-primary mb-2" style={{ fontSize: '1.5rem' }}></i>
          <p className="small text-muted mb-0">
            Click any example above to auto-fill the form and test the detector
          </p>
        </div>
      </div>
    </div>
  );
};

export default ExampleEmails;
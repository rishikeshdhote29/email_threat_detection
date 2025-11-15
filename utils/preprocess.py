"""
Email Preprocessing Utilities
Functions for cleaning and preprocessing email data for phishing detection
"""

import re
import string
from typing import List, Union


def clean_text(text: str) -> str:
    """Clean and normalize text data"""
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def extract_features(email_text: str, subject: str = "", sender: str = "") -> dict:
    """Extract features from email for machine learning"""
    features = {}
    
    # Text length features
    features['email_length'] = len(email_text)
    features['subject_length'] = len(subject)
    
    # Keyword features (common phishing indicators)
    phishing_keywords = [
        'urgent', 'immediate', 'click here', 'verify', 'confirm',
        'suspended', 'expired', 'winner', 'congratulations',
        'free', 'prize', 'offer', 'limited time', 'act now'
    ]
    
    email_lower = email_text.lower()
    subject_lower = subject.lower()
    
    for keyword in phishing_keywords:
        features[f'has_{keyword.replace(" ", "_")}'] = (
            keyword in email_lower or keyword in subject_lower
        )
    
    # URL and link features
    features['num_urls'] = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_text))
    features['has_suspicious_links'] = bool(re.search(r'bit\.ly|tinyurl|t\.co', email_text.lower()))
    
    # Sender features
    features['sender_suspicious'] = bool(re.search(r'noreply|no-reply|donotreply', sender.lower()))
    
    # Punctuation and formatting
    features['exclamation_count'] = email_text.count('!')
    features['question_count'] = email_text.count('?')
    features['caps_ratio'] = sum(1 for c in email_text if c.isupper()) / max(len(email_text), 1)
    
    return features


def preprocess_email(email_text: str, subject: str = "", sender: str = "") -> List[float]:
    """
    Preprocess email data for model prediction
    This function should match the preprocessing used during training
    """
    # Extract features - this should match what was used during training
    features = extract_features(email_text, subject, sender)
    
    # Return the feature vector as a list of values
    # This matches the format expected by the trained model
    return list(features.values())


def preprocess_dataset(data_path: str) -> tuple:
    """
    Preprocess the entire dataset for training
    Returns features and labels
    """
    import pandas as pd
    
    try:
        # Load the dataset
        df = pd.read_csv(data_path)
        
        # Initialize lists for features and labels
        features = []
        labels = df['is_phishing'].tolist()
        
        # Process each email
        for _, row in df.iterrows():
            email_text = str(row.get('email_text', ''))
            subject = str(row.get('subject', ''))
            sender = str(row.get('sender', ''))
            
            # Extract features
            email_features = extract_features(email_text, subject, sender)
            features.append(list(email_features.values()))
        
        return features, labels
    
    except Exception as e:
        print(f"Error preprocessing dataset: {e}")
        return [], []


def get_feature_names() -> List[str]:
    """Get the names of all features extracted by extract_features"""
    # This should match the features extracted in extract_features
    base_features = ['email_length', 'subject_length']
    
    phishing_keywords = [
        'urgent', 'immediate', 'click_here', 'verify', 'confirm',
        'suspended', 'expired', 'winner', 'congratulations',
        'free', 'prize', 'offer', 'limited_time', 'act_now'
    ]
    
    keyword_features = [f'has_{keyword}' for keyword in phishing_keywords]
    
    other_features = [
        'num_urls', 'has_suspicious_links', 'sender_suspicious',
        'exclamation_count', 'question_count', 'caps_ratio'
    ]
    
    return base_features + keyword_features + other_features
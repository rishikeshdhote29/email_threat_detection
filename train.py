"""
Email Phishing Detection Model Training Script
Train a machine learning model to detect phishing emails
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
from utils.preprocess import preprocess_dataset, get_feature_names, extract_features


class PhishingModelTrainer:
    def __init__(self, data_path='data/emails.csv', model_path='model/phishing_model.pkl'):
        """Initialize the trainer with data and model paths"""
        self.data_path = data_path
        self.model_path = model_path
        self.model = None
        self.feature_names = None
    
    def load_data(self):
        """Load and preprocess the training data"""
        print("Loading and preprocessing data...")
        
        try:
            # Load the CSV file
            df = pd.read_csv(self.data_path)
            print(f"Loaded {len(df)} emails from {self.data_path}")
            
            # Extract features for each email
            features = []
            labels = df['is_phishing'].tolist()
            
            for _, row in df.iterrows():
                email_text = str(row.get('email_text', ''))
                subject = str(row.get('subject', ''))
                sender = str(row.get('sender', ''))
                
                # Extract features using the preprocessing utility
                email_features = extract_features(email_text, subject, sender)
                features.append(list(email_features.values()))
            
            # Convert to numpy arrays
            X = np.array(features)
            y = np.array(labels)
            
            # Store feature names for later use
            self.feature_names = get_feature_names()
            
            print(f"Feature matrix shape: {X.shape}")
            print(f"Number of phishing emails: {sum(y)}")
            print(f"Number of legitimate emails: {len(y) - sum(y)}")
            
            return X, y
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None
    
    def train_model(self, X, y, test_size=0.2, random_state=42):
        """Train the phishing detection model"""
        print("\nTraining the model...")
        
        # Check if we have enough samples for stratified splitting
        min_class_size = min(np.bincount(y))
        min_test_samples = max(1, int(len(y) * test_size))
        
        # Adjust test_size or disable stratification for small datasets
        if len(y) < 10 or min_test_samples < min_class_size:
            print(f"Small dataset ({len(y)} samples). Using simple random split without stratification.")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
        else:
            # Use stratified split for larger datasets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )
        
        print(f"Training set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")
        
        # Create and train the model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=random_state,
            max_depth=10
        )
        
        self.model.fit(X_train, y_train)
        
        # Make predictions on test set
        y_pred = self.model.predict(X_test)
        
        # Print evaluation metrics
        print("\n" + "="*50)
        print("MODEL EVALUATION RESULTS")
        print("="*50)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Legitimate', 'Phishing']))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            print("\nTop 10 Most Important Features:")
            feature_importance = list(zip(self.feature_names, self.model.feature_importances_))
            feature_importance.sort(key=lambda x: x[1], reverse=True)
            
            for i, (feature, importance) in enumerate(feature_importance[:10]):
                print(f"{i+1:2d}. {feature:<20} {importance:.4f}")
        
        return self.model
    
    def save_model(self):
        """Save the trained model to file"""
        if self.model is None:
            print("No model to save. Train the model first.")
            return
        
        try:
            # Create model directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            # Save the model
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            print(f"\nModel saved successfully to {self.model_path}")
        
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def test_predictions(self):
        """Test the model with some example emails"""
        if self.model is None:
            print("No model available for testing.")
            return
        
        print("\n" + "="*50)
        print("TESTING MODEL PREDICTIONS")
        print("="*50)
        
        # Test examples
        test_emails = [
            {
                'email_text': "Click here to claim your prize! You've won $1000!",
                'subject': "Congratulations Winner!",
                'sender': "winner@suspicious-site.com",
                'expected': 'Phishing'
            },
            {
                'email_text': "Meeting reminder for tomorrow at 2 PM in conference room A",
                'subject': "Team Meeting Tomorrow",
                'sender': "sarah.johnson@company.com",
                'expected': 'Legitimate'
            },
            {
                'email_text': "Your account has been compromised. Click link to secure it immediately.",
                'subject': "Urgent: Account Security Alert",
                'sender': "security@fake-bank.net",
                'expected': 'Phishing'
            }
        ]
        
        for i, email in enumerate(test_emails, 1):
            features = extract_features(email['email_text'], email['subject'], email['sender'])
            feature_vector = np.array([list(features.values())])
            
            prediction = self.model.predict(feature_vector)[0]
            probability = self.model.predict_proba(feature_vector)[0]
            
            result = 'Phishing' if prediction == 1 else 'Legitimate'
            confidence = max(probability) * 100
            
            print(f"\nTest {i}:")
            print(f"Subject: {email['subject']}")
            print(f"Expected: {email['expected']}")
            print(f"Predicted: {result}")
            print(f"Confidence: {confidence:.2f}%")
            print(f"Correct: {'✓' if result == email['expected'] else '✗'}")


def main():
    """Main training function"""
    print("Email Phishing Detection Model Training")
    print("="*50)
    
    # Initialize trainer
    trainer = PhishingModelTrainer()
    
    # Load and preprocess data
    X, y = trainer.load_data()
    
    if X is None or y is None:
        print("Failed to load data. Exiting.")
        return
    
    # Train the model
    model = trainer.train_model(X, y)
    
    if model is not None:
        # Save the model
        trainer.save_model()
        
        # Test with examples
        trainer.test_predictions()
        
        print("\n" + "="*50)
        print("Training completed successfully!")
        print("You can now run the application using: python app/main.py")
        print("="*50)
    else:
        print("Training failed.")


if __name__ == "__main__":
    main()
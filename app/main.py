"""
Email Phishing Detection Application
Main application file for running phishing detection on emails
"""

import os
import pickle
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocess import preprocess_email


class PhishingDetector:
    def __init__(self, model_path='../model/phishing_model.pkl'):
        """Initialize the phishing detector with a trained model"""
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model from file"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("Model loaded successfully!")
        except FileNotFoundError:
            print(f"Model file not found at {self.model_path}")
            print("Please train the model first using train.py")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def predict(self, email_text, subject="", sender=""):
        """Predict if an email is phishing or not"""
        if self.model is None:
            return "Model not loaded"
        
        # Preprocess the email to get feature vector
        feature_vector = preprocess_email(email_text, subject, sender)
        
        # Convert to the format expected by the model (2D array)
        import numpy as np
        features_array = np.array([feature_vector])
        
        # Make prediction
        try:
            prediction = self.model.predict(features_array)
            probability = self.model.predict_proba(features_array)
            
            is_phishing = prediction[0] == 1
            confidence = max(probability[0]) * 100
            
            return {
                'is_phishing': is_phishing,
                'confidence': confidence,
                'label': 'Phishing' if is_phishing else 'Legitimate'
            }
        except Exception as e:
            return f"Error making prediction: {e}"


def main():
    """Main function to run the phishing detector"""
    detector = PhishingDetector()
    
    print("Email Phishing Detector")
    print("-" * 30)
    
    while True:
        print("\nEnter email details (or 'quit' to exit):")
        email_text = input("Email content: ")
        
        if email_text.lower() == 'quit':
            break
        
        subject = input("Subject (optional): ")
        sender = input("Sender (optional): ")
        
        result = detector.predict(email_text, subject, sender)
        
        if isinstance(result, dict):
            print(f"\nResult: {result['label']}")
            print(f"Confidence: {result['confidence']:.2f}%")
        else:
            print(f"\nError: {result}")


if __name__ == "__main__":
    main()
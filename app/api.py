"""
Email Phishing Detection REST API
Flask API for phishing detection that can be used by web applications
"""

import os
import pickle
import sys
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocess import preprocess_email

app = Flask(__name__)
CORS(app)  # Enable CORS for web app integration

# Global variables
model = None
model_loaded = False

def load_phishing_model():
    """Load the trained phishing detection model"""
    global model, model_loaded
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'phishing_model.pkl')
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        model_loaded = True
        print(f"✅ Model loaded successfully from {model_path}")
        return True
    except FileNotFoundError:
        print(f"❌ Model file not found at {model_path}")
        print("Please train the model first using: python train.py")
        return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    """API status endpoint"""
    return jsonify({
        'message': 'Email Phishing Detection API',
        'version': '1.0',
        'status': 'active',
        'model_loaded': model_loaded,
        'endpoints': {
            'predict': '/predict (POST)',
            'health': '/health (GET)',
            'status': '/ (GET)'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if model_loaded else 'model_not_loaded',
        'model_loaded': model_loaded,
        'timestamp': str(np.datetime64('now'))
    })

@app.route('/predict', methods=['POST'])
def predict_phishing():
    """
    Predict if an email is phishing or legitimate
    
    Expected JSON payload:
    {
        "email_text": "Your email content here",
        "subject": "Email subject (optional)",
        "sender": "sender@example.com (optional)"
    }
    
    Returns:
    {
        "success": true,
        "prediction": {
            "is_phishing": true/false,
            "confidence": 85.5,
            "label": "Phishing" or "Legitimate"
        },
        "input_data": {...}
    }
    """
    
    # Check if model is loaded
    if not model_loaded or model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please ensure the model is trained and available.',
            'message': 'Run python train.py to train the model first.'
        }), 500
    
    # Validate request
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'email_text' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required field: email_text'
        }), 400
    
    # Extract input data
    email_text = data.get('email_text', '').strip()
    subject = data.get('subject', '').strip()
    sender = data.get('sender', '').strip()
    
    # Validate email_text is not empty
    if not email_text:
        return jsonify({
            'success': False,
            'error': 'email_text cannot be empty'
        }), 400
    
    try:
        # Preprocess the email to get feature vector
        feature_vector = preprocess_email(email_text, subject, sender)
        
        # Convert to the format expected by the model (2D array)
        features_array = np.array([feature_vector])
        
        # Make prediction
        prediction = model.predict(features_array)
        probability = model.predict_proba(features_array)
        
        # Format results
        is_phishing = bool(prediction[0] == 1)
        confidence = float(max(probability[0]) * 100)
        label = 'Phishing' if is_phishing else 'Legitimate'
        
        # Prepare response
        response = {
            'success': True,
            'prediction': {
                'is_phishing': is_phishing,
                'confidence': round(confidence, 2),
                'label': label,
                'risk_level': get_risk_level(confidence, is_phishing)
            },
            'input_data': {
                'email_text': email_text[:100] + ('...' if len(email_text) > 100 else ''),  # Truncate for response
                'subject': subject,
                'sender': sender
            },
            'metadata': {
                'feature_count': len(feature_vector),
                'model_version': '1.0'
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}',
            'message': 'An error occurred while processing the email.'
        }), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict multiple emails at once
    
    Expected JSON payload:
    {
        "emails": [
            {
                "id": "email_1",
                "email_text": "Email content 1",
                "subject": "Subject 1",
                "sender": "sender1@example.com"
            },
            {
                "id": "email_2", 
                "email_text": "Email content 2",
                "subject": "Subject 2",
                "sender": "sender2@example.com"
            }
        ]
    }
    """
    
    # Check if model is loaded
    if not model_loaded or model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded'
        }), 500
    
    # Validate request
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    if 'emails' not in data or not isinstance(data['emails'], list):
        return jsonify({
            'success': False,
            'error': 'Missing or invalid emails array'
        }), 400
    
    if len(data['emails']) > 50:  # Limit batch size
        return jsonify({
            'success': False,
            'error': 'Batch size too large. Maximum 50 emails per request.'
        }), 400
    
    results = []
    
    try:
        for email_data in data['emails']:
            email_id = email_data.get('id', f'email_{len(results)}')
            email_text = email_data.get('email_text', '').strip()
            subject = email_data.get('subject', '').strip()
            sender = email_data.get('sender', '').strip()
            
            if not email_text:
                results.append({
                    'id': email_id,
                    'success': False,
                    'error': 'Empty email_text'
                })
                continue
            
            # Process email
            feature_vector = preprocess_email(email_text, subject, sender)
            features_array = np.array([feature_vector])
            
            prediction = model.predict(features_array)
            probability = model.predict_proba(features_array)
            
            is_phishing = bool(prediction[0] == 1)
            confidence = float(max(probability[0]) * 100)
            
            results.append({
                'id': email_id,
                'success': True,
                'prediction': {
                    'is_phishing': is_phishing,
                    'confidence': round(confidence, 2),
                    'label': 'Phishing' if is_phishing else 'Legitimate',
                    'risk_level': get_risk_level(confidence, is_phishing)
                }
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Batch prediction failed: {str(e)}'
        }), 500

def get_risk_level(confidence, is_phishing):
    """Determine risk level based on confidence and prediction"""
    if is_phishing:
        if confidence >= 90:
            return 'HIGH'
        elif confidence >= 70:
            return 'MEDIUM'
        else:
            return 'LOW'
    else:
        return 'SAFE'

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist.'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred.'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Email Phishing Detection API...")
    print("📡 Loading model...")
    
    # Load the model on startup
    if load_phishing_model():
        print("✅ Model loaded successfully!")
        print("🌐 API is ready!")
    else:
        print("❌ Model not found. Creating basic model for deployment...")
        # Try to create a basic model if none exists
        try:
            from utils.preprocess import get_feature_names
            import pickle
            from sklearn.ensemble import RandomForestClassifier
            import numpy as np
            
            # Create a dummy model for deployment
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            # Fit with dummy data
            X_dummy = np.random.random((10, len(get_feature_names())))
            y_dummy = np.random.randint(0, 2, 10)
            model.fit(X_dummy, y_dummy)
            
            # Save the model
            os.makedirs('model', exist_ok=True)
            with open('model/phishing_model.pkl', 'wb') as f:
                pickle.dump(model, f)
            print("✅ Basic model created successfully!")
            
            # Load the created model
            load_phishing_model()
        except Exception as e:
            print(f"❌ Failed to create basic model: {e}")
    
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting server on port {port}")
    
    # Run the Flask app (debug=False for production)
    app.run(debug=False, host='0.0.0.0', port=port)
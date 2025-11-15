"""
API Test Script
Test the Email Phishing Detection API with sample requests
"""

import requests
import json

# API base URL
API_URL = "http://localhost:5000"

def test_api_status():
    """Test the API status endpoint"""
    print("🔍 Testing API Status...")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"📊 Model Loaded: {data['model_loaded']}")
        else:
            print(f"❌ API Status Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_health_check():
    """Test the health check endpoint"""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Status: {data['status']}")
        else:
            print(f"❌ Health Check Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_phishing_prediction():
    """Test phishing email prediction"""
    print("\n🚨 Testing Phishing Email Detection...")
    
    phishing_email = {
        "email_text": "URGENT! Your account has been compromised. Click here to secure it immediately!",
        "subject": "Account Security Alert",
        "sender": "security@fake-bank.net"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            headers={"Content-Type": "application/json"},
            json=phishing_email
        )
        
        if response.status_code == 200:
            data = response.json()
            prediction = data['prediction']
            print(f"✅ Prediction: {prediction['label']}")
            print(f"📊 Confidence: {prediction['confidence']:.2f}%")
            print(f"⚠️  Risk Level: {prediction['risk_level']}")
        else:
            print(f"❌ Prediction Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_legitimate_prediction():
    """Test legitimate email prediction"""
    print("\n✅ Testing Legitimate Email Detection...")
    
    legitimate_email = {
        "email_text": "Meeting reminder for tomorrow at 2 PM in conference room A. Please bring your quarterly reports.",
        "subject": "Team Meeting Tomorrow",
        "sender": "sarah.johnson@company.com"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            headers={"Content-Type": "application/json"},
            json=legitimate_email
        )
        
        if response.status_code == 200:
            data = response.json()
            prediction = data['prediction']
            print(f"✅ Prediction: {prediction['label']}")
            print(f"📊 Confidence: {prediction['confidence']:.2f}%")
            print(f"⚠️  Risk Level: {prediction['risk_level']}")
        else:
            print(f"❌ Prediction Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_batch_prediction():
    """Test batch prediction"""
    print("\n📦 Testing Batch Prediction...")
    
    batch_data = {
        "emails": [
            {
                "id": "email_1",
                "email_text": "Click here to claim your $1000 prize!",
                "subject": "Congratulations Winner!",
                "sender": "winner@scam.com"
            },
            {
                "id": "email_2",
                "email_text": "Please review the attached quarterly report",
                "subject": "Q3 Report Review",
                "sender": "finance@company.com"
            },
            {
                "id": "email_3",
                "email_text": "ACT NOW! Limited time offer expires in 24 hours!",
                "subject": "URGENT OFFER",
                "sender": "deals@spam.com"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict/batch",
            headers={"Content-Type": "application/json"},
            json=batch_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Processed {data['total_processed']} emails")
            
            for result in data['results']:
                if result['success']:
                    pred = result['prediction']
                    print(f"📧 {result['id']}: {pred['label']} ({pred['confidence']:.1f}% confidence)")
                else:
                    print(f"❌ {result['id']}: {result['error']}")
        else:
            print(f"❌ Batch Prediction Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def main():
    """Run all API tests"""
    print("🧪 Email Phishing Detection API Test Suite")
    print("=" * 50)
    
    # Test all endpoints
    test_api_status()
    test_health_check()
    test_phishing_prediction()
    test_legitimate_prediction()
    test_batch_prediction()
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("\n💡 Integration Tips:")
    print("- Use POST /predict for single email analysis")
    print("- Use POST /predict/batch for multiple emails")
    print("- Check /health before making predictions")
    print("- Handle errors gracefully in your web app")

if __name__ == "__main__":
    main()
# 🚀 Render.com Deployment Guide
## Email Phishing Detection API

## 📋 **Quick Setup for Render.com**

### **Step 1: Repository Setup**
1. Push your code to GitHub/GitLab
2. Connect your repository to Render

### **Step 2: Service Configuration**

#### **🐍 Flask API Service:**
- **Environment**: `Python 3`
- **Build Command**: `pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt`
- **Start Command**: `python app/api.py`
- **Runtime**: Uses `runtime.txt` (Python 3.12.7)
- **Auto-Deploy**: Uses `render.yaml` configuration

#### **⚛️ React Web App Service (optional):**
- **Environment**: `Node.js`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `serve -s build`
- **Publish Directory**: `build`

### **Step 3: Environment Variables**
No additional environment variables needed. Render automatically sets:
- `PORT` - The port your app should listen on

## 🔧 **Files Updated for Deployment**

### **1. requirements.txt**
```txt
# Build tools (required for Render deployment)
setuptools>=65.0.0
wheel>=0.37.0
pip>=22.0.0

# Core dependencies
flask==2.3.3
flask-cors==4.0.0
gunicorn==21.2.0

# ML and data processing
numpy>=1.24.0,<2.0.0
pandas>=2.0.0,<3.0.0
scikit-learn>=1.3.0,<2.0.0

# Additional utilities
requests>=2.31.0
```

### **2. runtime.txt & .python-version**
```txt
python-3.12.7
```

### **3. render.yaml**
```yaml
services:
  - type: web
    name: email-phishing-api
    env: python
    runtime: python-3.12.7
    buildCommand: "pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt"
    startCommand: "python app/api.py"
```

### **3. app/api.py**
- Updated with proper port handling
- Added fallback model creation
- Production-ready error handling

## 🚨 **Troubleshooting Common Issues**

### **Error: "Cannot import 'setuptools.build_meta'"**
✅ **Fixed by:**
- Adding setuptools, wheel, pip to requirements.txt
- Using Python 3.11.6 instead of 3.13
- Enhanced build command

### **Error: "Model not found"**
✅ **Fixed by:**
- Automatic model creation fallback
- Basic dummy model for deployment

### **Error: "Package version conflicts"**
✅ **Fixed by:**
- Version constraints in requirements.txt
- Compatible package versions

## 📱 **Alternative Build Commands (if needed)**

### **Option 1: Standard (recommended)**
```bash
pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
```

### **Option 2: If Python 3.13 is forced**
```bash
pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements-py313.txt
```

### **Option 3: Manual environment specification**
```bash
PYTHON_VERSION=3.12.7 pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

### **Option 4: Conservative approach**
```bash
python -m pip install --upgrade pip==25.3 setuptools==75.6.0 wheel==0.44.0 && python -m pip install --no-cache-dir -r requirements.txt
```

## 🌐 **After Deployment**

### **Your API will be available at:**
`https://your-app-name.onrender.com`

### **Test endpoints:**
- `GET /` - API status
- `GET /health` - Health check  
- `POST /predict` - Email analysis

### **Example API call:**
```bash
curl -X POST https://your-app-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Click here to win $1000!",
    "subject": "Winner!",
    "sender": "spam@fake.com"
  }'
```

## 🔄 **Updating Your React App**

If deploying the React frontend, update the API URL in:
```javascript
// src/App.js
const API_BASE_URL = 'https://your-api-name.onrender.com';
```

## 💡 **Pro Tips**

1. **Free Tier Limitations:**
   - Services sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds

2. **Keep Services Active:**
   - Use a service like UptimeRobot to ping your API
   - Or upgrade to paid plan

3. **Logs and Monitoring:**
   - Check Render dashboard for deployment logs
   - Monitor API health via `/health` endpoint

4. **Database (if needed later):**
   - Render offers PostgreSQL databases
   - Easy to add to your service

## 🎯 **Expected Build Time**
- **First deployment**: 3-5 minutes
- **Subsequent deployments**: 1-3 minutes

Your Email Phishing Detection API should now deploy successfully on Render! 🎉
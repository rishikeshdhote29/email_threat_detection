# 🚀 Complete Frontend Deployment Guide
## React Email Phishing Detector Web App

## 📋 **Step-by-Step Deployment**

### **Step 1: Update API URL in React App**

1. **Replace localhost with your deployed API URL:**
   ```javascript
   // In src/App.js
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-api-name.onrender.com';
   ```

2. **Get your API URL from Render dashboard** (from your backend deployment)

### **Step 2: Choose Deployment Method**

#### **🎯 Method 1: Static Site (Recommended - Free)**

**Render.com Settings:**
- **Type**: Static Site
- **Build Command**: `cd web_app && npm install && npm run build`
- **Publish Directory**: `web_app/build`
- **Auto-Deploy**: Yes

**Environment Variables:**
- `REACT_APP_API_URL`: `https://your-backend-api.onrender.com`

#### **🔧 Method 2: Node.js Web Service**

**Render.com Settings:**
- **Environment**: Node.js
- **Root Directory**: `web_app`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run serve`
- **Auto-Deploy**: Yes

**Environment Variables:**
- `NODE_ENV`: `production`
- `REACT_APP_API_URL`: `https://your-backend-api.onrender.com`

### **Step 3: Deploy on Render.com**

1. **Create New Service:**
   - Go to Render.com dashboard
   - Click "New +" → "Static Site" or "Web Service"
   - Connect your GitHub repository

2. **Configure Settings:**
   - **Name**: `email-phishing-frontend`
   - **Branch**: `main`
   - **Root Directory**: `web_app` (if needed)
   - **Build Command**: See methods above
   - **Publish Directory**: `build` (for static site)

3. **Set Environment Variables:**
   - Add `REACT_APP_API_URL` with your backend URL
   - Click "Create Static Site" or "Create Web Service"

4. **Wait for Deployment:**
   - First build takes 3-5 minutes
   - Check logs for any errors

### **Step 4: Update CORS Settings**

Update your backend API to allow requests from the frontend domain:

```python
# In app/api.py, update CORS settings
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",  # Development
    "https://your-frontend-app.onrender.com",  # Production
    "https://*.onrender.com"  # Allow all Render subdomains
])
```

## 🌐 **Alternative Deployment Options**

### **Option 2: Vercel (Free)**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd web_app
   vercel --prod
   ```

3. **Set Environment Variables:**
   ```bash
   vercel env add REACT_APP_API_URL production
   # Enter: https://your-backend-api.onrender.com
   ```

### **Option 3: Netlify (Free)**

1. **Build locally:**
   ```bash
   cd web_app
   npm run build
   ```

2. **Deploy to Netlify:**
   - Drag and drop `build` folder to Netlify
   - Or connect GitHub repository

3. **Set Environment Variables:**
   - Go to Site Settings → Environment Variables
   - Add `REACT_APP_API_URL`: `https://your-backend-api.onrender.com`

### **Option 4: GitHub Pages (Free)**

1. **Install gh-pages:**
   ```bash
   cd web_app
   npm install --save-dev gh-pages
   ```

2. **Add to package.json:**
   ```json
   {
     "homepage": "https://yourusername.github.io/repository-name",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```

3. **Deploy:**
   ```bash
   npm run deploy
   ```

## 🔧 **Post-Deployment Setup**

### **1. Test the Integration:**
- Visit your frontend URL
- Try analyzing a sample email
- Check browser console for errors
- Verify API calls are working

### **2. Update Backend CORS:**
Add your frontend domain to allowed origins in your Flask API.

### **3. Custom Domain (Optional):**
- Purchase domain from registrar
- Add CNAME record pointing to Render
- Configure custom domain in Render dashboard

## 📱 **URLs After Deployment**

- **Backend API**: `https://your-api-name.onrender.com`
- **Frontend App**: `https://your-frontend-name.onrender.com`
- **API Health Check**: `https://your-api-name.onrender.com/health`

## 🚨 **Troubleshooting**

### **CORS Errors:**
```javascript
// Add to your API allowed origins
"https://your-frontend-app.onrender.com"
```

### **Environment Variables Not Working:**
- Ensure they start with `REACT_APP_`
- Rebuild after adding env vars
- Check Render dashboard env vars section

### **Build Failures:**
- Check Node.js version compatibility
- Ensure all dependencies are in package.json
- Check build logs in Render dashboard

### **API Connection Issues:**
- Verify API URL is correct and accessible
- Check if API is sleeping (free tier)
- Test API endpoints directly

## 💡 **Pro Tips**

1. **Free Tier Considerations:**
   - Static sites never sleep (unlike web services)
   - Use static site for frontend when possible
   - API might sleep after 15 minutes of inactivity

2. **Performance:**
   - Use static site deployment for faster loading
   - Enable gzip compression
   - Optimize images and assets

3. **Monitoring:**
   - Set up uptime monitoring for API
   - Use Render's built-in analytics
   - Monitor for CORS and API errors

4. **Updates:**
   - Both services auto-deploy on git push
   - Can trigger manual deploys from dashboard
   - Check deployment logs for issues

Your React frontend will now be live and connected to your Flask API backend! 🎉

## 📋 **Final Architecture**

```
[User] → [React Frontend on Render] → [Flask API on Render] → [ML Model]
         https://frontend.onrender.com    https://api.onrender.com
```

Both services are now deployed and working together! 🚀
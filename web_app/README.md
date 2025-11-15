# React Web App Setup Instructions

## 🚀 Quick Start

### 1. Navigate to the web app directory
```bash
cd web_app
```

### 2. Install Node.js dependencies
```bash
npm install
```

### 3. Start the React development server
```bash
npm start
```

The web app will open automatically at `http://localhost:3000`

## 📋 Prerequisites

Make sure you have:
1. **Node.js** (version 14 or higher)
2. **npm** (comes with Node.js)
3. **Python API server** running on port 5000

## 🔧 Complete Setup Process

### Step 1: Install Dependencies
```bash
# Navigate to web app folder
cd email_phishing_detector/web_app

# Install all React dependencies
npm install
```

### Step 2: Start the API Server
In a separate terminal, from the root project directory:
```bash
# Make sure you have trained the model first
python train.py

# Start the API server
python app/api.py
```

### Step 3: Start the Web App
```bash
# In the web_app directory
npm start
```

## 🌐 Using the Web App

1. **Open your browser** to `http://localhost:3000`
2. **Paste email content** into the text area
3. **Add subject and sender** (optional but recommended)
4. **Click "Analyze Email"** to get results
5. **View the results** with confidence scores and risk levels

## ✨ Features

- **Real-time Analysis**: Instant phishing detection
- **Beautiful UI**: Modern, responsive design
- **Example Emails**: Click-to-test with sample emails
- **Detailed Results**: Confidence scores, risk levels, and recommendations
- **API Status**: Live monitoring of API server status
- **Batch Processing**: Analyze multiple emails (via API)

## 🛠️ Troubleshooting

### API Connection Issues
- Make sure the Python API is running on `http://localhost:5000`
- Check that the model is trained (`python train.py`)
- Verify no firewall is blocking port 5000

### React App Issues
- Ensure Node.js version 14+ is installed
- Try `npm install` again if packages are missing
- Clear browser cache if styles look broken

### Port Conflicts
- React app uses port 3000
- API server uses port 5000
- Make sure these ports are available

## 📱 Responsive Design

The web app works on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones
- ✅ All modern browsers

## 🎨 Customization

You can customize the app by editing:
- `src/App.css` - Main styling
- `src/index.css` - Global styles
- `src/components/` - Individual components
- `public/index.html` - HTML template

## 🚦 Production Deployment

For production deployment:

1. **Build the app**:
   ```bash
   npm run build
   ```

2. **Serve the built files** using a web server like nginx or Apache

3. **Update API URL** in `src/App.js` to point to your production API server

4. **Configure CORS** on your API server for your domain

## 💡 Tips

- Use the example buttons for quick testing
- The app automatically checks API status
- Results include actionable security recommendations
- All analysis happens on your local server for privacy

Enjoy your new phishing detection web app! 🎉
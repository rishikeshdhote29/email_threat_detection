# Render.com Frontend Deployment Settings

## Web Service Configuration:
- **Environment**: Node.js
- **Node Version**: 20.11.0 (via .nvmrc)
- **Root Directory**: web_app
- **Build Command**: `npm install && chmod -R 755 node_modules/.bin/ && CI=false npx react-scripts build`
- **Start Command**: `npx serve -s build -p $PORT`

## Static Site Configuration (Alternative):
- **Build Command**: `cd web_app && npm install && chmod -R 755 node_modules/.bin/ && CI=false npx react-scripts build`
- **Publish Directory**: web_app/build

## Environment Variables:
- CI: false
- NODE_ENV: production
- REACT_APP_API_URL: https://email-threat-detection.onrender.com

## Build Command Options (if above fails):
1. `npm install && npm run build:render`
2. `npm ci && CI=false npx react-scripts build`
3. `npm install --legacy-peer-deps && CI=false npx react-scripts build`
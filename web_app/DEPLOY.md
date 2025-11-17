# Frontend Deployment Configuration

## For React Static Site on Render.com

### Build Settings:
- **Environment**: Static Site
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `build`
- **Auto-Deploy**: Yes

### Environment Variables:
- `REACT_APP_API_URL`: https://your-backend-api.onrender.com

## Alternative: Node.js Web Service

### Build Settings:
- **Environment**: Node.js
- **Build Command**: `npm install && npm run build`
- **Start Command**: `serve -s build -l $PORT`
- **Root Directory**: `web_app`
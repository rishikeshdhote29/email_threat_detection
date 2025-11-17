# Render.com Deployment Configuration

## Build Settings for Render

### For Flask API Service:
- **Environment**: Python 3
- **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
- **Start Command**: `python app/api.py`
- **Python Version**: 3.11.6 (specified in runtime.txt)

### For React Web App Service:
- **Environment**: Node.js
- **Build Command**: `npm install && npm run build`
- **Start Command**: `serve -s build`
- **Publish Directory**: `build`

## Environment Variables (if needed):
- `PYTHON_VERSION`: 3.11.6
- `PORT`: (automatically set by Render)

## Build Command Explanation:
The enhanced build command includes:
1. `pip install --upgrade pip setuptools wheel` - Ensures build tools are up to date
2. `pip install -r requirements.txt` - Installs your app dependencies

## Files Created for Deployment:
- `runtime.txt` - Specifies Python version (3.11.6 to avoid 3.13 compatibility issues)
- `requirements.txt` - Updated with build tools and version constraints
- Enhanced API with proper port handling

## Troubleshooting:
If build still fails:
1. Try Python 3.10.13 in runtime.txt
2. Use the alternative build command: `pip3 install -r requirements.txt`
3. Check Render logs for specific package conflicts
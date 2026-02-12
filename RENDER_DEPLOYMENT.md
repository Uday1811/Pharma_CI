# Render Deployment Guide for PharmaIntelScan

## Prerequisites
- GitHub account with the repository: https://github.com/Uday1811/Pharma_CI
- Render account (sign up at https://render.com)

## Deployment Steps

### 1. Sign Up / Log In to Render
- Go to https://render.com
- Sign up or log in (you can use your GitHub account)

### 2. Create New Web Service
1. Click "New +" button in the top right
2. Select "Web Service"
3. Connect your GitHub account if not already connected
4. Select the repository: `Pharma_CI`
5. Click "Connect"

### 3. Configure the Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `pharma-ci` (or any name you prefer)
- **Region**: Choose closest to your location
- **Branch**: `main`
- **Root Directory**: Leave empty (or use `PharmaIntelScan-main` if needed)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

**Instance Type:**
- Select "Free" (or paid plan for better performance)

**Environment Variables:**
- Click "Add Environment Variable"
- Add: `PYTHON_VERSION` = `3.11.0`
- Add: `PORT` = `8501` (Render will override this automatically)

### 4. Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Run the setup script
   - Start your Streamlit app

### 5. Monitor Deployment
- Watch the logs in real-time
- Deployment typically takes 2-5 minutes
- Once complete, you'll see "Your service is live 🎉"

### 6. Access Your App
- Render will provide a URL like: `https://pharma-ci.onrender.com`
- Click the URL to access your deployed app

## Important Notes

### Free Tier Limitations
- Free instances spin down after 15 minutes of inactivity
- First request after inactivity may take 30-60 seconds to wake up
- 750 hours/month of free usage

### Files Already Configured
✅ `requirements.txt` - Lightweight dependencies (7 packages)
✅ `Procfile` - Start command for Render
✅ `setup.sh` - Streamlit configuration script
✅ `runtime.txt` - Python version specification

### Database
- The app uses SQLite (`pharma_ci.db`)
- On Render free tier, the database will reset on each deploy
- For persistent data, consider upgrading to a paid plan with persistent disk

## Troubleshooting

### If deployment fails:
1. Check the logs in Render dashboard
2. Verify all files are pushed to GitHub
3. Ensure `requirements.txt` has no heavy packages
4. Check Python version compatibility

### If app doesn't load:
1. Check Render logs for errors
2. Verify the start command is correct
3. Ensure port configuration is correct
4. Check if the service is running (not sleeping)

## Alternative: Manual Configuration

If you prefer to configure manually:

1. In Render dashboard, go to your service settings
2. Update "Start Command" to:
   ```
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
   ```
3. Save changes and redeploy

## Support
- Render Documentation: https://render.com/docs
- Streamlit on Render: https://render.com/docs/deploy-streamlit

---

**Your app is ready to deploy! Just follow the steps above.**

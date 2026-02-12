# Deploying Pharma CI Platform to Render

## Prerequisites

1. A [Render](https://render.com) account (free tier available)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Optional: A PostgreSQL database (Render provides free PostgreSQL)

## Deployment Steps

### Option 1: Deploy with Blueprint (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and configure the service

3. **Configure Environment Variables** (Optional)
   - If you want to use PostgreSQL instead of SQLite:
     - Create a PostgreSQL database in Render (New → PostgreSQL)
     - Copy the Internal Database URL
     - In your web service settings, add environment variable:
       - Key: `DATABASE_URL`
       - Value: `<your-postgres-internal-url>`

### Option 2: Manual Deployment

1. **Push your code to GitHub** (same as above)

2. **Create a New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your repository

3. **Configure the Service**
   - **Name**: pharma-ci-platform
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Instance Type**: Free (or paid for better performance)

4. **Add Environment Variables** (Optional)
   - Click "Environment" tab
   - Add `DATABASE_URL` if using PostgreSQL

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app

## Database Setup (Optional)

### Using PostgreSQL on Render

1. **Create PostgreSQL Database**
   - In Render Dashboard, click "New" → "PostgreSQL"
   - Name: `pharma-ci-db`
   - Database: `pharma_ci`
   - User: `pharma_ci_user`
   - Region: Same as your web service
   - Plan: Free or paid
   - Click "Create Database"

2. **Get Database URL**
   - Once created, copy the "Internal Database URL"
   - Format: `postgresql://user:password@host/database`

3. **Add to Web Service**
   - Go to your web service settings
   - Environment tab → Add Environment Variable
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL
   - Save changes

4. **Initialize Database**
   - The app will automatically initialize the database on first run
   - Check logs to confirm: "Database initialized successfully"

### Using SQLite (Default)

- If you don't set `DATABASE_URL`, the app uses SQLite
- Note: SQLite data is ephemeral on Render's free tier (resets on redeploy)
- For production, use PostgreSQL

## Post-Deployment

1. **Access Your App**
   - Render will provide a URL like: `https://pharma-ci-platform.onrender.com`
   - The app will be accessible at this URL

2. **Monitor Logs**
   - Go to your service in Render Dashboard
   - Click "Logs" tab to see application logs
   - Check for any errors during startup

3. **Custom Domain** (Optional)
   - In service settings, go to "Settings" → "Custom Domain"
   - Add your domain and follow DNS configuration instructions

## Troubleshooting

### App Not Starting
- Check logs for errors
- Verify all dependencies in `requirements.txt`
- Ensure `DATABASE_URL` is correctly formatted if using PostgreSQL

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Use "Internal Database URL" not "External Database URL"
- Check database is in the same region as web service

### Port Issues
- Render automatically sets `$PORT` environment variable
- The start command uses `--server.port=$PORT` to bind correctly

### Memory Issues
- Free tier has 512MB RAM limit
- Consider upgrading to paid tier if needed
- Optimize data loading and caching

## Files Created for Deployment

- `requirements.txt` - Python dependencies
- `render.yaml` - Render Blueprint configuration
- `runtime.txt` - Python version specification
- `.streamlit/config.toml` - Streamlit configuration

## Cost Estimate

- **Free Tier**: $0/month
  - Web service spins down after 15 minutes of inactivity
  - PostgreSQL: 90 days free, then $7/month
  
- **Starter Tier**: $7/month
  - Always-on web service
  - Better performance

## Support

For issues with Render deployment:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

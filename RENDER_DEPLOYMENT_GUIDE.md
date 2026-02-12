# Deploy Pharma CI Platform to Render with PostgreSQL (Free 90 Days)

## Complete Step-by-Step Guide

### Step 1: Prepare Your Code for Deployment

Your code is already configured! These files are ready:
- ✓ `requirements.txt` - Dependencies
- ✓ `render.yaml` - Render configuration
- ✓ `runtime.txt` - Python version
- ✓ `.streamlit/config.toml` - Streamlit settings

### Step 2: Push Code to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for Render deployment"
   ```

2. **Create GitHub Repository**:
   - Go to [https://github.com/new](https://github.com/new)
   - Name: `pharma-ci-platform`
   - Make it Public or Private (your choice)
   - Don't initialize with README (you already have one)
   - Click "Create repository"

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/pharma-ci-platform.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**:
   - Visit [https://dashboard.render.com](https://dashboard.render.com)
   - Sign up or log in (can use GitHub account)

2. **Create PostgreSQL Database**:
   - Click **"New +"** button (top right)
   - Select **"PostgreSQL"**

3. **Configure Database**:
   - **Name**: `pharma-ci-db`
   - **Database**: `pharma_ci` (or leave default)
   - **User**: `pharma_ci_user` (or leave default)
   - **Region**: Choose closest to you (e.g., Oregon, Ohio, Frankfurt)
   - **PostgreSQL Version**: 15 or 16 (latest)
   - **Plan**: **Free** (90 days free, then $7/month)

4. **Create Database**:
   - Click **"Create Database"**
   - Wait 1-2 minutes for provisioning

5. **Copy Connection String**:
   - Once created, scroll down to **"Connections"** section
   - Copy the **"Internal Database URL"** (NOT External)
   - It looks like:
     ```
     postgresql://pharma_ci_user:xxxxx@dpg-xxxxx-a/pharma_ci_xxxxx
     ```
   - **IMPORTANT**: Keep this tab open, you'll need it in Step 4!

### Step 4: Deploy Web Service on Render

1. **Create Web Service**:
   - In Render Dashboard, click **"New +"** → **"Web Service"**

2. **Connect Repository**:
   - Click **"Connect a repository"**
   - Authorize Render to access your GitHub
   - Select your `pharma-ci-platform` repository

3. **Configure Web Service**:
   Fill in these settings:

   - **Name**: `pharma-ci-platform`
   - **Region**: **Same as your database** (important!)
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
     ```
   - **Instance Type**: **Free**

4. **Add Environment Variables**:
   - Scroll down to **"Environment Variables"** section
   - Click **"Add Environment Variable"**
   - Add this variable:
     - **Key**: `DATABASE_URL`
     - **Value**: Paste the Internal Database URL you copied in Step 3
   - Click **"Add"**

5. **Deploy**:
   - Click **"Create Web Service"**
   - Render will start building your app (takes 3-5 minutes)

### Step 5: Monitor Deployment

1. **Watch Build Logs**:
   - You'll see logs in real-time
   - Look for:
     ```
     ==> Installing dependencies from requirements.txt
     ==> Build successful!
     ==> Starting service...
     ```

2. **Check Application Logs**:
   - Once deployed, click **"Logs"** tab
   - You should see:
     ```
     ✓ Using database: postgresql://pharma_ci_user@***
     You can now view your Streamlit app in your browser.
     ```

3. **Access Your App**:
   - Render provides a URL like: `https://pharma-ci-platform.onrender.com`
   - Click the URL at the top of the page
   - Your app should load! 🎉

### Step 6: Initialize Database

The database will be automatically initialized when the app first runs. You should see sample data including:
- 13 pharmaceutical companies
- 16 drugs across all development phases
- 5 Key Opinion Leaders
- 5 scientific publications

### Troubleshooting

#### Build Fails
- Check logs for specific error
- Verify `requirements.txt` is correct
- Ensure Python version matches `runtime.txt`

#### App Won't Start
- Check logs for errors
- Verify `DATABASE_URL` is set correctly
- Make sure you used **Internal Database URL** (not External)

#### Database Connection Error
- Ensure database and web service are in **same region**
- Verify `DATABASE_URL` format is correct
- Check database is running (green status in Render dashboard)

#### App is Slow
- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds (cold start)
- Upgrade to paid tier ($7/month) for always-on service

#### "This site can't be reached"
- Wait 3-5 minutes for initial deployment
- Check build logs for errors
- Verify service status is "Live" (green)

### Important Notes

#### Free Tier Limitations
- **Web Service**: Spins down after 15 min inactivity
- **PostgreSQL**: Free for 90 days, then $7/month
- **Storage**: 1GB database storage
- **Bandwidth**: 100GB/month

#### After 90 Days
You'll receive an email before the free period ends. Options:
1. Upgrade to paid plan ($7/month for database)
2. Export your data and migrate to another service
3. Switch back to SQLite (data will be lost on redeploy)

#### Security
- Never commit `.env` file to Git
- Use Render's environment variables for secrets
- Database URL is encrypted in Render

### Updating Your App

When you make changes:

1. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```

2. **Auto-deploy**:
   - Render automatically detects changes
   - Rebuilds and redeploys your app
   - Takes 2-3 minutes

### Custom Domain (Optional)

1. Go to your web service settings
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain
4. Update DNS records as instructed
5. SSL certificate is automatically provisioned

### Monitoring

- **Logs**: Real-time application logs
- **Metrics**: CPU, memory usage (paid plans)
- **Alerts**: Email notifications for downtime

## Quick Reference

### Your Render URLs
- **Web App**: `https://pharma-ci-platform.onrender.com`
- **Database**: Internal URL (in environment variables)

### Useful Commands

Check database connection:
```bash
# In Render Shell (Settings → Shell)
python -c "from utils.database import engine; print('Connected!' if engine else 'Failed')"
```

Re-initialize database:
```bash
python init_db.py
```

### Support Resources
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Streamlit Docs](https://docs.streamlit.io)

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] PostgreSQL database created on Render
- [ ] Internal Database URL copied
- [ ] Web service created and connected to GitHub
- [ ] DATABASE_URL environment variable set
- [ ] Build completed successfully
- [ ] App is accessible via Render URL
- [ ] Sample data loaded correctly
- [ ] All pages working (Dashboard, Pipeline, News, KOL)

## Next Steps

Once deployed:
1. Test all features
2. Share the URL with your team
3. Monitor usage and performance
4. Consider upgrading before 90-day free period ends
5. Set up custom domain if needed

Congratulations! Your Pharma CI Platform is now live! 🚀

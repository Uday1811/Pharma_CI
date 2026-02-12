# Render Deployment Checklist

## Pre-Deployment ✓

- [x] `requirements.txt` created
- [x] `render.yaml` configured
- [x] `runtime.txt` set to Python 3.11
- [x] `.streamlit/config.toml` configured
- [x] `.gitignore` includes `.env`
- [x] Database code supports PostgreSQL

## Step 1: GitHub Setup

- [ ] Git repository initialized
- [ ] All files committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Repository is accessible

## Step 2: Render PostgreSQL Database

- [ ] Render account created/logged in
- [ ] PostgreSQL database created
- [ ] Database name: `pharma-ci-db`
- [ ] Region selected (remember this!)
- [ ] Database status: **Live** (green)
- [ ] **Internal Database URL** copied and saved

## Step 3: Render Web Service

- [ ] Web service created
- [ ] GitHub repository connected
- [ ] Service name: `pharma-ci-platform`
- [ ] Region: **Same as database**
- [ ] Build command set correctly
- [ ] Start command set correctly
- [ ] Instance type: **Free**

## Step 4: Environment Variables

- [ ] `DATABASE_URL` added
- [ ] Value is **Internal Database URL** (not External)
- [ ] Format: `postgresql://user:pass@host/database`

## Step 5: Deployment

- [ ] "Create Web Service" clicked
- [ ] Build started
- [ ] Build completed successfully (no errors)
- [ ] Service status: **Live** (green)
- [ ] Logs show: "You can now view your Streamlit app"

## Step 6: Verification

- [ ] App URL accessible
- [ ] Dashboard page loads
- [ ] Competitor Pipeline page works
- [ ] News Monitor page works
- [ ] KOL Insights page works
- [ ] Sample data visible (companies, drugs, etc.)
- [ ] Charts rendering correctly
- [ ] No error messages in UI

## Post-Deployment

- [ ] URL bookmarked
- [ ] Team notified
- [ ] Calendar reminder set for 80 days (before free period ends)
- [ ] Documentation reviewed

## Troubleshooting Reference

### If build fails:
1. Check build logs for specific error
2. Verify all files are in GitHub
3. Check `requirements.txt` syntax

### If app won't start:
1. Check application logs
2. Verify `DATABASE_URL` is set
3. Ensure database is in same region

### If database connection fails:
1. Verify using **Internal** URL (not External)
2. Check database status is Live
3. Confirm regions match

### If app is slow:
- Normal on free tier (cold starts)
- First request after 15 min takes 30-60 seconds
- Consider upgrading to paid tier

## Important URLs

- Render Dashboard: https://dashboard.render.com
- Your App: `https://pharma-ci-platform.onrender.com`
- GitHub Repo: `https://github.com/YOUR_USERNAME/pharma-ci-platform`

## Timeline

- **Now**: Free web service + Free PostgreSQL (90 days)
- **Day 80**: Receive reminder email from Render
- **Day 90**: PostgreSQL becomes $7/month (or export data)

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- This project's guide: `RENDER_DEPLOYMENT_GUIDE.md`

# Deployment Guide for Pharma CI Platform

## Recommended: Streamlit Community Cloud (Free & Easy)

Streamlit Community Cloud is the best option for deploying Streamlit apps. It's free, easy to use, and specifically designed for Streamlit applications.

### Steps to Deploy on Streamlit Community Cloud:

1. **Push your code to GitHub** (already done!)
   ```bash
   git push -u origin main
   ```

2. **Go to Streamlit Community Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

3. **Deploy your app**
   - Click "New app"
   - Select your repository: `Uday1811/Pharma_CI`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

4. **Your app will be live at:**
   - `https://[your-app-name].streamlit.app`

### Environment Variables (if needed):
- Go to your app settings
- Add any required environment variables like `DATABASE_URL`

---

## Alternative: Heroku Deployment

If you prefer Heroku, follow these steps:

### Prerequisites:
- Heroku account
- Heroku CLI installed

### Files Required (already created):
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version
- `Procfile` - Heroku process file

### Create Procfile:
```bash
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Create setup.sh:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Deploy to Heroku:
```bash
heroku login
heroku create pharma-ci-platform
git push heroku main
heroku open
```

---

## Alternative: Railway Deployment

Railway is another great option for deploying Streamlit apps.

### Steps:

1. **Go to Railway**
   - Visit: https://railway.app/
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Uday1811/Pharma_CI`

3. **Configure**
   - Railway will auto-detect it's a Python app
   - Add start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Deploy**
   - Click "Deploy"
   - Your app will be live!

---

## Note about Vercel

Vercel is primarily designed for Next.js and static sites. While it's possible to deploy Streamlit apps on Vercel, it requires additional configuration and may not work optimally. We recommend using Streamlit Community Cloud, Heroku, or Railway instead.

---

## Database Configuration

For production deployment, you'll need to:

1. Set up a PostgreSQL database (most platforms offer free tiers)
2. Add the `DATABASE_URL` environment variable
3. Run database migrations

### Free PostgreSQL Options:
- **Neon** (https://neon.tech/) - Free PostgreSQL
- **Supabase** (https://supabase.com/) - Free PostgreSQL
- **ElephantSQL** (https://www.elephantsql.com/) - Free tier available

---

## Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] Database is connected
- [ ] All pages load correctly
- [ ] Data is displaying properly
- [ ] No errors in logs

---

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/Uday1811/Pharma_CI/issues

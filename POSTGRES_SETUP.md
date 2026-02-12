# PostgreSQL Setup Guide

## Quick Start - Use Free Cloud PostgreSQL (Recommended)

### Option 1: Neon (Easiest - No Credit Card Required)

1. **Sign up for Neon**
   - Go to [https://neon.tech](https://neon.tech)
   - Click "Sign Up" (free, no credit card needed)
   - Sign in with GitHub, Google, or email

2. **Create a Project**
   - Click "Create Project"
   - Name: `pharma-ci-platform`
   - Region: Choose closest to you
   - Click "Create Project"

3. **Get Connection String**
   - After creation, you'll see the connection details
   - Copy the **Connection String** (looks like):
     ```
     postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
     ```

4. **Configure Your App**
   - Run the setup script:
     ```bash
     python setup_postgres.py
     ```
   - Paste your connection string when prompted
   - OR manually create a `.env` file:
     ```
     DATABASE_URL=postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
     ```

5. **Initialize Database**
   ```bash
   python init_db.py
   ```

6. **Run the App**
   ```bash
   streamlit run app.py
   ```

### Option 2: Supabase

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up and create a new project
3. Go to Settings → Database
4. Copy the "Connection string" (URI format)
5. Follow steps 4-6 from Neon instructions above

### Option 3: Render PostgreSQL

1. Go to [https://render.com](https://render.com)
2. Sign up/login
3. Click "New" → "PostgreSQL"
4. Create database (90 days free)
5. Copy the "Internal Database URL"
6. Follow steps 4-6 from Neon instructions above

## Local PostgreSQL Installation

### Windows

1. **Download PostgreSQL**
   - Go to [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
   - Download the installer (version 15 or 16)

2. **Install**
   - Run the installer
   - Remember the password you set for the `postgres` user
   - Keep default port: 5432
   - Install pgAdmin (included)

3. **Create Database**
   - Open pgAdmin
   - Right-click "Databases" → "Create" → "Database"
   - Name: `pharma_ci`
   - Click "Save"

4. **Configure Connection**
   - Create `.env` file in project root:
     ```
     DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/pharma_ci
     ```
   - Replace `YOUR_PASSWORD` with your postgres password

5. **Initialize and Run**
   ```bash
   python init_db.py
   streamlit run app.py
   ```

### Using Docker (Alternative)

1. **Install Docker Desktop**
   - Download from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. **Run PostgreSQL Container**
   ```bash
   docker run --name pharma-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=pharma_ci -p 5432:5432 -d postgres:15
   ```

3. **Configure Connection**
   - Create `.env` file:
     ```
     DATABASE_URL=postgresql://postgres:password@localhost:5432/pharma_ci
     ```

4. **Initialize and Run**
   ```bash
   python init_db.py
   streamlit run app.py
   ```

## Verify Connection

After setup, run this to test your connection:

```bash
python -c "from utils.database import engine; print('✓ Database connection successful!' if engine else '✗ Connection failed')"
```

## Migrate Existing SQLite Data (Optional)

If you have existing data in SQLite that you want to migrate:

```bash
# Export from SQLite
sqlite3 pharma_ci.db .dump > backup.sql

# Import to PostgreSQL (requires manual conversion)
# Or just re-run init_db.py to seed fresh data
python init_db.py
```

## Troubleshooting

### Connection Refused
- Check if PostgreSQL is running
- Verify port 5432 is not blocked
- Check username/password are correct

### SSL Required Error
- Add `?sslmode=require` to the end of your DATABASE_URL
- Example: `postgresql://user:pass@host/db?sslmode=require`

### Permission Denied
- Ensure the database user has proper permissions
- For local PostgreSQL, use the `postgres` superuser

## Environment Variables

The app looks for `DATABASE_URL` in this order:
1. `.env` file in project root
2. System environment variable
3. Falls back to SQLite if not found

## Security Notes

- Never commit `.env` file to Git (it's in `.gitignore`)
- Use strong passwords for production databases
- For production, use connection pooling and SSL
- Rotate credentials regularly

## Next Steps

Once PostgreSQL is configured:
1. Your app will automatically use PostgreSQL instead of SQLite
2. Data persists across restarts
3. Ready for production deployment on Render
4. Can handle multiple concurrent users

"""
Setup script to configure PostgreSQL database.
This script helps you set up a PostgreSQL connection.
"""

import os
import sys

def setup_postgres():
    print("=" * 60)
    print("PostgreSQL Setup for Pharma CI Platform")
    print("=" * 60)
    print()
    print("You have several options to get a PostgreSQL database:")
    print()
    print("1. Use a FREE cloud PostgreSQL service (Recommended):")
    print("   - Neon (https://neon.tech) - Free tier, no credit card")
    print("   - Supabase (https://supabase.com) - Free tier")
    print("   - ElephantSQL (https://www.elephantsql.com) - Free tier")
    print("   - Render (https://render.com) - 90 days free")
    print()
    print("2. Install PostgreSQL locally:")
    print("   - Download from: https://www.postgresql.org/download/windows/")
    print("   - Or use Docker: docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres")
    print()
    print("=" * 60)
    print()
    
    choice = input("Do you have a PostgreSQL connection URL? (y/n): ").lower()
    
    if choice == 'y':
        print()
        print("Please enter your PostgreSQL connection URL.")
        print("Format: postgresql://username:password@host:port/database")
        print("Example: postgresql://user:pass@localhost:5432/pharma_ci")
        print()
        db_url = input("DATABASE_URL: ").strip()
        
        if db_url:
            # Create .env file
            with open('.env', 'w') as f:
                f.write(f"DATABASE_URL={db_url}\n")
            
            print()
            print("✓ Configuration saved to .env file")
            print()
            print("Next steps:")
            print("1. Run: python init_db.py (to initialize the database)")
            print("2. Run: streamlit run app.py (to start the application)")
            print()
            return True
    else:
        print()
        print("Please follow these steps:")
        print()
        print("OPTION A - Use Neon (Easiest, Free):")
        print("1. Go to https://neon.tech")
        print("2. Sign up (free, no credit card required)")
        print("3. Create a new project")
        print("4. Copy the connection string")
        print("5. Run this script again and paste the connection string")
        print()
        print("OPTION B - Install PostgreSQL Locally:")
        print("1. Download PostgreSQL from: https://www.postgresql.org/download/windows/")
        print("2. Install with default settings (remember the password)")
        print("3. Open pgAdmin or psql and create a database: CREATE DATABASE pharma_ci;")
        print("4. Your connection URL will be: postgresql://postgres:YOUR_PASSWORD@localhost:5432/pharma_ci")
        print("5. Run this script again and paste the connection string")
        print()
    
    return False

if __name__ == "__main__":
    setup_postgres()

"""
Vercel serverless function wrapper for Streamlit app.
Note: This is a workaround and may have limitations.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from streamlit.web import cli as stcli

def handler(request):
    """Handle Vercel serverless function requests"""
    sys.argv = ["streamlit", "run", "app.py", "--server.headless", "true"]
    sys.exit(stcli.main())

"""
Download required models for the application.
This script is run during deployment to download spaCy language models.
"""
import subprocess
import sys

def download_spacy_model():
    """Download spaCy English language model"""
    try:
        print("Downloading spaCy English language model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ spaCy model downloaded successfully")
    except Exception as e:
        print(f"Warning: Could not download spaCy model: {e}")
        print("The app will work but NLP features may be limited")

if __name__ == "__main__":
    download_spacy_model()

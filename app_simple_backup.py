import streamlit as st

st.set_page_config(
    page_title="Pharma CI Platform",
    page_icon="💊",
    layout="wide"
)

st.title("🎉 Pharma CI Platform")
st.success("✅ App is running successfully!")

st.markdown("""
## Welcome to Pharma CI Platform

This is a pharmaceutical competitive intelligence monitoring platform.

### Features:
- 📊 Dashboard with key industry metrics
- 🔬 Competitor Pipeline tracking
- 📰 News Monitoring system
- 👥 KOL (Key Opinion Leader) Insights

### Status:
- ✅ Streamlit: Working
- ✅ Dependencies: Installed
- 🔄 Full features: Coming soon

The app is being configured for cloud deployment.
""")

st.sidebar.title("Navigation")
st.sidebar.info("Full navigation coming soon!")

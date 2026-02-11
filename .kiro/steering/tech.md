---
inclusion: always
---

# Technology Stack

## Core Technologies

- Python 3.11+
- Streamlit (web framework for the UI)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Alembic (database migrations)

## Key Libraries

- plotly: Interactive data visualizations
- pandas: Data manipulation and analysis
- biopython: Biological data processing
- spacy: Natural language processing
- textblob: Sentiment analysis
- trafilatura: Web scraping and text extraction
- psycopg2-binary: PostgreSQL adapter

## Package Management

- Uses uv/pyproject.toml for dependency management
- Dependencies defined in pyproject.toml [project.dependencies]

## Common Commands

### Database Operations
```bash
# Initialize database and seed with sample data
python init_db.py
```

### Running the Application
```bash
# Start the Streamlit application (runs on port 5000)
streamlit run app.py --server.port 5000
```

Note: In Replit, use the "Run" button which automatically starts the application.

## Environment Variables

Required environment variables (set in Replit Secrets or .env):
- DATABASE_URL: PostgreSQL connection string
- API_KEY: API key for external services (optional)

## Development Notes

- The application is designed to run on Replit
- Uses PostgreSQL for data persistence
- Streamlit provides the web interface with automatic reloading during development

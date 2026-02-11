---
inclusion: always
---

# Project Structure

## Directory Organization

```
├── app.py                    # Main Streamlit application entry point
├── init_db.py               # Database initialization and seeding script
├── components/              # UI components (Streamlit pages)
│   ├── dashboard.py         # Main dashboard with metrics and charts
│   ├── competitor_pipeline.py  # Pipeline tracking interface
│   ├── news_monitor.py      # News monitoring and sentiment analysis
│   ├── kol_insights.py      # KOL tracking and publications
│   └── __init__.py
├── models/                  # Data models and entity definitions
│   └── entities.py          # DrugEntity, CompanyEntity, KolEntity classes
├── utils/                   # Utility functions and helpers
│   ├── database.py          # SQLAlchemy models, DB operations, seeding
│   ├── visualization.py     # Plotly chart creation functions
│   ├── clinical_trials.py   # ClinicalTrials.gov API integration
│   ├── pubmed.py           # PubMed API integration
│   ├── fda.py              # FDA database integration
│   ├── news_scraper.py     # Web scraping for news articles
│   ├── text_processing.py  # NLP and text analysis utilities
│   ├── data_aggregation.py # Data aggregation and processing
│   └── __init__.py
├── migrations/              # Alembic database migrations
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
└── .streamlit/             # Streamlit configuration
    └── config.toml

```

## Architecture Patterns

### Component Structure
- Each component in `components/` is a self-contained Streamlit page
- Components use a `render_*()` function pattern (e.g., `render_dashboard()`)
- Navigation is handled via sidebar radio buttons in `app.py`

### Database Layer
- SQLAlchemy ORM models defined in `utils/database.py`
- Models: Company, Drug, NewsArticle, KOL, Publication
- Database initialization and seeding functions in same file
- Session management using `SessionLocal` factory pattern

### Visualization Pattern
- All chart creation functions in `utils/visualization.py`
- Functions follow naming: `create_*_chart()`
- Return Plotly figure objects
- Accept pandas DataFrames or lists as input

### Data Models
- Entity classes in `models/entities.py` for business logic
- Separate from SQLAlchemy models (database layer)
- Include `to_dict()` methods for serialization

## Code Conventions

- Use docstrings for all functions and classes
- Type hints in function signatures where applicable
- Database operations use context managers or explicit session handling
- Error handling with try/except blocks, especially for database operations
- Streamlit components use `st.error()` for user-facing error messages

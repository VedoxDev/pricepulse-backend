# PricePulse Backend

Backend service for tracking product prices across multiple e-commerce platforms. Built with FastAPI, Celery, and PostgreSQL, the service exposes an HTTP API for managing tracked products and background tasks for periodic scraping.

## Features

- FastAPI application with modular routing under `app/`
- Async SQLAlchemy setup backed by PostgreSQL, powered by Pydantic-based settings
- Celery worker and beat configuration using Redis for broker/result backend
- Placeholder domain layers for models, schemas, scrapers, and tasks

## Getting Started

1. **Create and activate a virtual environment** (example with `venv`):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**: create a `.env` file in the project root. Example values:

   ```env
   PROJECT_NAME=PricePulse
   VERSION=0.1.0
   API_V1_PREFIX=/api/v1

   DATABASE_URL=postgresql://postgres:<password>@mainline.proxy.rlwy.net:46475/railway
   DATABASE_ECHO=false
   DATABASE_POOL_SIZE=5
   DATABASE_MAX_OVERFLOW=10
   DATABASE_POOL_TIMEOUT=30

   REDIS_URL=redis://localhost:6379/0
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   SCRAPE_INTERVAL_MINUTES=60
   ```

   > The application automatically adapts `postgresql://` URLs for async use (`postgresql+asyncpg://`), so you can paste connection strings from your provider directly.

4. **Run the FastAPI app**:

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Start Celery worker & beat** (in separate terminals):

   ```bash
   celery -A app.tasks.celery_app.celery_app worker --loglevel=info
   celery -A app.tasks.celery_app.celery_app beat --loglevel=info
   ```

## Project Structure

```
app/
├── core/            # Configuration & settings
├── db/              # Database base class and session management
├── models/          # SQLAlchemy models
├── routes/          # FastAPI routers
├── schemas/         # Pydantic schemas
├── scrapers/        # Scraper abstraction layer
└── tasks/           # Celery application and task definitions
```

## License

[MIT](LICENSE)

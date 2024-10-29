# Magazine Content Search API

A high-performance hybrid search API that enables searching across 1 million content records from 5,000 magazines using
keywords and various filters. The system implements a hybrid search architecture combining keyword-based and semantic
search capabilities for optimal results.

## Quick Links

- API Documentation: [ReDoc](https://hybrid-search-348886817567.us-central1.run.app/redoc)
- Test Interface: [Web UI](https://hybrid-search-webpage-348886817567.us-central1.run.app)

## Project Structure

```
project/
├── alembic/ # Database migrations
├── app/
│   ├── core/
│   │   ├── config.py # Environment variables
│   │   ├── db.py # Database related code
│   ├── models/ # SQLAlchemy models
│   ├── services/ # Business logic
│   │   ├── elasticsearch.py # Elasticsearch service implementation
│   │   └── search.py # Search service implementation
│   └── schemas.py # Pydantic schema definitions
├── scripts/
│   └── push_to_elasticsearch.py # Data push script for Elasticsearch
├── tests/
│   ├── test_search.py # Tests for search functionality
│   └── test_main.py # Tests for main endpoint
├── .env.example # Example environment variables
├── cloudbuild.yaml # Cloud Build configuration
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── main.py # Main application entry point
```

## Tech Stack

A fully async app implemented using the following modern technologies:

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Elasticsearch**: Primary search engine implementing hybrid search
- **PostgreSQL**: Permanent data storage
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool

## Data Store Architecture

- PostgreSQL serves as the system of record
- Elasticsearch handles all search operations with optimized indexing
- `scripts/push_to_elasticsearch.py` simulates real-time synchronization between PostgreSQL and Elasticsearch, which
  would be needed if this challenge included creating new magazine contents

### Quick Start with Existing Data

To test the API with pre-populated data, use the Elastic credentials included in `.dov.example`.

### If You Want To Set Up With Your Own Data (not recommended for simple app review)

1. Run database migrations:

    ```bash
    alembic upgrade head
    ```

2. Insert your magazine records according to the schema in `src/models.py`

3. Populate Elasticsearch:

    ```bash
    python scripts/push_to_elasticsearch.py
    ```

## Development

1. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/Mac
    venv\Scripts\activate # Windows
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    ```bash
    cp .env.example .env
    ```

4. Edit `.env` with your configurations

5. Run the development server:
    ```bash
    uvicorn main:app --port 8000
    ```

## Testing

```bash
pytest
```

## License

MIT
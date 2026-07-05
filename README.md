![Python](https://img.shields.io/badge/Python-3.14-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![CI](https://github.com/rory1337-prog/finance-etl-pipeline/actions/workflows/ci.yml/badge.svg)

# Finance ETL Pipeline

Production-ready ETL pipeline for collecting, transforming, and storing cryptocurrency market data from BingX.

The project demonstrates modern Python backend and data engineering practices: ETL architecture, SQLAlchemy 2.0, Alembic migrations, PostgreSQL, Docker, scheduling, automated testing, structured logging, Ruff, and GitHub Actions CI/CD.

Supported assets:

- BTC-USDT
- ETH-USDT
- BNB-USDT
- SOL-USDT

## Architecture

```text
              BingX REST API
                    │
                    ▼
              BingXProvider
                    │
                    ▼
                ETLService
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
AssetRepository PriceRepository MetricRepository
      │             │             │
      └─────────────┼─────────────┘
                    ▼
                PostgreSQL
                    │
                    ▼
            ETLRunRepository
```

## Tech Stack

- Python 3.14
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Docker / Docker Compose
- Pandas
- APScheduler
- Pytest
- Ruff
- GitHub Actions
- BingX REST API

## Features

- Multi-asset crypto ETL pipeline
- BingX market data extraction
- PostgreSQL persistence
- SQLAlchemy repository layer
- Alembic database migrations
- Technical indicators:
    - Daily Return
    - MA7
    - MA30
    - EMA20
    - Volatility
- CLI execution
- Daily scheduled execution
- ETL run logging
- Structured application logging
- Unit tests
- Ruff linting and formatting
- GitHub Actions CI

## Design Principles

- Layered Architecture
- Repository Pattern
- Dependency Injection
- Separation of Concerns
- Idempotent ETL Loads
- Transaction-based persistence
- Structured logging

## Project Structure

```text
finance-etl-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── db/
│   │   ├── models/
│   │   ├── base.py
│   │   └── session.py
│   ├── extract/
│   ├── pipeline/
│   ├── repositories/
│   ├── scheduler/
│   ├── services/
│   ├── transform/
│   ├── config.py
│   ├── constants.py
│   ├── logging_config.py
│   └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── requirements.txt
└── README.md
```

## Getting Started

```bash
git clone https://github.com/rory1337-prog/finance-etl-pipeline.git
cd finance-etl-pipeline

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Create .env from .env.example
```bash
cp .env.example .env
```

Required variables:
```bash 
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/finance_etl
BINGX_BASE_URL=https://open-api.bingx.com
DEFAULT_INTERVAL=1d
DEFAULT_LIMIT=365
```

### Database Setup

```bash
docker compose up -d
alembic upgrade head
```

### Running ETL

Run for all tracked assets:
```bash
python -m app.main --all
```
Run for a single asset:
```bash
python -m app.main --asset BTC-USDT
```

### Example Output

```text
2026-07-06 00:20:39,604 | INFO     | app.pipeline.runner | Finance ETL pipeline started
2026-07-06 00:20:39,962 | INFO     | app.services.etl_service | Loaded 0 candles for BTC-USDT
2026-07-06 00:20:40,007 | INFO     | app.services.etl_service | Saved 365 metrics for BTC-USDT
2026-07-06 00:20:40,007 | INFO     | app.pipeline.runner | BTC-USDT | candles=0 | metrics=365
2026-07-06 00:20:40,012 | INFO     | app.pipeline.runner | Finance ETL pipeline finished successfully | candles=0 | metrics=365
```

### Scheduler

```bash
python -m app.scheduler.scheduler
```
The scheduler runs the ETL pipeline daily at 00:00 UTC

### Testing

```bash
python -m pytest
```

### Linting and Formatting

```bash
ruff check .
ruff format --check .
```
Format code
```bash
ruff format .
```

## CI/CD

GitHub Actions automatically validates every push and pull request by:

- Running Ruff lint checks
- Verifying code formatting
- Starting a PostgreSQL service container
- Applying Alembic migrations
- Executing the Pytest test suite

## Database Schema

Main tables:

- `assets`
- `price_history`
- `daily_metrics`
- `etl_runs`

## Roadmap

- Repository integration tests
- Pipeline integration tests
- RSI / ATR / MACD indicators
- FastAPI read-only API
- Parquet export

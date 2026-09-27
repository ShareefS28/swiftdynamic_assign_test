## Setup

### 1. Start PostgreSQL (Docker)

```bash
docker compose up -d
```

This starts Postgres 16 with database `school_data_center`, user `postgres`,
password `postgres`, on port `5432` — matching the defaults in `settings.py`.

The database connection can be overridden via environment variables:
`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`,
`POSTGRES_PORT`.

### 2. Install dependencies

```bash
conda env create --file py310.yml
```

### 3. Migrate and run

```bash
python manage.py migrate
python manage.py runserver
```

### 4. Run the tests

```bash
python manage.py test
```

Database and Migrations

This project now uses SQLAlchemy for persistence and Alembic for migrations.

- To create the database (default SQLite at `mergington.db`):

  ```bash
  python -m src.seed
  ```

- To run Alembic migrations (requires `alembic` installed):

  ```bash
  alembic upgrade head
  ```

- Environment variable: `DATABASE_URL` (defaults to `sqlite:///./mergington.db`)

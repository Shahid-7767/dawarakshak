
import psycopg
from psycopg.rows import dict_row
from flask import current_app


def get_db():
    database_url = current_app.config.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env file."
        )

    return psycopg.connect(
        database_url,
        row_factory=dict_row
    )


def init_db():
    connection = get_db()

    try:
        # Medicine records
        connection.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                batch_id TEXT PRIMARY KEY,
                medicine_name TEXT NOT NULL,
                manufacturer TEXT NOT NULL,
                manufactured_on DATE NOT NULL,
                expires_on DATE NOT NULL,
                block_index INTEGER NOT NULL,
                block_hash TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Permanent blockchain storage
        connection.execute("""
            CREATE TABLE IF NOT EXISTS blockchain_blocks (
                block_index INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                transactions JSONB NOT NULL,
                previous_hash TEXT NOT NULL,
                block_hash TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()

import psycopg2
import psycopg2.pool
import os
from contextlib import contextmanager
from dotenv import load_dotenv
import json

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

_pool = psycopg2.pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URL)


@contextmanager
def get_conn():
    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


def create_table():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    vector VECTOR(1536)
                );
                """
            )


def create_questions_table():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id SERIAL PRIMARY KEY,
                    value TEXT NOT NULL,
                    answered BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


def add_question(value, answered=False):
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO questions (value, answered) VALUES (%s, %s);",
                    (value, answered),
                )
    except Exception as e:
        print(f"Error adding question: {e}")


def batch_insert_embeddings(chunks, embeddings):
    data_to_insert = [
        (chunks[i].page_content, json.dumps(embedding))
        for i, embedding in enumerate(embeddings)
    ]
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO embeddings (content, vector) VALUES (%s, %s)",
                data_to_insert,
            )


def create_index():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_embeddings_vector
                ON embeddings
                USING hnsw (vector vector_cosine_ops);
                """
            )


def search_embeddings(query_vector, top_k=5):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT content
                FROM embeddings
                ORDER BY vector <=> %s::vector
                LIMIT %s;
                """,
                (query_vector, top_k),
            )
            rows = cursor.fetchall()
    return [row[0] for row in rows]


def clear_embeddings_table():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM embeddings;")

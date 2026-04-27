import psycopg
from psycopg_pool import ConnectionPool
import os
from contextlib import contextmanager
from dotenv import load_dotenv
import json

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

_pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10)


@contextmanager
def get_conn():
    with _pool.connection() as conn:
        yield conn


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
        (chunk, json.dumps(embedding))
        for chunk, embedding in zip(chunks, embeddings)
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

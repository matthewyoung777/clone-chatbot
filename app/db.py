import psycopg2
import os
from dotenv import load_dotenv
import json

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


def create_table():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS embeddings (
                id SERIAL PRIMARY KEY,
                content TEXT,
                vector VECTOR(1536)
            );
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def batch_insert_embeddings(chunks, embeddings):
    """Insert multiple text contents and their embeddings into the database in one batch."""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        data_to_insert = [
            (chunks[i].page_content, json.dumps(embedding))
            for i, embedding in enumerate(embeddings)
        ]

        cursor.executemany(
            "INSERT INTO embeddings (content, vector) VALUES (%s, %s)", data_to_insert
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting embeddings: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_index():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_embeddings_vector 
        ON embeddings 
        USING hnsw (vector vector_cosine_ops);
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


def search_embeddings(query_vector, top_k=5):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Perform vector search using cosine similarity or other metrics
    cursor.execute(
        """
        SELECT content, vector
        FROM embeddings
        ORDER BY vector <-> %s::vector
        LIMIT %s;
        """,
        (query_vector, top_k),
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows  # This will contain the most relevant content based on the query


# create_index()

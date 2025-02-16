import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def insert_embedding(content: str, vector: list):
    """Insert a text content and its embedding into the database"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO embeddings (content, vector) VALUES (%s, %s)", (content, vector)
    )
    conn.commit()

    cursor.close()
    conn.close()


def search_similar_vectors(vector: list):
    """Find the most similar entries using pgvector"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT content, vector <=> %s AS similarity
        FROM embeddings
        ORDER BY similarity
        LIMIT 5;
    """,
        (vector,),
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results

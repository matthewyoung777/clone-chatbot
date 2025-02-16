import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
print(DATABASE_URL)
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

import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import batch_insert_embeddings, clear_embeddings_table
from app.embeddings import generate_embeddings, get_chunks_by_headers

load_dotenv()

document_path = "data/about.md"
with open(document_path, "r", encoding="utf-8") as f:
    markdown_text = f.read()

chunks = get_chunks_by_headers(markdown_text)
embeddings = generate_embeddings(chunks)
clear_embeddings_table()
batch_insert_embeddings(chunks, embeddings)
print(f"Embedded {len(chunks)} chunks.")

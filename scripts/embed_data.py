# %% import libraries
from pprint import pprint
from dotenv import load_dotenv
import os, sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import batch_insert_embeddings, clear_embeddings_table
from app.embeddings import generate_embeddings, get_chunks_by_headers

# %%
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


# %% Get the documents
document_path = "data/about.md"
with open(document_path, "r", encoding="utf-8") as file:
    markdown_text = file.read()


# %%
chunks = get_chunks_by_headers(markdown_text)

# %% Generate Embeddings and insert them to the database
embeddings = generate_embeddings(chunks)
clear_embeddings_table()
batch_insert_embeddings(chunks, embeddings)

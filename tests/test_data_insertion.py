# %% import libraries

from dotenv import load_dotenv
import os, sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import batch_insert_embeddings
from app.embeddings import get_chunks, generate_embeddings


load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


# %% Chunk the Docment
document_path = "../data/forgefitness.md"
chunks = get_chunks(document_path)
# %% Generate Embeddings and insert them to the database
embeddings = generate_embeddings(chunks)
batch_insert_embeddings(chunks, embeddings)

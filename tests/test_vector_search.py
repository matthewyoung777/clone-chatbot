# %% import libraries
import os, sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import search_embeddings
from app.embeddings import generate_query_embedding

from app.queries import ask_gpt
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


# %% Receive a query and generate an embedding for it
query = "What are the features of ForgeFitness?"
query_embedding = generate_query_embedding(query)

# %% Run a vector simliarity search and return the results (chunks)
search_results = search_embeddings(query_embedding)

# %%
# for result in search_results:
#     print(f"Content: {result[0]}")
# %%

answer = ask_gpt(search_results, query)

print(answer.content)
# print(answer.response_metadata)

# %%

# %%
import psycopg2
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_openai import OpenAIEmbeddings
from db import batch_insert_embeddings


load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def chunking(document_path: str):
    loader = UnstructuredMarkdownLoader(document_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def generate_embeddings(chunks, batch_size=10):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # 8192 token limit
    all_embeddings = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        batch_embeddings = embeddings.embed_documents(
            [chunk.page_content for chunk in batch]
        )
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


def generate_query_embedding(query):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    query_embedding = embeddings.embed_query(query)  # Get embedding for the query
    return query_embedding


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


# %%

document_path = "../data/forgefitness.md"
chunks = chunking(document_path)
# %%
embeddings = generate_embeddings(chunks)
batch_insert_embeddings(chunks, embeddings)


# %%
# Example usage
query = "What is the tech stack of Forge Fitness?"
query_embedding = generate_query_embedding(query)

# %%
search_results = search_embeddings(query_embedding)

# %%
for result in search_results:
    print(f"Content: {result[0]}")

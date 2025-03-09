# %%
import os
from dotenv import load_dotenv
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
)
from langchain_openai import OpenAIEmbeddings


load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def get_chunks_by_headers(documents):

    headers = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    text_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers, strip_headers=True
    )
    chunks = text_splitter.split_text(documents)
    for chunk in chunks:
        chunk_headers = " ".join(chunk.metadata.values())
        chunk.page_content = f"{chunk_headers} {chunk.page_content}"
    return chunks


def generate_embeddings(chunks, batch_size=5):
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

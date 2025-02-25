# %%
import os
from dotenv import load_dotenv
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
)
import os
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
)
from langchain_openai import OpenAIEmbeddings


load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def get_chunks(document_path: str):
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


def get_chunks_by_headers(document_path: str):
    loader = UnstructuredMarkdownLoader(document_path)
    documents = loader.load()
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    text_splitter = MarkdownTextSplitter(headers_to_split_on=headers_to_split_on)
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

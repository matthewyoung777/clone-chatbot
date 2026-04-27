import re
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = OpenAI()
_EMBEDDING_MODEL = "text-embedding-3-small"


def get_chunks_by_headers(text):
    """Split markdown by header hierarchy, prepending a breadcrumb to each chunk."""
    header_re = re.compile(r'^(#{1,3}) (.+)$', re.MULTILINE)
    matches = list(header_re.finditer(text))

    active_headers = {}  # level (1/2/3) -> header text
    chunks = []

    for i, match in enumerate(matches):
        level = len(match.group(1))
        header = match.group(2).strip()

        active_headers[level] = header
        active_headers = {k: v for k, v in active_headers.items() if k <= level}

        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[content_start:content_end].strip()

        if content:
            breadcrumb = " ".join(active_headers[l] for l in sorted(active_headers))
            chunks.append(f"{breadcrumb} {content}")

    return chunks


def generate_embeddings(chunks, batch_size=4):
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        response = _client.embeddings.create(model=_EMBEDDING_MODEL, input=batch)
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings


def generate_query_embedding(query):
    response = _client.embeddings.create(model=_EMBEDDING_MODEL, input=query)
    return response.data[0].embedding

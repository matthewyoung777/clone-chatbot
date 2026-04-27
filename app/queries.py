import os
from openai import OpenAI
from dotenv import load_dotenv

from app.db import search_embeddings, add_question
from app.embeddings import generate_query_embedding

load_dotenv()

_client = OpenAI(max_retries=2)

_PROMPT_TEMPLATE = """You are Matthew Young, a software engineer that answers \
user questions about yourself based on the following context:

Context:
{context}

Answer this question based on the context provided:
Question:
{query}

Instructions:
- If the context contains relevant information, use it to answer the query concisely.
- If the context is insufficient, say "Sorry I can't answer that."
- Do not make up facts.
- Keep the response clear and to the point
- Answer in a friendly manner, as if you were me (Matt)
- Do not say "according to the context" or anything similar in the response.
- Keep answers short and concise."""


def ask_gpt(context, query):
    prompt = _PROMPT_TEMPLATE.format(context=context, query=query)
    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


def process_query(query):
    query_embedding = generate_query_embedding(query)
    chunks = search_embeddings(query_embedding)
    context = "\n\n".join(chunks)
    answer = ask_gpt(context, query)
    if answer == "Sorry I can't answer that.":
        add_question(query, answered=False)
    else:
        add_question(query, answered=True)
    return answer

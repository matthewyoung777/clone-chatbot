# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Python FastAPI backend for a RAG (Retrieval-Augmented Generation) chatbot that answers questions about the owner (Matthew Young) using content stored in a PostgreSQL pgvector database. Deployed on Render.

## Required Environment Variables

```
OPENAI_API_KEY    # OpenAI API key for embeddings and LLM
DATABASE_URL      # PostgreSQL connection string (must have pgvector extension)
CHATBOT_API_KEY   # Secret key required in X-API-KEY header for all requests
```

## Dependencies

Install:
```bash
pip install "psycopg[binary]" psycopg-pool openai fastapi "uvicorn[standard]" gunicorn \
            slowapi python-dotenv
```

Remove if present (replaced by raw openai SDK):
```
langchain langchain-community langchain-core langchain-openai langchain-text-splitters langsmith
```

## Commands

```bash
# Run dev server (auto-reload)
uvicorn app.main:app --reload
# or
python run.py

# Run production server (matches Procfile)
gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app

# Run tests
python -m pytest tests/test_app.py -v

# Re-embed knowledge base after editing data/about.md
python scripts/embed_data.py
```

## Architecture

### Request Flow

```
POST /ask  →  auth.py (validate X-API-KEY)
           →  queries.py::process_query()
                ├── embeddings.py::generate_query_embedding()   # embed the user query
                ├── db.py::search_embeddings()                  # cosine similarity, top 5
                ├── queries.py::ask_gpt()                       # gpt-4o-mini with RAG prompt
                └── db.py::add_question()                       # log query + answered flag
```

### Data Embedding Pipeline

`data/about.md` is the single source of truth for the knowledge base. To update what the chatbot knows, edit that file then re-run `scripts/embed_data.py`, which:

1. Splits the markdown by header hierarchy using a custom regex splitter (`get_chunks_by_headers`)
2. Prepends header breadcrumbs to each chunk's text (e.g. `"Projects Forge Fitness Overview <body>"`)
3. Batch-embeds chunks with OpenAI `text-embedding-3-small` (1536 dimensions)
4. Clears and replaces the `embeddings` table

### Database Tables

- **`embeddings`** — `(id, content TEXT, vector VECTOR(1536))` — HNSW index on vector column using cosine ops
- **`questions`** — `(id, value TEXT, answered BOOL, created_at TIMESTAMP)` — logs every query for review

### Key Design Decisions

- All routes require the `X-API-KEY` header (enforced globally via `FastAPI(dependencies=[Depends(validate_api_key)])`).
- Rate limiting on `POST /ask` is 10 requests/minute per IP via SlowAPI.
- CORS is restricted to `localhost:3000` (dev) and `matthewyoung.info` (production).
- The LLM prompt instructs the model to reply as Matthew in first person; if context is insufficient it returns the literal string `"Sorry I can't answer that."` — `process_query` checks for this exact string to set the `answered` flag.
- `db.py` uses a `psycopg_pool.ConnectionPool` (1–10 connections) accessed via a `get_conn()` context manager that handles commit/rollback/return automatically. psycopg3 (`psycopg`) is used, not the older psycopg2.
- `app/embeddings.py` and `app/queries.py` each hold a module-level `OpenAI` client singleton to avoid re-instantiation per request.
- `get_chunks_by_headers` returns plain `List[str]` — no LangChain Document objects anywhere in the pipeline.

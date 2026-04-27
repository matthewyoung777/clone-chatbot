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

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run dev server (auto-reload)
uvicorn app.main:app --reload
# or
python run.py

# Run production server (matches Procfile)
gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app

# Re-embed knowledge base after editing data/about.md
python scripts/embed_data.py

# Interactive RAG test (CLI loop — requires DB + OpenAI access)
python tests/test_vector_search.py

# Inspect data chunking output without inserting
python tests/test_data_insertion.py
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

1. Splits the markdown by header hierarchy using LangChain's `MarkdownHeaderTextSplitter`
2. Prepends header breadcrumbs to each chunk's text (so the vector captures context)
3. Batch-embeds chunks with OpenAI `text-embedding-ada-002` (1536 dimensions)
4. Clears and replaces the `embeddings` table

### Database Tables

- **`embeddings`** — `(id, content TEXT, vector VECTOR(1536))` — HNSW index on vector column using cosine ops
- **`questions`** — `(id, value TEXT, answered BOOL, created_at TIMESTAMP)` — logs every query for review

### Key Design Decisions

- All routes require the `X-API-KEY` header (enforced globally via `FastAPI(dependencies=[Depends(validate_api_key)])`). The `/wake` and `/` health-check routes are also gated.
- Rate limiting on `POST /ask` is 10 requests/minute per IP via SlowAPI.
- CORS is restricted to `localhost:3000` (dev) and `matthewyoung.info` (production).
- The LLM prompt instructs the model to reply as Matthew in first person; if context is insufficient it returns the literal string `"Sorry I can't answer that."` — `process_query` checks for this exact string to set the `answered` flag.
- `db.py` uses raw `psycopg2` (not SQLAlchemy) with per-call connection management.
- `embeddings.py` and `queries.py` both call `load_dotenv()` independently; env vars are loaded module-level.

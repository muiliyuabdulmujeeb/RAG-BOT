# RAG PDF QA Bot

A multi-service PDF question-answering system built to explore retrieval, token-aware chunking, pgvector search, and local LLM inference.
Instead of treating RAG as a thin wrapper around embeddings and prompting, it splits the workflow into separate services for ingestion, chunking, embedding, retrieval, and answer generation.

## Overview

This project is best described as a practical AI systems project focused on retrieval quality, latency, local inference constraints, and backend service design. It is built around a simple question:

> what does it take to make a local-inference document QA system useful in practice?

And the answer goes far beyond storing embeddings and retrieving chunks.

The more interesting work in this repository sits in the tradeoffs around:

- chunking strategy
- embedding quality
- retrieval quality
- local model constraints
- latency
- service boundaries


## What The System Does

At a high level, the system:

1. accepts a PDF document
2. extracts text page by page
3. chunks the text using tokenizer-aware logic
4. generates normalized embeddings for the chunks
5. stores chunk content and vectors in PostgreSQL with pgvector
6. embeds an incoming user query
7. retrieves the most relevant chunks by vector similarity
8. sends retrieved context to a generation service backed by Ollama
9. returns an answer plus the retrieved supporting chunks

## Why This Project Matters

What makes this project interesting is that the hard part is not the happy-path demo.

The harder part is building a pipeline that makes reasonable engineering choices under real constraints:

- the embedding model has token limits
- chunk size and overlap affect retrieval quality
- local inference introduces latency and hardware constraints
- response quality depends on retrieval quality, not only the LLM
- the system becomes easier to reason about when service responsibilities are separated cleanly

## Architecture Summary

The repository is split into three application services plus infrastructure:

- `rag_api`
  - handles document upload, persistence, retrieval orchestration, and the main user-facing API
- `embedding_service`
  - handles tokenizer-aware chunking and embedding generation
- `generation_service`
  - handles answer generation through Ollama-backed local inference
- `PostgreSQL + pgvector`
  - stores documents and metadata, chunks, and vector embeddings
- `Ollama`
  - serves the local generation model

This architecture keeps the main concerns separated:

- ingestion and persistence
- embedding and chunking
- answer generation

That separation makes it easier to reason about latency, service boundaries, and future scaling decisions.

## Implementation Details That Matter

Several implementation choices that make this project more than a surface-level RAG project includes:

- chunking is token-aware, not character-count based
- chunking uses overlap to preserve context across chunk boundaries
- embeddings are normalized before storage and retrieval
- vectors are stored in pgvector with a 384-dimensional embedding column
- retrieval uses cosine distance over stored chunk embeddings
- answer generation is routed through a separate generation service instead of being mixed directly into the main API layer
- the compose stack automatically pulls a local Ollama model for generation

Current model and retrieval details used:

- embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- embedding dimension: `384`
- generation model: `llama3.2:3b`
- default chunk size: `200` tokens
- default overlap: `40` tokens

## Current API Surface

Main API routes currently exposed by `rag_api`:

- `POST /documents/upload`
  - uploads and processes a PDF
- `GET /documents`
  - lists processed documents
- `POST /chat/query`
  - accepts a question plus selected document ids and returns:
    - an answer
    - retrieved supporting chunks

Supporting internal services expose:

- `POST /embed`
- `POST /chunk`
- `POST /generate`

Health endpoints exist on each service.

## Repository Layout

- `rag_api/`
  - main FastAPI application, database models, retrieval flow, and API routes
- `embedding_service/`
  - tokenizer-aware chunking and embedding generation service
- `generation_service/`
  - Ollama-backed answer generation service
- `docker-compose.yml`
  - local multi-service runtime
- `test_qa.txt`
  - sample output and QA artifact from local runs for debugging and solving arising issues

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
- Docker Compose
- Ollama
- sentence-transformers
- transformers
- pypdf
- httpx

## Local Setup

### Prerequisites

- Docker
- Docker Compose

### 1. Create a root `.env`

The compose stack expects a root `.env` file, but the repository does not currently include a committed `.env.example`.

At minimum, the API settings expect:

- `DATABASE_URL`
- `EMBEDDING_SERVICE_URL`
- `GENERATION_SERVICE_URL`

For the local Compose setup, the service URLs should point to the internal container names:

- `EMBEDDING_SERVICE_URL=http://embedding_api:8001`
- `GENERATION_SERVICE_URL=http://generation_service:8002`

### 2. Start the stack

```bash
docker compose up --build
```

The compose setup includes:

- `db` - pgvector-enabled PostgreSQL
- `ollama` - local model runtime
- `ollama-pull` - one-shot model pull for `llama3.2:3b`
- `embedding_api` - embedding and chunking service
- `generation_service` - answer generation service
- `api` - main RAG API

### 3. Default service ports

- API: [http://localhost:8000](http://localhost:8000)
- Embedding service: [http://localhost:8001](http://localhost:8001)
- Generation service: [http://localhost:8002](http://localhost:8002)
- Ollama: [http://localhost:11434](http://localhost:11434)

## Current Challenges

The main engineering challenges in this project are:

- reducing end-to-end latency
- improving answer coherence and naturalness
- choosing local models that fit hardware constraints
- balancing chunk size with retrieval quality
- making the system more robust as document size and query complexity grow

## Current Status

This project is still in progress as the challenges are being addressed using different methods to ffind the best middlegrounds between tradeoffs.
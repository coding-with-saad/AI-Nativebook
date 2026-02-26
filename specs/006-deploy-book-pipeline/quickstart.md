# Quickstart: Embedding Pipeline

This document provides a guide for setting up and running the embedding pipeline for the Docusaurus book.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed.
- Cohere API Key (Trial/Free tier).
- Qdrant Cloud API Key and Cluster URL (Free tier).

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <repo-root>
   ```

2. **Initialize Backend**:
   ```bash
   cd backend
   uv sync
   ```

3. **Configure Environment Variables**:
   Create a `backend/.env` file:
   ```env
   COHERE_API_KEY=your-cohere-key
   QDRANT_URL=your-qdrant-cluster-url
   QDRANT_API_KEY=your-qdrant-api-key
   BOOK_BASE_URL=https://your-github-pages-url.io
   ```

## Running the Pipeline

To run the full ingestion flow:
```bash
uv run python main.py
```

The pipeline will:
1. Extract content from the deployed book.
2. Chunk the markdown content (~500 tokens).
3. Generate embeddings using Cohere `embed-english-v3.0`.
4. Store vectors in Qdrant with stable IDs for idempotency.

## Verification

After running, verify the ingestion in Qdrant Cloud dashboard:
- Collection name: `ai_native_book`
- Vector dimension: 1024
- Check that `module` and `url` metadata are present.

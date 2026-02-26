# AI Native Book - Embedding Pipeline

This directory contains the Python script for the embedding pipeline. The pipeline extracts content from the deployed Docusaurus book, chunks it, generates embeddings using Cohere, and stores them in a Qdrant vector database.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Python package installer and virtual environment manager)
- API keys for Cohere and Qdrant Cloud.

## Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and install dependencies**:
    `uv` will automatically create a virtual environment (`.venv`) and install the packages listed in `pyproject.toml`.
    ```bash
    uv sync
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file by copying the template:
    ```bash
    cp .env.template .env
    ```
    Then, edit the `.env` file and add your credentials:
    ```env
    COHERE_API_KEY="your-cohere-api-key"
    QDRANT_URL="https://your-qdrant-cluster-url.qdrant.tech:6333"
    QDRANT_API_KEY="your-qdrant-api-key"
    BOOK_BASE_URL="https://your-github-username.github.io/your-repo-name/"
    ```

## Running the Pipeline

To run the full ingestion pipeline, execute the `main.py` script from within the `backend` directory:

```bash
uv run python main.py
```

The script will:
1.  Fetch content from the `BOOK_BASE_URL`.
2.  Chunk the content into smaller documents.
3.  Generate embeddings using Cohere's `embed-english-v3.0` model.
4.  Upsert the documents and their vectors into your Qdrant collection, specified as `ai_native_book`.

## Verification

You can verify the pipeline's success by:
-   Checking the logs in your terminal for success messages.
-   Navigating to your Qdrant Cloud dashboard and inspecting the `ai_native_book` collection to see the number of points and their metadata.

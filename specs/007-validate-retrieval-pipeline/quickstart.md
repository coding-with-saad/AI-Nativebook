# Quickstart for Retrieval Pipeline Validation

This guide explains how to set up and run the retrieval validation script.

## Prerequisites

1.  **Python 3.11** or later.
2.  A **Qdrant Cloud** account (Free Tier is sufficient).
3.  A **Cohere API key**.

## Setup

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt 
    ```
    *(Note: a `requirements.txt` will be created as part of the implementation)*

2.  **Set environment variables**:
    Create a `.env` file in the `backend` directory with the following content:
    ```
    QDRANT_URL="..."
    QDRANT_API_KEY="..."
    COHERE_API_KEY="..."
    ```

## Running the script

To run the validation script, execute the following command from the root of the repository:

```bash
python backend/retrieve.py "your query here"
```

The script will output the most relevant chunks from the Qdrant database for your query.

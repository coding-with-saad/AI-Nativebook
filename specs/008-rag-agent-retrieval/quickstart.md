# Quickstart: RAG Agent with Retrieval Pipeline

**Feature Branch**: `008-rag-agent-retrieval` | **Date**: 2026-02-27 | **Plan**: [specs/008-rag-agent-retrieval/plan.md]
**Spec**: [specs/008-rag-agent-retrieval/spec.md]

This document provides instructions to quickly set up and run the RAG Agent with Retrieval Pipeline.

## Prerequisites

- Python 3.9+
- `pip` for package management
- Access to OpenAI API, Cohere API, and Qdrant Cloud.

## Setup

1.  **Clone the repository (if not already done):**
    ```bash
    git clone <repository-url>
    cd ai-native-book
    git checkout 008-rag-agent-retrieval
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install qdrant-client cohere pandas pytest openai-agents python-dotenv
    ```
    (Note: `python-dotenv` is required for loading .env files)

4.  **Set up Environment Variables:**
    Create a `.env` file in the project root with your API keys and Qdrant configuration:
    ```ini
    OPENAI_API_KEY="your_openai_api_key_here"
    COHERE_API_KEY="your_cohere_api_key_here"
    QDRANT_URL="your_qdrant_cloud_url_here"
    QDRANT_API_KEY="your_qdrant_api_key_here"
    QDRANT_COLLECTION_NAME="rag_book_collection" # Or your actual collection name
    ```

## Running the RAG Agent

The core agent logic is in `src/agent.py` and the retrieval pipeline is in `src/retrieval_pipeline.py`.

1.  **Ensure Qdrant Collection is Populated:**
    This quickstart assumes you have already ingested your book embeddings into the specified Qdrant collection (`QDRANT_COLLECTION_NAME`).

2.  **Execute the agent:**
    You can run the agent from your terminal as a command-line tool.

## Example Query

Once the agent is running, you can interact with it. Assuming a simple CLI interface:

```bash
# Example: Sending a query
python src/agent.py --query "Summarize the key plot points of 'Pride and Prejudice'."
```

The agent should return an answer grounded in the retrieved content from your Qdrant collection, along with the sources.

**Expected Output Example:**
```
Answer: The key plot points of 'Pride and Prejudice' revolve around Elizabeth Bennet, who navigates societal expectations and personal biases to find love with Mr. Darcy...
Sources: [pride_and_prejudice_chunk_1, pride_and_prejudice_chunk_5]
```

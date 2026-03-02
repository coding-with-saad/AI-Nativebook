import pytest
import os
import cohere
from unittest.mock import MagicMock, patch
from src.retrieval_pipeline import get_embedding, search_qdrant
from qdrant_client.http.models import ScoredPoint

# Mock Cohere client for testing
@pytest.fixture
def mock_cohere_client():
    with patch('cohere.Client') as mock_client:
        mock_instance = MagicMock()
        mock_instance.embed.return_value = MagicMock(embeddings=[[0.1, 0.2, 0.3]])
        mock_client.return_value = mock_instance
        yield mock_instance

# Mock Qdrant client for testing
@pytest.fixture
def mock_qdrant_client():
    with patch('qdrant_client.QdrantClient') as mock_client:
        mock_instance = MagicMock()
        # Mocking search method to return a list of ScoredPoint objects
        mock_instance.search.return_value = [
            ScoredPoint(
                id="1", score=0.9, payload={"content": "chunk 1", "source_book_id": "book_a", "text_chunk_id": "chunk_a1"}
            ),
            ScoredPoint(
                id="2", score=0.8, payload={"content": "chunk 2", "source_book_id": "book_a", "text_chunk_id": "chunk_a2"}
            )
        ]
        mock_client.return_value = mock_instance
        yield mock_instance

def test_get_embedding_success(mock_cohere_client):
    """
    Test that get_embedding successfully generates an embedding.
    """
    os.environ["COHERE_API_KEY"] = "mock_key"
    text = "test text"
    embedding = get_embedding(text)

    mock_cohere_client.embed.assert_called_once_with(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    assert embedding == [0.1, 0.2, 0.3]

def test_get_embedding_missing_api_key():
    """
    Test that get_embedding raises an error if COHERE_API_KEY is missing.
    """
    if "COHERE_API_KEY" in os.environ:
        del os.environ["COHERE_API_KEY"]
    
    with pytest.raises(ValueError, match="COHERE_API_KEY environment variable not set."):
        get_embedding("test text")

def test_get_embedding_input_type():
    """
    Test that get_embedding correctly passes input_type.
    """
    os.environ["COHERE_API_KEY"] = "mock_key"
    text = "test query"
    input_type = "search_query"
    embedding = get_embedding(text, input_type=input_type)

    mock_cohere_client.embed.assert_called_once_with(
        texts=[text], model="embed-english-v3.0", input_type=input_type
    )
    assert embedding == [0.1, 0.2, 0.3]

# --- Tests for search_qdrant ---
def test_search_qdrant_success(mock_qdrant_client):
    """
    Test that search_qdrant successfully retrieves results.
    """
    os.environ["QDRANT_URL"] = "http://mock-qdrant.com"
    os.environ["QDRANT_API_KEY"] = "mock_qdrant_key"
    os.environ["QDRANT_COLLECTION_NAME"] = "mock_collection"

    query_embedding = [0.4, 0.5, 0.6]
    top_k = 2
    results = search_qdrant(query_embedding, top_k)

    mock_qdrant_client.search.assert_called_once_with(
        collection_name="mock_collection",
        query_vector=query_embedding,
        limit=top_k,
        query_timeout=10000,
    )
    assert len(results) == 2
    assert results[0]["content"] == "chunk 1"
    assert results[0]["relevance_score"] == 0.9

def test_search_qdrant_missing_env_vars():
    """
    Test that search_qdrant raises an error if environment variables are missing.
    """
    if "QDRANT_URL" in os.environ: del os.environ["QDRANT_URL"]
    if "QDRANT_API_KEY" in os.environ: del os.environ["QDRANT_API_KEY"]
    if "QDRANT_COLLECTION_NAME" in os.environ: del os.environ["QDRANT_COLLECTION_NAME"]

    with pytest.raises(ValueError, match="QDRANT_URL, QDRANT_API_KEY, and QDRANT_COLLECTION_NAME environment variables must be set."):
        search_qdrant([0.1, 0.2, 0.3])

def test_search_qdrant_no_results(mock_qdrant_client):
    """
    Test that search_qdrant handles no results gracefully.
    """
    mock_qdrant_client.search.return_value = [] # Mock no results

    os.environ["QDRANT_URL"] = "http://mock-qdrant.com"
    os.environ["QDRANT_API_KEY"] = "mock_qdrant_key"
    os.environ["QDRANT_COLLECTION_NAME"] = "mock_collection"

    query_embedding = [0.4, 0.5, 0.6]
    top_k = 2
    results = search_qdrant(query_embedding, top_k)

    assert len(results) == 0

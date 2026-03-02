import pytest
from unittest.mock import MagicMock, patch
import os

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "mock_openai_key",
        "COHERE_API_KEY": "mock_cohere_key",
        "QDRANT_URL": "http://mock-qdrant.com",
        "QDRANT_API_KEY": "mock_qdrant_key",
        "QDRANT_COLLECTION_NAME": "mock_collection"
    }):
        yield

# Mock the RAGAgent's external dependencies
@pytest.fixture
def mock_rag_agent_dependencies():
    with patch('src.retrieval_pipeline.get_embedding') as mock_get_embedding, 
         patch('src.retrieval_pipeline.search_qdrant') as mock_search_qdrant, 
         patch('openai_agents.Agent.run') as mock_agent_run:
        
        # Configure mocks
        mock_get_embedding.return_value = [0.1, 0.2, 0.3]
        mock_search_qdrant.return_value = [
            {"content": "Relevant content 1.", "source_book_id": "book_a", "text_chunk_id": "chunk_a1"},
            {"content": "Relevant content 2.", "source_book_id": "book_b", "text_chunk_id": "chunk_b1"}
        ]
        # Mock the agent's run method to return a predefined response
        mock_agent_run.return_value = {
            "answer": "This is a mocked answer based on retrieved context.",
            "sources": ["book_a:chunk_a1", "book_b:chunk_b1"]
        }
        
        yield mock_get_embedding, mock_search_qdrant, mock_agent_run

def test_e2e_query_processing(mock_rag_agent_dependencies):
    """
    Simulates an end-to-end query processing call to the RAG agent (conceptual API).
    This test will involve creating a conceptual 'app' or entry point for the agent.
    """
    from src.agent import RAGAgent
    # Re-import RAGAgent here to ensure it uses the mocked dependencies
    # from the fixture, as it might have been imported before patching.

    rag_agent = RAGAgent()
    user_query = "What is the main topic of the documents?"

    # Simulate the API call to the RAG agent (e.g., through a conceptual 'handle_query' function)
    # For now, we directly call the agent's run_query method, which will be the entry point.
    response = rag_agent.run_query(user_query)

    # Assertions based on the expected behavior of the full pipeline
    mock_rag_agent_dependencies[0].assert_called_once_with(user_query, input_type="search_query") # get_embedding
    mock_rag_agent_dependencies[1].assert_called_once() # search_qdrant called
    mock_rag_agent_dependencies[2].assert_called_once() # agent.run called

    assert "answer" in response
    assert "sources" in response
    assert response["answer"] == "This is a mocked answer based on retrieved context."
    assert "book_a:chunk_a1" in response["sources"]
    assert "book_b:chunk_b1" in response["sources"]

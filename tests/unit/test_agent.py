import pytest
import os
from unittest.mock import MagicMock, patch
from src.agent import RAGAgent

# Mock for OpenAI Agents SDK Agent and its run_query method
@pytest.fixture
def mock_openai_agent():
    with patch('openai_agents.Agent') as mock_agent_class:
        mock_instance = MagicMock()
        mock_instance.name = "Test Agent"
        mock_instance.instructions = "Default instructions."
        mock_agent_class.return_value = mock_instance
        yield mock_instance

# Mock for the context formatting function (to be implemented in agent.py)
# This test will initially fail because _format_context is not implemented
def test_format_context_with_xml_tags(mock_openai_agent):
    """
    Test that the agent correctly formats retrieved context using XML-like tags.
    This test assumes a _format_context method will be added to RAGAgent.
    """
    rag_agent = RAGAgent(instructions="Test instructions") # Initialize RAGAgent, which uses mock_openai_agent
    
    mock_chunks = [
        {"content": "First chunk content.", "source_book_id": "book1", "text_chunk_id": "b1c1"},
        {"content": "Second chunk content.", "source_book_id": "book2", "text_chunk_id": "b2c2"},
    ]
    
    expected_formatted_context = """<context>
  <chunk source="book1:b1c1">First chunk content.</chunk>
  <chunk source="book2:b2c2">Second chunk content.</chunk>
</context>"""

    # Manually call the method that will be created
    # This will fail until _format_context is added to RAGAgent
    formatted_context = rag_agent._format_context(mock_chunks)
    assert formatted_context == expected_formatted_context

# --- Tests for hallucination check logic ---
def test_check_groundedness_success(mock_openai_agent):
    """
    Test that _check_groundedness returns True when answer is grounded.
    """
    rag_agent = RAGAgent(instructions="Test instructions")
    answer = "The quick brown fox is fast."
    context = "The quick brown fox is a fast animal. It jumps over the lazy dog."
    assert rag_agent._check_groundedness(answer, context) is True

def test_check_groundedness_failure(mock_openai_agent):
    """
    Test that _check_groundedness returns False when answer contains ungrounded facts.
    """
    rag_agent = RAGAgent(instructions="Test instructions")
    answer = "The quick brown fox is also very blue."
    context = "The quick brown fox is a fast animal. It jumps over the lazy dog."
    assert rag_agent._check_groundedness(answer, context) is False

def test_check_groundedness_empty_context(mock_openai_agent):
    """
    Test that _check_groundedness handles empty context.
    """
    rag_agent = RAGAgent(instructions="Test instructions")
    answer = "The quick brown fox is fast."
    context = ""
    assert rag_agent._check_groundedness(answer, context) is False

# --- Tests for error handling ---
def test_rag_agent_init_missing_openai_api_key():
    """
    Test that RAGAgent initialization raises ValueError if OPENAI_API_KEY is missing.
    """
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable not set."):
        RAGAgent()

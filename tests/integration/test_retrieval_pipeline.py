# test_retrieval_pipeline.py

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from dotenv import load_dotenv
import time

# Add the backend directory to the Python path to import retrieve.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from retrieve import initialize_clients, generate_embedding, search_qdrant, display_results, parse_arguments, main

# Load environment variables for potential use in tests (e.g., for config)
load_dotenv()

# Mocking constants for testing
MOCK_COLLECTION_NAME = "my_collection"
MOCK_EMBEDDING_DIMENSION = 1024 # Common dimension for many embedding models
PERFORMANCE_THRESHOLD_SECONDS = 5 # Placeholder for performance assertion

class TestRetrievalPipeline(unittest.TestCase):

    @patch('retrieve.load_dotenv')
    @patch('retrieve.os.getenv')
    def test_initialize_clients_success(self, mock_getenv, mock_load_dotenv):
        """Tests successful initialization of Cohere and Qdrant clients."""
        mock_getenv.side_effect = lambda key: {
            "COHERE_API_KEY": "fake_cohere_key",
            "QDRANT_URL": "http://localhost:6333",
            "QDRANT_API_KEY": "fake_qdrant_key"
        }.get(key)

        mock_qdrant_client = MagicMock(spec=QdrantClient)
        mock_qdrant_client.get_collections.return_value = MagicMock() # Mock successful collection retrieval
        mock_cohere_client = MagicMock(spec=cohere.Client)

        with patch('retrieve.QdrantClient', return_value=mock_qdrant_client) as MockQdrantClient, \
             patch('retrieve.cohere.Client', return_value=mock_cohere_client) as MockCohereClient:
            
            cohere_client, qdrant_client = initialize_clients()

            mock_cohere_client.assert_called_once_with(api_key="fake_cohere_key")
            MockQdrantClient.assert_called_once_with(url="http://localhost:6333", api_key="fake_qdrant_key")
            mock_qdrant_client.get_collections.assert_called_once()
            self.assertIsNotNone(cohere_client)
            self.assertIsNotNone(qdrant_client)

    @patch('retrieve.load_dotenv')
    @patch('retrieve.os.getenv')
    def test_initialize_clients_missing_env(self, mock_getenv, mock_load_dotenv):
        """Tests client initialization failure due to missing environment variables."""
        mock_getenv.side_effect = lambda key: {"COHERE_API_KEY": "fake_cohere_key"}.get(key) # Missing Qdrant
        
        with self.assertRaises(SystemExit) as cm:
            initialize_clients()
        self.assertEqual(cm.exception.code, 1)

    @patch('retrieve.load_dotenv')
    @patch('retrieve.os.getenv')
    @patch('retrieve.cohere.Client')
    @patch('retrieve.QdrantClient')
    def test_generate_embedding_success(self, MockQdrantClient, MockCohereClient, mock_getenv, mock_load_dotenv):
        """Tests successful embedding generation."""
        mock_getenv.side_effect = lambda key: {"COHERE_API_KEY": "fake_key"}.get(key)
        mock_cohere_client = MockCohereClient.return_value
        mock_cohere_client.embed.return_value.embeddings = [[0.1] * MOCK_EMBEDDING_DIMENSION] # Mock embedding
        
        embedding = generate_embedding(mock_cohere_client, "a sample query")
        self.assertIsNotNone(embedding)
        self.assertEqual(len(embedding), MOCK_EMBEDDING_DIMENSION)

    @patch('retrieve.load_dotenv')
    @patch('retrieve.os.getenv')
    @patch('retrieve.cohere.Client')
    def test_generate_embedding_no_embeddings(self, MockCohereClient, mock_getenv, mock_load_dotenv):
        """Tests embedding generation when no embeddings are returned."""
        mock_getenv.side_effect = lambda key: {"COHERE_API_KEY": "fake_key"}.get(key)
        mock_cohere_client = MockCohereClient.return_value
        mock_cohere_client.embed.return_value.embeddings = [] # Mock no embeddings

        embedding = generate_embedding(mock_cohere_client, "a sample query")
        self.assertIsNone(embedding)

    def test_parse_arguments_success(self):
        """Tests successful parsing of command line arguments."""
        original_argv = sys.argv
        sys.argv = ['retrieve.py', 'a sample query']
        query = parse_arguments()
        self.assertEqual(query, 'a sample query')
        sys.argv = original_argv # Restore original argv

    def test_parse_arguments_no_args(self):
        """Tests argument parsing when no query is provided."""
        original_argv = sys.argv
        sys.argv = ['retrieve.py'] # No query argument
        with self.assertRaises(SystemExit) as cm:
            parse_arguments()
        self.assertEqual(cm.exception.code, 1) # Expecting exit code 1 for error
        sys.argv = original_argv # Restore original argv

    @patch('retrieve.models.NamedVector')
    @patch('retrieve.QdrantClient')
    def test_search_qdrant_success(self, MockQdrantClient, MockNamedVector):
        """Tests successful Qdrant search."""
        mock_qdrant_client = MockQdrantClient.return_value
        mock_search_result = [
            MagicMock(score=0.9, payload={'text': 'relevant chunk 1', 'doc_id': 1}),
            MagicMock(score=0.8, payload={'text': 'relevant chunk 2', 'doc_id': 2})
        ]
        mock_qdrant_client.search.return_value = mock_search_result

        embedding = [0.1] * MOCK_EMBEDDING_DIMENSION
        results = search_qdrant(mock_qdrant_client, embedding)

        MockNamedVector.assert_called_once_with(name="vector", vector=embedding)
        mock_qdrant_client.search.assert_called_once_with(
            collection_name=MOCK_COLLECTION_NAME,
            query_vector=MockNamedVector.return_value,
            query_filter=None,
            limit=5,
            with_payload=True,
            score_threshold=0.7
        )
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].score, 0.9)

    @patch('retrieve.QdrantClient')
    def test_search_qdrant_no_embedding(self, MockQdrantClient):
        """Tests Qdrant search when no embedding is provided."""
        mock_qdrant_client = MockQdrantClient.return_value
        results = search_qdrant(mock_qdrant_client, None)
        self.assertIsNone(results)
        mock_qdrant_client.search.assert_not_called()

    @patch('retrieve.QdrantClient')
    def test_search_qdrant_empty_results(self, MockQdrantClient):
        """Tests Qdrant search when no results are found."""
        mock_qdrant_client = MockQdrantClient.return_value
        mock_qdrant_client.search.return_value = []
        embedding = [0.1] * MOCK_EMBEDDING_DIMENSION
        results = search_qdrant(mock_qdrant_client, embedding)
        self.assertEqual(len(results), 0)

    def test_display_results_success(self, *mocks):
        """Tests successful display of search results."""
        results = [
            MagicMock(score=0.9, payload={'text': 'Chunk 1 content is quite long and needs truncation to fit nicely in the display output to avoid overwhelming the user.', 'doc_id': 1}),
            MagicMock(score=0.8, payload={'text': 'Chunk 2', 'doc_id': 2, 'other_field': 123})
        ]
        
        # Redirect stdout to capture print output
        from io import StringIO
        import sys
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            display_results(results)
            output = sys.stdout.getvalue()
            self.assertIn("--- Search Results ---", output)
            self.assertIn("1. Score: 0.9000", output)
            self.assertIn("   Payload:", output)
            self.assertIn("     - text: Chunk 1 content is quite long and needs truncation to fit nicely in the ...", output) # Test truncation
            self.assertIn("     - doc_id: 1", output)
            self.assertIn("2. Score: 0.8000", output)
            self.assertIn("     - text: Chunk 2", output)
            self.assertIn("     - other_field: 123", output)
            self.assertIn("--------------------", output)
        finally:
            sys.stdout = original_stdout # Restore stdout

    def test_display_results_no_results(self):
        """Tests display_results when no results are provided."""
        # Redirect stdout to capture print output
        from io import StringIO
        import sys
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            display_results([])
            output = sys.stdout.getvalue()
            self.assertIn("No results to display.", output)
        finally:
            sys.stdout = original_stdout # Restore stdout

    # Mocking Cohere and Qdrant clients for the main function test
    @patch('retrieve.initialize_clients')
    @patch('retrieve.generate_embedding')
    @patch('retrieve.search_qdrant')
    @patch('retrieve.display_results')
    def test_main_function_success(self, mock_display_results, mock_search_qdrant, mock_generate_embedding, mock_initialize_clients):
        """Tests the main function execution flow in a success scenario."""
        mock_cohere_client = MagicMock()
        mock_qdrant_client = MagicMock()
        mock_initialize_clients.return_value = (mock_cohere_client, mock_qdrant_client)

        mock_embedding = [0.1] * MOCK_EMBEDDING_DIMENSION
        mock_generate_embedding.return_value = mock_embedding

        mock_search_results = [MagicMock(score=0.9, payload={'text': 'result'})]
        mock_search_qdrant.return_value = mock_search_results

        # Mock sys.argv for parse_arguments
        original_argv = sys.argv
        sys.argv = ['retrieve.py', 'test query']

        with patch('builtins.print') as mock_print:
            main()

        mock_initialize_clients.assert_called_once()
        mock_generate_embedding.assert_called_once_with(mock_cohere_client, 'test query')
        mock_search_qdrant.assert_called_once_with(mock_qdrant_client, mock_embedding)
        mock_display_results.assert_called_once_with(mock_search_results)
        
        sys.argv = original_argv # Restore original argv

    @patch('retrieve.initialize_clients')
    @patch('retrieve.generate_embedding')
    @patch('retrieve.main')
    def test_main_function_embedding_failure(self, mock_main, mock_generate_embedding, mock_initialize_clients):
        """Tests main function when embedding generation fails."""
        mock_cohere_client = MagicMock()
        mock_qdrant_client = MagicMock()
        mock_initialize_clients.return_value = (mock_cohere_client, mock_qdrant_client)
        mock_generate_embedding.return_value = None # Simulate embedding failure

        original_argv = sys.argv
        sys.argv = ['retrieve.py', 'test query']

        with patch('builtins.print') as mock_print:
            with self.assertRaises(SystemExit) as cm:
                main()
            mock_print.assert_any_call("Failed to obtain embedding. Exiting.")
            self.assertEqual(cm.exception.code, 1)
        
        sys.argv = original_argv # Restore original argv

    @patch('retrieve.initialize_clients')
    @patch('retrieve.generate_embedding')
    @patch('retrieve.search_qdrant')
    @patch('retrieve.main')
    def test_main_function_search_failure(self, mock_main, mock_search_qdrant, mock_generate_embedding, mock_initialize_clients):
        """Tests main function when Qdrant search fails."""
        mock_cohere_client = MagicMock()
        mock_qdrant_client = MagicMock()
        mock_initialize_clients.return_value = (mock_cohere_client, mock_qdrant_client)

        mock_embedding = [0.1] * MOCK_EMBEDDING_DIMENSION
        mock_generate_embedding.return_value = mock_embedding

        mock_search_qdrant.return_value = None # Simulate search failure

        original_argv = sys.argv
        sys.argv = ['retrieve.py', 'test query']

        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("No search results found or an error occurred during search.")
        
        sys.argv = original_argv # Restore original argv

    def test_main_function_performance(self):
        """Tests the overall retrieval pipeline performance."""
        # Mocking all components to control execution flow and simulate time
        mock_cohere_client = MagicMock()
        mock_qdrant_client = MagicMock()
        
        # Mock initialize_clients to return mock clients
        with patch('retrieve.initialize_clients', return_value=(mock_cohere_client, mock_qdrant_client)), \
             patch('retrieve.generate_embedding') as mock_generate_embedding, \
             patch('retrieve.search_qdrant') as mock_search_qdrant, \
             patch('retrieve.display_results') as mock_display_results, \
             patch('retrieve.parse_arguments') as mock_parse_arguments:
            
            # Configure mock return values
            mock_embedding = [0.1] * MOCK_EMBEDDING_DIMENSION
            mock_generate_embedding.return_value = mock_embedding
            
            mock_search_results = [MagicMock(score=0.9, payload={'text': 'result'})]
            mock_search_qdrant.return_value = mock_search_results
            
            # Mock parse_arguments to return a query
            mock_parse_arguments.return_value = "test query"

            start_time = time.perf_counter()
            main()
            end_time = time.perf_counter()

            execution_time = end_time - start_time
            print(f"Pipeline execution time: {execution_time:.4f} seconds")

            # Assert that the execution time is within the defined threshold
            self.assertLessEqual(execution_time, PERFORMANCE_THRESHOLD_SECONDS, 
                                 f"Pipeline took {execution_time:.4f}s, exceeding the threshold of {PERFORMANCE_THRESHOLD_SECONDS}s")
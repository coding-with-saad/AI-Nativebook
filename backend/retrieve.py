# retrieve.py

import sys
import os
import logging
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
import cohere

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parses command line arguments to get the user query."""
    logger.info("Parsing command line arguments.")
    if len(sys.argv) < 2:
        logger.error("Usage: python retrieve.py \"<your query here>\"")
        sys.exit(1)
    query = sys.argv[1]
    logger.info(f"Received query: '{query}'")
    return query

def initialize_clients():
    """Initializes and returns Cohere and Qdrant clients."""
    logger.info("Initializing Cohere and Qdrant clients.")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key:
        logger.error("COHERE_API_KEY not found in environment variables.")
        sys.exit(1)
    if not qdrant_url or not qdrant_api_key:
        logger.error("QDRANT_URL and QDRANT_API_KEY not found in environment variables.")
        sys.exit(1)

    try:
        cohere_client = cohere.Client(api_key=cohere_api_key)
        logger.info("Cohere client initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing Cohere client: {e}")
        sys.exit(1)

    try:
        # Qdrant Cloud URLs typically start with https:// and may look like "clustername.eu-central-1.qdrant.cloud"
        # Localhost URLs start with http:// or http://
        if qdrant_url.startswith("http://") or qdrant_url.startswith("https://"):
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            # Fallback for potentially malformed URLs or if a direct IP is used (less common for cloud)
            logger.warning(f"Qdrant URL '{qdrant_url}' format might be unusual. Attempting to use it directly.")
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        
        # Basic check to see if Qdrant is reachable
        client.get_collections() 
        logger.info("Qdrant client initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing Qdrant client or connecting to Qdrant: {e}")
        sys.exit(1)

    return cohere_client, client

def generate_embedding(cohere_client, text):
    """
    Generates an embedding for the given text using the Cohere client.
    """
    logger.info(f"Generating embedding for text: '{text[:50]}...'")
    try:
        response = cohere_client.embed(
            texts=[text],
            model="embed-english-light-v3.0", # Using a common English model
            input_type="search_query" # Specify input type as search query
        )
        if response.embeddings and response.embeddings[0]:
            embedding = response.embeddings[0]
            logger.info(f"Embedding generated successfully. Dimension: {len(embedding)}")
            return embedding
        else:
            logger.error("No embeddings returned from Cohere.")
            return None
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None

def search_qdrant(qdrant_client, query_embedding):
    """
    Performs a similarity search in Qdrant.
    """
    logger.info("Performing Qdrant similarity search.")
    # Key decisions from plan.md: top_k value, similarity threshold
    # These should ideally be configurable or determined empirically.
    # For now, using placeholder values.
    COLLECTION_NAME = "my_collection"  # Placeholder: Needs to be a valid collection name in Qdrant
    TOP_K = 5  # Placeholder: Number of results to retrieve
    SIMILARITY_THRESHOLD = 0.7 # Placeholder: Minimum similarity score

    if not query_embedding:
        logger.error("Cannot perform Qdrant search without a query embedding.")
        return None

    try:
        search_result = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=models.NamedVector(
                name="vector", # Assuming the vector is stored under the name "vector"
                vector=query_embedding
            ),
            query_filter=None, # No filter for now, could be expanded later
            limit=TOP_K,
            with_payload=True, # Return payload (metadata)
            score_threshold=SIMILARITY_THRESHOLD # Apply similarity threshold
        )
        logger.info(f"Qdrant search completed. Found {len(search_result)} results above threshold.")
        return search_result
    except Exception as e:
        logger.error(f"Error performing Qdrant search: {e}")
        return None

def display_results(results):
    """
    Displays the search results in a user-friendly format.
    """
    logger.info("Displaying search results.")
    if not results:
        logger.warning("No results to display.")
        print("No results to display.")
        return

    print("\n--- Search Results ---")
    for i, hit in enumerate(results):
        print(f"\n{i+1}. Score: {hit.score:.4f}")
        if hit.payload:
            print("   Payload:")
            for key, value in hit.payload.items():
                # Truncate long text payloads for better readability
                if isinstance(value, str) and len(value) > 100:
                    print(f"     - {key}: {value[:100]}...")
                else:
                    print(f"     - {key}: {value}")
        else:
            print("   No payload available.")
    print("--------------------\n")
    logger.info("Finished displaying search results.")

def main():
    """
    Main function to orchestrate the retrieval pipeline.
    """
    logger.info("Starting retrieval pipeline execution.")
    query = parse_arguments()
    
    cohere_client, qdrant_client = initialize_clients()

    # Generate embedding for the query
    query_embedding = generate_embedding(cohere_client, query)

    if query_embedding:
        logger.info("Embedding obtained. Ready for Qdrant search.")
        # Perform Qdrant search
        search_results = search_qdrant(qdrant_client, query_embedding)
        
        if search_results:
            logger.info("Search results obtained. Ready to display.")
            # Display the results
            display_results(search_results)
        else:
            logger.warning("No search results found or an error occurred during search.")
    else:
        logger.error("Failed to obtain embedding. Exiting.")
        sys.exit(1)
    logger.info("Retrieval pipeline execution finished.")

if __name__ == "__main__":
    main()
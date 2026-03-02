import os
import cohere
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def get_embedding(text: str, input_type: str = "search_document") -> list[float]:
    """
    Generates a Cohere embedding for the given text.

    Args:
        text: The text to embed.
        input_type: The type of input ('search_document' or 'search_query').

    Returns:
        A list of floats representing the embedding.
    Raises:
        ValueError: If COHERE_API_KEY is not set.
        Exception: For Cohere API errors.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logger.error("COHERE_API_KEY environment variable not set.")
        raise ValueError("COHERE_API_KEY environment variable not set.")

    try:
        co = cohere.Client(api_key=cohere_api_key)
        response = co.embed(texts=[text], model="embed-english-v3.0", input_type=input_type)
        return response.embeddings[0]
    except Exception as e:
        logger.error(f"Error during Cohere embedding: {e}")
        raise Exception(f"Failed to get embedding from Cohere: {e}")

def search_qdrant(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """
    Searches the Qdrant vector database for relevant text chunks.
    Uses the modern query_points API.

    Args:
        query_embedding: The embedding of the query.
        top_k: The number of top relevant results to retrieve.

    Returns:
        A list of dictionaries, each representing a retrieved text chunk.
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "rag_book_collection")

    if not all([qdrant_url, qdrant_api_key]):
        logger.error("QDRANT_URL and QDRANT_API_KEY must be set.")
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set.")

    try:
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # Using the newer query_points API which replaced search in 1.17.0
        search_result = client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
        ).points
        
        retrieved_chunks = []
        for hit in search_result:
            payload = hit.payload or {}
            retrieved_chunks.append({
                "content": payload.get("content"),
                "source_book_id": payload.get("source_book_id"),
                "text_chunk_id": payload.get("text_chunk_id"),
                "relevance_score": hit.score if hasattr(hit, 'score') else None
            })
        return retrieved_chunks
    except Exception as e:
        logger.error(f"An unexpected error occurred during Qdrant search: {e}")
        raise Exception(f"Failed to search Qdrant: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)

    sample_query = "What is the main character's name in 'Pride and Prejudice'?"
    try:
        query_embedding = get_embedding(sample_query, "search_query")
        logger.info("Query embedding generated.")

        results = search_qdrant(query_embedding, top_k=3)
        logger.info(f"Retrieved {len(results)} chunks from Qdrant.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

import os
import logging
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup
import uuid
from langchain_text_splitter import RecursiveCharacterTextSplitter # Import the text splitter
from langchain_core.documents import Document # Import Document class for structured data
import cohere # Import Cohere client
from qdrant_client import QdrantClient, models # Import Qdrant client and models

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
# Use dotenv_path to explicitly point to the template, in a real scenario, 
# you'd ensure the .env file with actual keys is present at runtime.
load_dotenv(dotenv_path='backend/.env.template') 

# --- Configuration ---
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
BOOK_BASE_URL = os.getenv("BOOK_BASE_URL") # e.g., "https://your-github-pages-url.io"

# --- Constants ---
COLLECTION_NAME = "ai_native_book"
EMBEDDING_DIMENSION = 1024 # Cohere embed-english-v3.0
# Chunking parameters from research: max 512 tokens, 10% overlap
CHUNK_SIZE = 500 
CHUNK_OVERLAP = 50 
METADATA_SCHEMA = {
    "url": "keyword",
    "title": "text",
    "module": "keyword",
    "chunk_index": "integer",
    "source_hash": "keyword" # To help with idempotency and detecting changes
}

# Initialize Cohere client
# Check if API key is available before initializing
if COHERE_API_KEY:
    cohere_client = cohere.Client(COHERE_API_KEY)
else:
    cohere_client = None
    logging.warning("COHERE_API_KEY not found. Embedding generation will not work.")

# Initialize Qdrant client
if QDRANT_URL and QDRANT_API_KEY:
    try:
        qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        # Check connection by trying to get collection info (optional, but good for verification)
        # This will raise an exception if connection fails or key is invalid.
        # qdrant_client.get_collection(collection_name=COLLECTION_NAME) 
        logging.info("Qdrant client initialized successfully.")
    except Exception as e:
        qdrant_client = None
        logging.error(f"Failed to initialize Qdrant client: {e}")
else:
    qdrant_client = None
    logging.warning("QDRANT_URL or QDRANT_API_KEY not found. Qdrant storage will not work.")

# --- Helper Functions ---

def generate_point_id(url: str, chunk_index: int) -> str:
    """Generates a deterministic UUID for a chunk based on its URL and index."""
    unique_string = f"{url}_chunk_{chunk_index}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, unique_string))

def extract_content_from_url(url: str) -> tuple[str | None, str | None, str | None, str | None]:
    """
    Fetches content from a URL, parses it, and extracts main text and title.
    Returns (title, main_content_text, module_name, source_html_hash)
    """
    logging.info(f"Fetching content from: {url}")
    try:
        response = httpx.get(url, timeout=20)
        response.raise_for_status() # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.string.strip() if title_tag else "Untitled Page"

        # Attempt to find main content (common patterns for documentation sites)
        # Look for common main content tags or IDs. This might need adjustment
        # based on the actual Docusaurus structure.
        main_content_element = soup.find('main') or soup.find('article') or soup.find('div', id='main-content') or soup.find('div', class_='markdown') or soup.body
        
        # Extract text, clean up whitespace
        text_content = ""
        if main_content_element:
            # Extract text, remove script and style elements
            for script_or_style in main_content_element(["script", "style"]):
                script_or_style.extract()
            text_content = main_content_element.get_text(separator='\n', strip=True)
        
        # Basic module extraction (e.g., from URL path)
        # This is a simplification and might need a more robust approach
        path_parts = url.replace(BOOK_BASE_URL, "").strip('/').split('/')
        module_name = path_parts[0] if path_parts and path_parts[0] not in [''] else 'introduction'

        # Calculate a hash of the raw HTML content to detect changes
        # This is a simplified approach; a more robust method might hash specific content sections.
        source_hash = str(uuid.uuid5(uuid.NAMESPACE_DNS, response.text))

        return title, text_content, module_name, source_hash

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error fetching {url}: {e}")
        return None, None, None, None
    except httpx.RequestError as e:
        logging.error(f"Request error fetching {url}: {e}")
        return None, None, None, None
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing {url}: {e}")
        return None, None, None, None

def chunk_text(text: str, url: str, title: str, module: str, source_hash: str) -> list[Document]:
    """
    Chunks the given text into smaller documents with metadata.
    """
    if not text:
        return []

    logging.info(f"Chunking text for: {url}")
    # Initialize the text splitter
    # Using RecursiveCharacterTextSplitter as researched
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len, # Default length function for strings
        # Add separators if needed, but for general text, defaults are often fine
    )
    
    # Split the text into chunks
    chunks = text_splitter.split_text(text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        # Generate a unique ID for each chunk to ensure idempotency in Qdrant
        point_id = generate_point_id(url, i)
        
        doc_metadata = {
            "url": url,
            "title": title,
            "module": module,
            "chunk_index": i,
            "source_hash": source_hash # Link chunk to its source document hash
        }
        
        # Create a Langchain Document object
        # Note: The vector itself will be added later when embedding.
        # For now, we store the text and its metadata.
        documents.append(Document(page_content=chunk, metadata=doc_metadata, id=point_id))
        
    logging.info(f"Split text into {len(documents)} chunks.")
    return documents

def generate_embeddings(documents: list[Document]):
    """
    Generates embeddings for the provided documents using Cohere.
    Updates each Document object with its vector.
    """
    if not cohere_client:
        logging.error("Cohere client not initialized. Cannot generate embeddings.")
        return

    if not documents:
        logging.warning("No documents provided for embedding.")
        return

    logging.info(f"Generating embeddings for {len(documents)} documents...")
    
    texts_to_embed = [doc.page_content for doc in documents]
    
    try:
        # Use Cohere's embedding model
        # Refer to Cohere documentation for available models and their dimensions.
        # 'embed-english-v3.0' is a good general-purpose choice.
        response = cohere_client.embed(
            texts=texts_to_embed,
            model='embed-english-v3.0', # As per research
            input_type='search_document' # Suitable for RAG
        )
        
        embeddings = response.embeddings
        
        if len(embeddings) == len(documents):
            for i, doc in enumerate(documents):
                # For now, we store the vector in metadata. In a full implementation, 
                # you'd pass this to Qdrant or another vector store.
                doc.metadata["vector"] = embeddings[i] 
            logging.info(f"Successfully generated embeddings for {len(documents)} documents.")
        else:
            logging.error(f"Mismatch in number of embeddings ({len(embeddings)}) and documents ({len(documents)}).")
            
    except Exception as e:
        logging.error(f"Error generating embeddings with Cohere: {e}")

def store_embeddings_in_qdrant(documents: list[Document]):
    """
    Stores the documents (with embeddings) in Qdrant.
    Ensures the collection exists and handles upsert operations idempotently.
    """
    if not qdrant_client:
        logging.error("Qdrant client not initialized. Cannot store embeddings.")
        return

    if not documents:
        logging.warning("No documents provided to store in Qdrant.")
        return

    logging.info(f"Storing {len(documents)} documents in Qdrant collection '{COLLECTION_NAME}'...")

    try:
        # Ensure the collection exists
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=EMBEDDING_DIMENSION, distance=models.Distance.COSINE),
            # Optional: Define payload schema for filtering and searching
            # Using METADATA_SCHEMA as defined in constants for payload indexing
            payload_selectors=models.PayloadSelector(
                enable_payload_indexing=True,
                indexed_payload_names=list(METADATA_SCHEMA.keys())
            )
        )
        logging.info(f"Collection '{COLLECTION_NAME}' recreated or ensured.")

        # Prepare points for upsert
        points_to_upsert = []
        for doc in documents:
            if "vector" in doc.metadata and doc.id:
                points_to_upsert.append(
                    models.PointStruct(
                        id=doc.id, # Use the generated idempotent UUID
                        vector=doc.metadata["vector"],
                        payload={
                            "url": doc.metadata.get("url"),
                            "title": doc.metadata.get("title"),
                            "module": doc.metadata.get("module"),
                            "chunk_index": doc.metadata.get("chunk_index"),
                            "source_hash": doc.metadata.get("source_hash"),
                            # Add original content if needed for debugging/display,
                            # but avoid for large texts to save storage/cost if not needed for search.
                            # "content": doc.page_content 
                        }
                    )
                )
            else:
                logging.warning(f"Skipping document with ID {doc.id} due to missing vector or ID.")
        
        if points_to_upsert:
            # Perform the upsert operation
            # Qdrant's upsert is idempotent based on point ID
            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                wait=True, # Wait for the operation to complete
                points=points_to_upsert
            )
            logging.info(f"Successfully upserted {len(points_to_upsert)} points into Qdrant.")
        else:
            logging.warning("No points were prepared for upsert.")

    except Exception as e:
        logging.error(f"Error storing embeddings in Qdrant: {e}")


# --- Main Execution Flow ---
def main():
    # This is a placeholder for the full pipeline.
    # The complete pipeline will orchestrate:
    # 1. Fetching the list of URLs to process (e.g., from sitemap or crawling website/)
    # 2. For each URL: extract_content_from_url
    # 3. Chunk the extracted text using chunk_text
    # 4. Generate embeddings using Cohere
    # 5. Store embeddings in Qdrant

    logging.info("Starting embedding pipeline execution...")

    # Example: Process a single URL for demonstration
    if BOOK_BASE_URL:
        # In a real scenario, you would likely get a list of all relevant URLs
        # For now, let's try to process the base URL itself as a starting point.
        # A more robust solution would involve finding all links from the homepage
        # or parsing a sitemap.
        example_url = BOOK_BASE_URL
        if not example_url.startswith("http"):
            example_url = f"https://{example_url}" # Ensure it's a valid URL

        title, content, module, source_hash = extract_content_from_url(example_url)

        if title and content and module and source_hash:
            logging.info(f"Successfully extracted content for: {title} (Module: {module}, Hash: {source_hash})")
            logging.info(f"Content preview: {content[:200]}...")
            
            # Chunk the extracted content
            documents = chunk_text(content, example_url, title, module, source_hash)
            
            if documents:
                logging.info(f"Successfully chunked content into {len(documents)} documents.")
                # Log first document's content and metadata as an example
                logging.info(f"Example Document ID: {documents[0].id}")
                logging.info(f"Example Document Content Preview: {documents[0].page_content[:200]}...")
                logging.info(f"Example Document Metadata: {documents[0].metadata}")

                # Generate embeddings for the chunked documents
                generate_embeddings(documents)

                # Store the documents (with embeddings) in Qdrant
                store_embeddings_in_qdrant(documents)
            else:
                logging.warning("No documents were created after chunking.")
            
        else:
            logging.error("Failed to extract content or metadata for the example URL.")
    else:
        logging.error("BOOK_BASE_URL not set. Please configure it in your .env file.")

    logging.info("Embedding pipeline execution finished.")

if __name__ == "__main__":
    main()

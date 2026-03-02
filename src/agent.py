import os
import time
import uuid
import argparse
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from src.utils.logger import setup_logger
from src.retrieval_pipeline import get_embedding, search_qdrant
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load API keys and config from .env
load_dotenv(override=True)

# Setup OpenRouter client if needed
client = AsyncOpenAI(
    api_key=os.getenv("Openrouter_api_key"),
    base_url="https://openrouter.ai/api/v1",
)

# Initialize the third party model
third_party_model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="z-ai/glm-4.5-air:free",
)

# Initialize logger
logger = setup_logger(__name__)

@function_tool
def retrieve_book_content(query: str) -> str:
    """
    Search the book database for relevant information based on the query.
    
    Args:
        query: The search term or question to look up in the book embeddings.
    """
    logger.info(f"Tool called: retrieve_book_content with query: '{query}'")
    try:
        # Use search_query input type for Cohere embeddings
        query_embedding = get_embedding(query, input_type="search_query")
        
        # Retrieve top 5 chunks from Qdrant
        chunks = search_qdrant(query_embedding, top_k=5)
        
        if not chunks:
            return "No relevant sections found in the book documents."
            
        formatted_context = "Retrieved Context:\n\n"
        for chunk in chunks:
            source_id = f"{chunk.get('source_book_id')}:{chunk.get('text_chunk_id')}"
            content = chunk.get("content", "").strip()
            formatted_context += f"--- Source ID: {source_id} ---\n{content}\n\n"
            
        return formatted_context
    except Exception as e:
        logger.error(f"Error in retrieve_book_content tool: {e}")
        return f"Error occurred during document retrieval: {str(e)}"

class RAGAgent:
    def __init__(self, name: str = "RAG Assistant"):
        """
        Initializes the RAG Agent using the OpenAI Agents SDK.
        """
        self.agent = Agent(
            name=name,
            instructions="""You are an expert RAG (Retrieval-Augmented Generation) Assistant.
            Your primary task is to answer user questions accurately by retrieving and analyzing content from specialized book documents.
            
            GUIDELINES:
            1. ALWAYS start by using the 'retrieve_book_content' tool to find relevant context for the user's query.
            2. Base your response ONLY on the information found in the retrieved context.
            3. If the context does not contain the answer, state: 'I am sorry, but the provided book documents do not contain enough information to answer this question.'
            4. ALWAYS provide citations for your statements using the [Source ID: book_id:chunk_id] format found in the tool output.
            5. Do not use external knowledge that contradicts or expands beyond the provided documents.
            6. Keep your tone professional, helpful, and grounded in the source material.""",
            tools=[retrieve_book_content],
            model=third_party_model
        )
        logger.info(f"RAG Agent '{name}' initialized with OpenAI Agents SDK and retrieval tools.")

    def run_query(self, user_query: str) -> dict:
        """
        Processes a user query through the agent loop using the OpenAI Agents SDK Runner.
        """
        query_id = str(uuid.uuid4())
        start_time = time.time()
        logger.info(f"[{query_id}] Starting RAG Agent cycle for: '{user_query}'")
        
        try:
            # Execute the agent loop synchronously using the Runner
            result = Runner.run_sync(self.agent, user_query)
            
            answer_text = result.final_output
            
            duration_ms = (time.time() - start_time) * 1000
            logger.info(f"[{query_id}] Query completed successfully in {duration_ms:.2f}ms.")
            
            return {
                "query_id": query_id,
                "answer": answer_text,
                "status": "SUCCESS",
                "response_time_ms": duration_ms
            }
            
        except Exception as e:
            logger.error(f"[{query_id}] Critical failure in agent loop: {e}")
            return {
                "query_id": query_id,
                "answer": f"I encountered an internal error while processing your request: {str(e)}",
                "status": "FAILURE",
                "response_time_ms": (time.time() - start_time) * 1000
            }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Agent CLI (OpenAI Agents SDK)")
    parser.add_argument("--query", type=str, required=True, help="The question you want to ask the RAG agent.")
    args = parser.parse_args()

    rag = RAGAgent()
    response = rag.run_query(args.query)
    
    print("\n" + "="*50)
    print(f"RAG AGENT RESPONSE")
    print("="*50)
    print(f"USER QUERY: {args.query}")
    print("-"*50)
    print(f"AGENT ANSWER:\n\n{response['answer']}")
    print("-" * 50)
    print(f"Status: {response['status']} | Time: {response['response_time_ms']:.2f}ms")
    print("="*50 + "\n")

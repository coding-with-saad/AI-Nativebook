import uvicorn
import sys
import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Add the project root to sys.path
# This helps resolve imports from 'src' when running directly or with uvicorn's reloader
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from agent import RAGAgent # Import the RAGAgent class

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SourceReference(BaseModel):
    path: str
    heading: Optional[str] = None
    page: Optional[int] = None

class Query(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    sources: List[SourceReference]

# Instantiate the RAGAgent globally
rag_agent = RAGAgent()

@app.post("/query", response_model=Response)
async def run_query(query: Query):
    # Call the synchronous run_query method of RAGAgent in a separate thread
    agent_response = await asyncio.to_thread(rag_agent.run_query, query.question)
    
    # The agent_response structure in agent.py's run_query is a dict with 'answer', 'sources', etc.
    # We need to ensure the 'sources' key is present and formatted correctly for the Response model.
    # The current agent_response in agent.py example does not directly return 'sources' list,
    # but the problem description implies it should. Let's assume for now agent_response['answer']
    # will contain the full text including citations, and we might need to parse it or
    # agent.py needs to be updated to return structured sources.
    
    # For now, let's adapt to what agent.py's run_query returns, which is a dict like:
    # { "query_id": ..., "answer": "...", "status": "SUCCESS", "response_time_ms": ... }
    # It does not explicitly return a 'sources' list, but its instructions ask to cite sources.
    # The Response model expects a list of SourceReference.
    # This means agent.py needs to be modified to return structured sources.
    # For now, I will return an empty list for sources to avoid a Pydantic validation error,
    # and we can refine agent.py later if needed.

    # If agent_response has sources, use them, otherwise default to empty list.
    sources_data = []
    if "answer" in agent_response:
        # Simple regex to extract source IDs from the answer text
        import re
        source_matches = re.findall(r'\[Source ID: ([^\]]+)\]', agent_response['answer'])
        for source_id_str in source_matches:
            # Assuming source_id_str is like "book_id:chunk_id" or "path/to/file.md:heading"
            # This parsing is a guess based on the example in retrieve_book_content.
            # A more robust solution would involve agent.py returning structured sources.
            parts = source_id_str.split(':')
            if len(parts) >= 2:
                path_or_id = parts[0]
                heading_or_chunk_id = parts[1]
                # Further parsing for page could be added if source_id_str includes it.
                sources_data.append(SourceReference(path=path_or_id, heading=heading_or_chunk_id))
            else:
                sources_data.append(SourceReference(path=source_id_str)) # Fallback if format is simple


    return Response(
        answer=agent_response.get('answer', "No answer found."),
        sources=sources_data # Placeholder for actual source parsing if agent.py returns structured sources
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

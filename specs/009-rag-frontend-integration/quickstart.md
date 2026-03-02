# Quickstart: RAG Frontend Integration

**Branch**: `009-rag-frontend-integration` | **Date**: 2026-03-02 | **Spec**: [spec.md](spec.md)

This guide provides instructions on how to run the integrated RAG frontend and backend for local development.

## Prerequisites

- Python 3.11+
- Node.js LTS
- An existing `agent.py` file with a functioning RAG agent.

## Backend Setup

1.  **Create the API file**: Create a new file named `api.py` in the project root.
2.  **Install dependencies**:
    ```bash
    pip install fastapi uvicorn python-dotenv
    ```
3.  **Add the following code to `api.py`**:
    ```python
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    
    # Assuming agent.py is in the same directory and has a query function
    from agent import query as ask_agent
    
    app = FastAPI()
    
    # CORS configuration
    origins = [
        "http://localhost:3000", # Docusaurus default port
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    class Query(BaseModel):
        question: str
    
    @app.post("/query")
    async def run_query(query: Query):
        # This is a placeholder for the actual agent call
        # You will need to adapt this to your agent's interface
        response = ask_agent(query.question) 
        return response
    
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```
4.  **Run the backend server**:
    ```bash
    uvicorn api:app --reload --port 8000
    ```

## Frontend Setup

1.  **Create the Chatbot component**: Create a new directory `src/components/Chatbot` inside your Docusaurus `website` directory. Inside this directory, create `index.js` and `styles.css`.
2.  **Add the following code to `website/src/components/Chatbot/index.js`**:
    ```jsx
    import React, { useState } from 'react';
    import styles from './styles.module.css';
    
    const Chatbot = () => {
      const [isOpen, setIsOpen] = useState(false);
      const [question, setQuestion] = useState('');
      const [response, setResponse] = useState(null);
      const [isLoading, setIsLoading] = useState(false);
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResponse(null);
    
        try {
          const res = await fetch('http://localhost:8000/query', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
          });
    
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
    
          const data = await res.json();
          setResponse(data);
        } catch (error) {
          console.error("Failed to fetch:", error);
          setResponse({ answer: "Sorry, something went wrong.", sources: [] });
        } finally {
          setIsLoading(false);
        }
      };
    
      return (
        <div>
          <button className={styles.floatingButton} onClick={() => setIsOpen(!isOpen)}>
            ?
          </button>
    
          {isOpen && (
            <div className={styles.chatWindow}>
              <div className={styles.chatHeader}>
                <h2>Ask the Book</h2>
                <button onClick={() => setIsOpen(false)}>&times;</button>
              </div>
              <div className={styles.chatBody}>
                {response && (
                  <div>
                    <p>{response.answer}</p>
                    {response.sources && response.sources.length > 0 && (
                      <div>
                        <strong>Sources:</strong>
                        <ul>
                          {response.sources.map((source, index) => (
                            <li key={index}>{source.path}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
                 {isLoading && <p>Loading...</p>}
              </div>
              <div className={styles.chatFooter}>
                <form onSubmit={handleSubmit}>
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question..."
                  />
                  <button type="submit">Send</button>
                </form>
              </div>
            </div>
          )}
        </div>
      );
    };
    
    export default Chatbot;
    ```
3.  **Add styles to `website/src/components/Chatbot/styles.css`**. (This will be done in the implementation phase).
4.  **Integrate the component**: Import and render the `Chatbot` component in your main Docusaurus layout file (e.g., `website/src/theme/Root.js`).
    ```jsx
    // website/src/theme/Root.js
    import React from 'react';
    import Chatbot from '@site/src/components/Chatbot';
    
    // Default implementation, that you can customize
    export default function Root({children}) {
      return (
        <>
          {children}
          <Chatbot />
        </>
      );
    }
    ```
5.  **Run the frontend server**:
    ```bash
    cd website
    npm start
    ```

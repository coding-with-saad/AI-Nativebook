import React, { useState } from 'react';
import './styles.css';

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
      <button className="floatingButton" onClick={() => setIsOpen(!isOpen)}>
        ?
      </button>

      {isOpen && (
        <div className="chatWindow">
          <div className="chatHeader">
            <h2>Ask the Book</h2>
            <button onClick={() => setIsOpen(false)}>&times;</button>
          </div>
          <div className="chatBody">
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
          <div className="chatFooter">
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

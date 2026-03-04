import React, { useState } from 'react';
import './styles.css'; // Use standard CSS import

// SVG icon for the chatbot button
const ChatbotIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
    </svg>
);

// SVG icon for the send button
const SendIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
    </svg>
);


const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return; // Don't send empty questions
        setIsLoading(true);
        setResponse(null);

        try {
            const res = await fetch('http://localhost:8000/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();
            setResponse(data);
        } catch (error) {
            console.error("Failed to fetch:", error);
            setResponse({ answer: "Sorry, something went wrong. Please try again later.", sources: [] });
        } finally {
            setIsLoading(false);
            setQuestion(''); // Clear input after sending
        }
    };

    return (
        <>
            <button className="floatingButton" onClick={() => setIsOpen(!isOpen)} aria-label="Open chat">
                <ChatbotIcon />
            </button>

            <div className={`chatWindow ${isOpen ? 'open' : 'closed'}`}>
                <div className="chatHeader">
                    <h2>Ask the Book</h2>
                    <button className="closeButton" onClick={() => setIsOpen(false)} aria-label="Close chat">&times;</button>
                </div>
                <div className="chatBody">
                    {response && (
                        <div className="responseContainer">
                            <p>{response.answer}</p>
                            {response.sources && response.sources.length > 0 && (
                                <>
                                    <strong>Sources:</strong>
                                    <ul>
                                        {response.sources.map((source, index) => (
                                            <li key={index}>{source.path}</li>
                                        ))}
                                    </ul>
                                </>
                            )}
                        </div>
                    )}
                    {isLoading && <p className="loadingMessage">Thinking...</p>}
                </div>
                <div className="chatFooter">
                    <form onSubmit={handleSubmit}>
                        <input
                            type="text"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            placeholder="Ask a question..."
                            aria-label="Ask a question"
                        />
                        <button type="submit" aria-label="Send question">
                            <SendIcon />
                        </button>
                    </form>
                </div>
            </div>
        </>
    );
};

export default Chatbot;

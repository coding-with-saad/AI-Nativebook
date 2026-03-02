from fastapi.testclient import TestClient
from api import app, Query, Response, SourceReference

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404 # No root endpoint defined

def test_query_endpoint():
    # Mocking the ask_agent function
    async def mock_ask_agent(question: str):
        if "hello" in question.lower():
            return {"answer": "Hello there!", "sources": []}
        if "VLA" in question:
            return {
                "answer": "A VLA is a Very Large Array.",
                "sources": [
                    {"path": "book/chapter1.md", "heading": "Introduction", "page": 10}
                ],
            }
        return {"answer": "Sorry, I don't know.", "sources": []}

    app.dependency_overrides[app.post("/query")._decorated.func] = lambda: mock_ask_agent

    # Test a simple query
    response = client.post("/query", json={"question": "hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Hello there!", "sources": []}

    # Test a query with expected sources
    response = client.post("/query", json={"question": "What is a VLA?"})
    assert response.status_code == 200
    expected_response = {
        "answer": "A VLA is a Very Large Array.",
        "sources": [
            {"path": "book/chapter1.md", "heading": "Introduction", "page": 10}
        ],
    }
    assert response.json() == expected_response

    # Test an unknown query
    response = client.post("/query", json={"question": "unknown topic"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Sorry, I don't know.", "sources": []}

    # Clean up the override
    app.dependency_overrides = {}

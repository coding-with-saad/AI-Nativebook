# Tasks for RAG Frontend Integration

**Branch**: `009-rag-frontend-integration` | **Date**: 2026-03-02 | **Spec**: [spec.md](spec.md)

This document outlines the tasks required to implement the RAG frontend integration.

## Phase 1: Setup

- [x] T001 Create `api.py` at the project root.
- [x] T002 Install backend dependencies: `fastapi`, `uvicorn`, `python-dotenv` by running `pip install fastapi uvicorn python-dotenv`.
- [x] T003 Create the directory `website/src/components/Chatbot`.
- [x] T004 Create the files `website/src/components/Chatbot/index.js` and `website/src/components/Chatbot/styles.css`.

## Phase 2: Foundational

- [x] T005 Implement the basic FastAPI application structure in `api.py`.
- [x] T006 Add CORS middleware to `api.py` to allow requests from `http://localhost:3000`.
- [x] T007 Implement the basic React component structure for `Chatbot` in `website/src/components/Chatbot/index.js`.
- [x] T008 Import and render the `Chatbot` component in `website/src/theme/Root.js`.

## Phase 3: User Story 1 - Ask questions from the book

- [x] T009 [US1] Define the `Query` and `Response` Pydantic models in `api.py` as specified in the data model.
- [x] T010 [US1] Implement the `/query` endpoint in `api.py` which takes a `Query` and returns a `Response` by calling the `ask_agent` function from `agent.py`.
- [x] T011 [P] [US1] Implement the floating button and chat window UI in `website/src/components/Chatbot/index.js`.
- [x] T012 [P] [US1] Implement the form submission logic in `website/src/components/Chatbot/index.js` to send the user's question to the `/query` endpoint.
- [x] T013 [US1] Implement the logic to render the Markdown response and source links from the backend in `website/src/components/Chatbot/index.js`.
- [x] T014 [P] [US1] Add CSS styles to `website/src/components/Chatbot/styles.css` for the floating button, chat window, and response display.

## Phase 4: User Story 2 - Real-time feedback and error handling

- [x] T015 [US2] Implement a loading indicator in `website/src/components/Chatbot/index.js` that is displayed while waiting for the backend response.
- [x] T016 [US2] Implement error handling in `website/src/components/Chatbot/index.js` to display a user-friendly message if the API call fails.

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T017 [P] Add a basic unit test for the `/query` endpoint in a new `tests/test_api.py` file.
- [x] T018 [P] Add a basic component test for the `Chatbot` component in `website/src/components/Chatbot/__tests__/index.test.js`.
- [x] T019 Review and refine the UI/UX of the chat window for a better user experience.

## Dependencies

- User Story 2 (Phase 4) depends on the completion of User Story 1 (Phase 3).
- The Polish phase (Phase 5) should be started after all user story phases are complete.

## Parallel Execution

- Within Phase 3, tasks T011, T012, and T014 can be worked on in parallel to a large extent.
- The backend tasks (T009, T010) and frontend tasks (T011, T012, T013, T014) can be worked on in parallel by different developers.

## Implementation Strategy

The implementation will follow a phased approach, starting with the MVP (Minimum Viable Product) which consists of completing Phase 1, 2 and 3. This will deliver the core functionality of asking a question and getting a response. Subsequent phases will add more robustness and polish to the feature.

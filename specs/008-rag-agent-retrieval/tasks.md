# Tasks: RAG Agent with Retrieval Pipeline

**Input**: Design documents from `/specs/008-rag-agent-retrieval/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

---
## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directories: `src/`, `tests/unit/`, `tests/integration/`, `tests/contract/`
- [X] T002 Initialize Python project and virtual environment.
- [X] T003 Install core dependencies: `openai-agents`, `qdrant-client`, `cohere`.
- [X] T004 Create placeholder `src/agent.py` file.
- [X] T005 Create placeholder `src/retrieval_pipeline.py` file.
- [X] T006 Configure environment variables for `OPENAI_API_KEY`, `COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME` (guidance in `specs/008-rag-agent-retrieval/quickstart.md`).

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Implement core Cohere embedding utility in `src/retrieval_pipeline.py` (Refer `research.md` for `input_type` and chunking best practices).
- [X] T008 Implement Qdrant client connection and basic search logic in `src/retrieval_pipeline.py` (Refer `research.md` for Qdrant best practices).
- [X] T009 Implement a generic logging utility for the application.
- [X] T010 Implement the basic OpenAI Agent setup and initialization in `src/agent.py`.

---
## Phase 3: User Story 1 - Ask a Question and Get Grounded Answer (Priority: P1) 🎯 MVP

**Goal**: Enable the RAG agent to receive user queries, retrieve relevant context, and generate grounded answers.

**Independent Test**: Provide a query and verify the agent's response is accurate, grounded in retrieved chunks, and logs sources/response time.

### Tests for User Story 1 (REQUIRED as per Acceptance Scenarios and Success Criteria)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Create unit test for embedding utility in `tests/unit/test_retrieval_pipeline.py`.
- [X] T012 [P] [US1] Create unit test for Qdrant retrieval logic in `tests/unit/test_retrieval_pipeline.py`.
- [X] T013 [P] [US1] Create unit test for context formatting in `tests/unit/test_agent.py`.
- [X] T014 [P] [US1] Create unit test for hallucination check logic in `tests/unit/test_agent.py`.
- [X] T015 [P] [US1] Create unit test for error handling logic in `tests/unit/test_agent.py`.
- [X] T016 [P] [US1] Create integration test for end-to-end query processing (`/query` endpoint) in `tests/integration/test_e2e_rag.py` (simulating API call).

### Implementation for User Story 1

- [X] T017 [US1] Implement embedding of user queries using Cohere (`search_query` `input_type`) in `src/retrieval_pipeline.py`. (Depends on T007)
- [X] T018 [US1] Implement retrieval of 5 relevant text chunks from Qdrant in `src/retrieval_pipeline.py`. (Depends on T008)
- [X] T019 [US1] Implement structured context formatting (XML-like tags) for agent prompt in `src/agent.py`. (Refer `research.md`)
- [X] T020 [US1] Implement injection of retrieved context into the OpenAI Agent's prompt in `src/agent.py`. (Depends on T019)
- [X] T021 [US1] Implement basic hallucination control (strict prompting invariants, initial programmatic guardrails) in `src/agent.py`. (Refer `research.md`)
- [X] T022 [US1] Implement comprehensive error handling (tool failures, Qdrant/embedding errors, SDK exceptions) across `src/agent.py` and `src/retrieval_pipeline.py`. (Refer `research.md`)
- [X] T023 [US1] Implement API endpoint `/query` in `src/agent.py` to receive user queries and return grounded answers with sources. (Refer `contracts/rag_api.yaml`)
- [X] T024 [US1] Implement logging of retrieved sources, response time, and query ID in `src/agent.py` and `src/retrieval_pipeline.py`. (Depends on T009)
- [X] T025 [US1] Integrate `retrieval_pipeline.py` into `agent.py`.

---
## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T026 Refine and clarify error messages for user-facing output.
- [X] T027 Review and enhance logging for debuggability and monitoring.
- [X] T028 Update `quickstart.md` with final installation steps and execution commands.
- [X] T029 Perform overall code cleanup and refactoring across `src/` and `tests/`.
- [X] T030 Validate `quickstart.md` by following the steps to ensure successful setup and execution.

---
## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed)
    -   Or sequentially in priority order (P1 → P2 → P3)
-   **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

-   Tests MUST be written and FAIL before implementation
-   Model/utility creation before integration
-   Core implementation before API exposure

### Parallel Opportunities

-   **Phase 1**: All tasks can run in parallel.
-   **Phase 2**: All tasks can run in parallel.
-   **Phase 3 (User Story 1)**:
    -   All unit test creation tasks (T011-T015) can run in parallel.
    -   `T017` and `T018` can be developed in parallel within `src/retrieval_pipeline.py`.
    -   `T019`, `T020`, `T021`, `T022`, `T023`, `T024`, `T025` can be developed mostly in parallel for `src/agent.py`, but will have internal dependencies.
-   **Phase 4**: Tasks T026, T027, T028, T029, T030 can run in parallel.

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done, Developer A can work on User Story 1.

---
## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

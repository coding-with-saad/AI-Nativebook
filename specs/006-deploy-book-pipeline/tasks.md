---
description: "Task list for feature: Deploy Book Website and Build Embedding Pipeline"
---

# Tasks: Deploy Book Website and Build Embedding Pipeline

**Input**: Design documents from `/specs/006-deploy-book-pipeline/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Backend Project Initialization)

**Purpose**: Create the basic structure for the Python embedding pipeline.

- [X] T001 Create project structure `backend/`
- [X] T002 Initialize `uv` project in `backend/pyproject.toml` with dependencies: `cohere`, `qdrant-client`, `httpx`, `beautifulsoup4`, `python-dotenv`, `pytest`
- [X] T003 Create `backend/.env.template` with keys: `COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `BOOK_BASE_URL`
- [X] T004 Create test directory structure: `backend/tests/unit/`, `backend/tests/integration/`

---

## Phase 2: User Story 1 - Deploy Book to GitHub Pages (Priority: P1) 🎯 MVP

**Goal**: Automatically deploy the Docusaurus book to a public URL so that the content is accessible.

**Independent Test**: A change merged to the `main` branch triggers a GitHub Action that successfully deploys the book to its public GitHub Pages URL.

### Implementation for User Story 1

- [X] T005 [US1] Create GitHub Actions workflow in `.github/workflows/deploy-docusaurus.yml`
- [X] T006 [US1] Configure the workflow to trigger on push to `main`, check out code, setup Node.js, install `website/` dependencies, and build the Docusaurus site
- [X] T007 [US1] Add a step to the workflow to deploy the `website/build` directory to the `gh-pages` branch
- [ ] T008 [US1] Configure GitHub Pages in repository settings to deploy from the `gh-pages` branch

**Checkpoint**: At this point, User Story 1 should be fully functional. The book should be live on a public URL.

---

## Phase 3: User Story 2 - Build Embedding Pipeline (Priority: P2)

**Goal**: Create a pipeline that extracts content from the deployed book, generates embeddings, and stores them in a Qdrant vector database.

**Independent Test**: Running `uv run python main.py` in the `backend/` directory successfully populates the Qdrant Cloud collection with vectors and metadata from the public book URL.

### Implementation for User Story 2

- [X] T009 [P] [US2] Implement content extraction logic in `backend/main.py` using `httpx` to fetch URLs and `BeautifulSoup4` to parse content from the deployed site.
- [X] T010 [P] [US2] Implement markdown-aware chunking logic in `backend/main.py` (e.g., using `RecursiveCharacterTextSplitter`).
- [X] T011 [P] [US2] Implement embedding generation in `backend/main.py` using the `cohere` client and the `embed-english-v3.0` model.
- [X] T012 [US2] Implement vector storage in `backend/main.py`, using `qdrant-client` to connect to Qdrant Cloud and `upsert` points with idempotent UUIDs.
- [X] T013 [US2] Assemble the full pipeline in a `main()` function within `backend/main.py`, orchestrating the extraction, chunking, embedding, and storage steps.

**Checkpoint**: At this point, User Story 2 should be fully functional. The pipeline can be run to populate the vector database.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improve robustness and documentation.

- [X] T014 [P] Add structured logging throughout the pipeline in `backend/main.py`.
- [X] T015 [P] Add robust error handling (e.g., for HTTP errors, API failures) in `backend/main.py`.
- [X] T016 [P] Create `backend/README.md` with detailed setup and execution instructions.
- [X] T017 Run `quickstart.md` validation.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: Can start immediately.
- **User Story 1 (Phase 2)**: Depends on `website/` code being present. Can start in parallel with Phase 1.
- **User Story 2 (Phase 3)**: Depends on Setup (Phase 1) and User Story 1 (Phase 2) completion, as it needs the public URL.
- **Polish (Phase 4)**: Depends on all other phases.

### Implementation Strategy

1. **MVP First (User Story 1)**: Complete Phase 1 and 2 to get the book deployed and publicly accessible.
2. **Incremental Delivery**: Complete Phase 3 to enable embedding generation.
3. **Polish**: Complete Phase 4 to finalize the pipeline for production use.

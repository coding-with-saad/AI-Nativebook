# Implementation Plan: Deploy Book Website and Build Embedding Pipeline

**Branch**: `006-deploy-book-pipeline` | **Date**: 2026-02-25 | **Spec**: [specs/006-deploy-book-pipeline/spec.md](specs/006-deploy-book-pipeline/spec.md)
**Input**: Feature specification from `/specs/006-deploy-book-pipeline/spec.md`

## Summary

This feature involves deploying a Docusaurus-based book to GitHub Pages and building a Python-based embedding pipeline. The pipeline will extract content from the deployed site, chunk it, generate embeddings using Cohere, and store them in Qdrant Cloud for future RAG capabilities.

## Technical Context

**Language/Version**: Python 3.12 (via `uv`)
**Primary Dependencies**: `cohere`, `qdrant-client`, `httpx`, `beautifulsoup4`, `python-dotenv`
**Storage**: Qdrant Cloud (Free Tier)
**Testing**: `pytest`
**Target Platform**: GitHub Pages (Deployment), Python (Pipeline)
**Project Type**: Web application + Backend Pipeline
**Performance Goals**: Idempotent re-runs, efficient embedding generation within free tier limits.
**Constraints**: No hardcoded secrets, support incremental updates, deployment to GitHub Pages.
**Scale/Scope**: Entire book content (multiple modules), stored as vectors with metadata.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Test-First**: Implementation will follow TDD for the pipeline logic.
- [x] **No Secrets**: Environment variables managed via `.env` and `uv`.
- [x] **Simplicity**: Backend structured as a single `main.py` for the ingestion flow.
- [x] **Documentation**: All architectural decisions documented in ADRs/research.

## Project Structure

### Documentation (this feature)

```text
specs/006-deploy-book-pipeline/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A for internal pipeline)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
website/                 # Docusaurus project
├── docs/
├── src/
└── ...

backend/                 # Embedding pipeline
├── main.py              # Full ingestion flow
├── pyproject.toml       # uv configuration
├── .env                 # Environment variables (local only)
└── tests/               # Pipeline tests
    ├── integration/
    └── unit/
```

**Structure Decision**: Option 2 (Web application) style, but with `backend/` specifically for the embedding pipeline as a standalone `uv` project.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

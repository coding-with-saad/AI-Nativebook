# Data Model: Embedding Pipeline

This document defines the entities and data structures used in the embedding pipeline and the Qdrant vector database.

## Entities

### 1. Document
- **Source**: Deployed Docusaurus page.
- **Fields**:
  - `url` (String): Publicly accessible URL.
  - `title` (String): Page title from metadata/H1.
  - `content` (String): Cleaned markdown content.
  - `module` (String): Module name (e.g., Module 1, Module 2).
  - `last_modified` (ISO Date): Last change timestamp.

### 2. Chunk
- **Source**: Document split into smaller pieces.
- **Fields**:
  - `id` (UUIDv5): Generated from `url + chunk_index`.
  - `content` (String): Text chunk (max 512 tokens).
  - `vector` (Array[1024]): Cohere `embed-english-v3.0` representation.
  - `metadata`:
    - `url` (String)
    - `title` (String)
    - `module` (String)
    - `chunk_index` (Integer)
    - `source_hash` (String): MD5 of the original document content to detect changes.

## Relationships

- **Document (1) <-> (N) Chunk**: A single page is split into multiple chunks for embedding.
- **Chunk (1) <-> (1) Vector**: Each chunk has exactly one 1024-dimension vector.

## Validation Rules

- **Chunk Size**: Must not exceed 512 tokens (Cohere limit).
- **Point ID**: Must be a stable UUID to ensure idempotency.
- **Metadata**: Every point MUST include a `url` for source referencing.

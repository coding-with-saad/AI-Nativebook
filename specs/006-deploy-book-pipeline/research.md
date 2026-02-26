# Research: Embedding Pipeline for Docusaurus Book

This research document addresses technical decisions for the embedding pipeline, specifically focusing on chunking, model selection, and vector storage.

## Decisions

### 1. Chunking Strategy
- **Decision**: Use `RecursiveCharacterTextSplitter` with markdown headers as primary separators.
- **Rationale**: Preserves semantic structure of the book. Cohere `embed-english-v3.0` has a 512-token limit.
- **Configuration**:
  - Chunk Size: ~500 tokens (to stay under 512 limit).
  - Chunk Overlap: 50 tokens (10%).
- **Alternatives Considered**: Fixed-size character splitting (rejected as it breaks sentences/code blocks).

### 2. Embedding Model
- **Decision**: Cohere `embed-english-v3.0`.
- **Rationale**: State-of-the-art for retrieval tasks, supports English natively, and fits within the free tier.
- **Dimensions**: 1024.

### 3. Vector Storage & Idempotency
- **Decision**: Qdrant Cloud (Free Tier) with deterministic UUIDs.
- **Rationale**: Qdrant's `upsert` is idempotent. To prevent duplicates on re-runs, each point ID will be a UUID generated from a hash of the `(url + chunk_index)`.
- **Metadata Schema**:
  ```json
  {
    "url": "string",
    "title": "string",
    "module": "string",
    "content": "string",
    "timestamp": "iso8601"
  }
  ```

### 4. Content Extraction
- **Decision**: Use `httpx` and `BeautifulSoup4` to scrape the deployed GitHub Pages site.
- **Rationale**: Ensures the embeddings reflect the publicly available version of the book. Parsing the `docs/` markdown files directly is an alternative but might include draft content or omit Docusaurus-generated metadata.

## Unknowns Resolved
- [x] Optimal chunk size for Cohere: 512 tokens max.
- [x] Qdrant dimension: 1024 for `embed-english-v3.0`.
- [x] Idempotency: Use content-based hashing for IDs.

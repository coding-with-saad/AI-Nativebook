# Data Model for Retrieval Pipeline

This feature does not introduce any new persistent data models. The `retrieve.py` script is stateless.

The data structures used in the pipeline are:

- **Input Query**: A plain string provided by the user.

- **Qdrant Point**: The structure stored in Qdrant, which includes:
  - `id`: A unique identifier for the chunk.
  - `vector`: The Cohere embedding of the text chunk.
  - `payload`: Metadata about the chunk, such as `document_id`, `text`, etc.

- **Retrieved Result**: A list of Qdrant points, representing the most relevant chunks for the user's query.

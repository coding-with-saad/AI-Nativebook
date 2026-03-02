# Research Notes: RAG Agent with Retrieval Pipeline

**Feature Branch**: `008-rag-agent-retrieval` | **Date**: 2026-02-27 | **Plan**: [specs/008-rag-agent-retrieval/plan.md]

## Research Topics

### 1. Context Formatting Style for OpenAI Agents SDK

-   **Description**: How should the retrieved `top_k` chunks be formatted and integrated into the OpenAI Agent's prompt effectively?
-   **Questions**:
    -   What are the best practices for structuring context within the prompt?
    -   Are there specific delimiters or instructions recommended by OpenAI for RAG contexts?
    -   How to ensure the agent correctly identifies and utilizes the provided context?
-   **Findings**:
    -   **Dynamic Instructions (System Prompts):** Use a function for `instructions` that receives `Agent` and `Context` objects, returning a string. This is ideal for injecting "always-on" context.
    -   **Structured Context Injection:** Use clear delimiters like triple quotes (`"""`) or XML-like tags (`<context>...</context>`) to separate instructions from retrieved data.
    -   **Agentic RAG:** Agent actively manages its own retrieval, using a "Search-Gather-Answer" pattern with distinct tools.
    -   **Semantic Chunking & Metadata:** Store chunks with rich metadata (`chunk_id`, `source_url`) and include IDs in context for citations.
    -   **Prompt Template for RAG:** Use a structured template within tool output or dynamic instructions, including CONTEXT, GUIDELINES (answer ONLY using context, cite sources, state inability to answer if not in context).
    -   **Context Trimming:** For long sessions, use `TrimmingSession` or manual history management to avoid context window overflow.
    -   **Tool-Level Context:** Use `ToolContext` if RAG tool needs its `tool_call_id` or arguments for logging/tracing.
    -   **Tracing:** Enable built-in tracing for debugging RAG tool interactions.
    -   **Provider Agnostic:** Ensure context formatting matches the strengths of the specific LLM being used.
    -   Decision: Adopt structured context injection using XML-like tags (e.g., `<context>...</context>`) within dynamic instructions or tool outputs. Implement the "Search-Gather-Answer" pattern where the agent explicitly uses tools for retrieval. Prioritize semantic chunking with metadata for citations.
    -   Rationale: Structured formatting improves clarity for the LLM and reduces misinterpretation. The "Search-Gather-Answer" pattern provides better control over the retrieval process and makes it more explicit. Metadata allows for proper attribution and debugging.
    -   Alternatives Considered:
        -   Simple concatenation of chunks: Less explicit for the LLM, higher risk of misinterpretation.
        -   Fixed system prompt with all context: Less flexible, harder to manage dynamic context.

### 2. Hallucination Control Strategy for RAG Agents

-   **Description**: Investigate techniques to prevent the RAG agent from generating information outside the provided retrieved context.
-   **Questions**:
    -   What prompt engineering techniques can be used?
    -   Are there specific parameters or configurations in the OpenAI Agents SDK to control grounding?
    -   How to detect and mitigate hallucination effectively?
-   **Findings**:
    -   **Multi-layered approach:** Recommended, leveraging SDK primitives like Agents, Guardrails, and Handoffs.
    -   **Layered Defense Architecture:**
        -   **Input:** Semantic Filtering using Tools to ensure only relevant context is retrieved.
        -   **Execution:** Grounding Instructions within `Agent.instructions` to force citing sources and admitting ignorance.
        -   **Validation:** Output Guardrails for programmatic checks comparing output with retrieved context.
        -   **Verification:** Critic Agent using Handoffs, where a second agent verifies the response against source text.
    -   **Programmatic Guardrails:** Implement a "Groundedness Check" with `Guardrails`. If output contains ungrounded facts, trigger fail-fast or retry with stricter prompt.
    -   **"Critic" Pattern (Multi-Agent):** Workflow where a Researcher Agent drafts, then a Validator Agent checks for discrepancies and provides correction instructions.
    -   **Tool-Level Grounding:** Use Function tools to structure retrieval, requiring "Source ID" for every fact and explicit inclusion in agent's response.
    -   **Recommended Prompting Invariants:**
        -   "If the answer is not in the provided context, state 'I do not have enough information'."
        -   "Every claim must be followed by a [Source ID] reference."
        -   "Do not use internal knowledge that contradicts the provided context."
    -   **Risks:** Increased latency and cost due to multi-agent verification.
    -   Decision: Implement a multi-layered hallucination control strategy. Start with programmatic guardrails using the SDK's `Guardrails` feature for a "Groundedness Check" and enforce strict prompting invariants. Explore the "Critic" pattern and tool-level grounding as advanced mechanisms or future enhancements.
    -   Rationale: Programmatic guardrails provide a direct and efficient first line of defense. Strict prompting directly guides the LLM's behavior. The multi-agent approach, while powerful, introduces complexity, latency, and cost that may be more suitable for later stages.
    -   Alternatives Considered:
        -   Relying solely on prompting: Less robust, higher risk of hallucination.
        -   Immediate full multi-agent system: Overkill for initial implementation, higher initial complexity, cost, and latency.

### 3. Error Handling for RAG Agents with OpenAI Agents SDK and Qdrant

-   **Description**: Define robust error handling mechanisms for failures in the retrieval pipeline (Qdrant, embedding service) and agent execution (OpenAI SDK).
-   **Questions**:
    -   What types of errors can occur in each component?
    -   How should the system gracefully handle these errors?
    -   What feedback should be provided to the user?
    -   Are retry mechanisms necessary?
-   **Findings**:
    -   **OpenAI Agents SDK Graceful Tool Failures:** Use `failure_error_function` in `@function_tool` to convert Python exceptions into LLM-readable messages, preventing crashes.
    -   **Handling Qdrant & Embedding Errors:**
        -   **Connection Issues:** Catch `UnexpectedResponse` or gRPC errors from Qdrant.
        -   **Empty Results:** Return specific messages like "No relevant documents found" if Qdrant returns no matches to prevent hallucination.
        -   **Embedding Failures:** Catch API errors (e.g., rate limits, timeouts) from the embedding model.
        -   Wrap retrieval logic in try-except blocks to return helpful messages to the Agent/user.
    -   **SDK-Level Exception Handling:** Wrap `agent.run()` calls to catch SDK-specific exceptions outside of tools:
        -   `ToolTimeoutError`: A tool took too long; increase `timeout_seconds`.
        -   `ModelBehaviorError`: LLM called non-existent tool or sent bad JSON; enable `strict_mode=True`.
        -   `MaxTurnsExceeded`: Agent stuck in a loop; increase `max_turns` or refine prompt.
        -   `GuardrailTripwireTriggered`: Violation of safety guardrail; log and inform user.
    -   **Best Practices for RAG Stability:**
        -   **Strict Mode:** Use `@function_tool(strict_mode=True)` to enforce JSON schema, reducing "Malformed Tool Call" errors.
        -   **Context Window Management:** Truncate large documents or use a reranker to prevent exceeding LLM's token limit.
        -   **Logging & Tracing:** Use SDK's built-in tracing or external tools (LangSmith/Arize Phoenix) to debug RAG chain failures.
        -   **Fallback Agents:** Use **Handoff** to pass control to a general-purpose agent or human if RAG repeatedly fails.
    -   Decision: Implement comprehensive error handling at multiple layers. Utilize `failure_error_function` for tool-level errors. Explicitly handle Qdrant and embedding service errors (connection, empty results, API failures) within retrieval tools. Implement SDK-level exception handling for agent runtime issues and incorporate RAG stability best practices like `strict_mode`, context window management, logging, and tracing. Consider fallback agents for persistent failures.
    -   Rationale: Layered error handling ensures robustness and resilience across the entire RAG pipeline, providing graceful degradation and better user experience. Explicit handling prevents crashes and guides the agent towards recovery or informing the user.
    -   Alternatives Considered:
        -   Basic try-except blocks only: Less granular, harder to debug, poor user feedback.
        -   Relying solely on SDK defaults: May not cover specific Qdrant/embedding service failures adequately.

### 4. Best Practices for OpenAI Agents SDK

-   **Description**: Gather general best practices for effectively using the OpenAI Agents SDK for building robust and performant agents.
-   **Questions**:
    -   What are common pitfalls to avoid?
    -   Tips for tool usage, agent configuration, and state management.
-   **Findings**:
    -   **Modular Agents over Monoliths:** Break complex tasks into specialized agents (e.g., `ResearchAgent`, `WriterAgent`) to simplify debugging and enable cost-effective model usage.
    -   **Handoffs for Delegation:** Use `handoff` primitive to transfer control between agents while maintaining conversation state, allowing generalist agents to pass users to specialists.
    -   **Deterministic Flows:** Use standard Python logic for known step sequences; avoid forcing LLM to decide if the flow is always the same.
    -   **Agents as Tools:** Treat entire agents as tools callable by other agents (e.g., a "Manager" agent calling a "DataAnalyst" agent).
    -   **Security & Safety (Guardrails):**
        -   **Input & Output Guardrails:** Implement to catch prompt injections, PII, off-topic requests (input) or validate against business rules/sensitive data (output).
        -   **"Tripwires":** Configure guardrails to trigger exceptions (e.g., `InputGuardrailTripwireTriggered`) for immediate halt on safety violations.
        -   **Least Privilege:** Grant agents only necessary tool access (e.g., read-only if write/delete is not needed).
        -   **Human-in-the-Loop (HITL):** Pause execution for human approval on high-stakes actions.
    -   **Performance & Optimization:**
        -   **Async & Streaming:** Use `Runner.run_streamed()` or `Runner.run()` (async) for production to prevent blocking and improve UX.
        -   **Context Management:** Use summarization strategies for long sessions to prevent "context drowning" and hallucinations.
        -   **Structured Outputs:** Utilize Pydantic-powered function tools for automatic schema generation, ensuring valid, structured data.
        -   **Parallel Execution:** Use `asyncio` for concurrent execution of independent tools to reduce latency.
    -   **Development & Debugging:**
        -   **Built-in Tracing:** Leverage native tracing to visualize agent loops, tool calls, and handoffs for debugging "dead loops."
        -   **Clear Instructions:** Treat agent instructions as job descriptions, defining role, boundaries, and routine steps.
        -   **Evals and Red-Teaming:** Use OpenAI Evals to simulate adversarial inputs and measure guardrail effectiveness.
    -   Decision: Adopt a modular agent architecture, utilizing handoffs for delegation. Implement robust input/output guardrails with tripwires and least privilege for tools. Optimize for performance using async/streaming, structured outputs via Pydantic, and parallel execution. Leverage built-in tracing for debugging and ensure clear agent instructions.
    -   Rationale: These practices promote maintainability, scalability, robustness, and safety in agent development, crucial for production-ready RAG systems.
    -   Alternatives Considered:
        -   Monolithic agent design: Less maintainable, harder to debug, less flexible.
        -   Ignoring guardrails/safety: High risk of security vulnerabilities and unreliable behavior.
        -   Synchronous execution: Poor performance and user experience in production.

### 5. Best Practices for Qdrant Cloud

-   **Description**: Investigate best practices for managing and querying a Qdrant Cloud instance for vector search.
-   **Questions**:
    -   Indexing strategies and optimization.
    -   Scalability considerations.
    -   Data synchronization and updates.
-   **Findings**:
    -   **Indexing & Search Optimization (HNSW):** Tune HNSW parameters (`m`, `ef_construct`, `ef`) to balance search speed, memory, and precision. Higher `m` and `ef_construct` improve recall but increase resource usage. `ef` is a query-time parameter for accuracy.
    -   **Memory Management & Quantization:**
        -   **Scalar Quantization (int8):** Reduce memory by 4x with minimal precision loss (often <1%).
        -   **Binary Quantization:** Reduce memory by up to 32x for massive speedups (may need re-scoring).
        -   **On-Disk Storage:** Store original vectors on disk while keeping quantized versions or HNSW index in RAM to save costs.
    -   **Efficient Filtering with Payload Indexes:** Always create indexes for fields used in filters. This enables Qdrant's efficient "filterable HNSW" and pre-filtering capabilities, which are faster than post-filtering. Indexes are most effective on high-cardinality fields.
    -   **Production & Architecture Best Practices:**
        -   **Batching:** Use `upsert` with batches for ingestion throughput.
        -   **Named Vectors:** Store multiple embedding models as named vectors in a single collection.
        -   **Hybrid Search:** Combine dense and sparse vectors for optimal retrieval in RAG systems.
        -   **Read-only Replicas:** Use replication for load distribution and high availability in Qdrant Cloud.
    -   Decision: Optimize Qdrant indexing with tuned HNSW parameters. Implement scalar quantization for memory efficiency. Utilize payload indexing for efficient filtering. Employ batching for data ingestion and consider read-only replicas for production scalability.
    -   Rationale: These practices ensure optimal performance, cost efficiency, and scalability for the vector store, which is critical for the RAG pipeline.
    -   Alternatives Considered:
        -   Default HNSW parameters: Sub-optimal performance for specific use cases.
        -   No quantization: Higher memory consumption, increased costs.
        -   No payload indexing: Slow filter operations.

### 6. Best Practices for Cohere Embeddings

-   **Description**: Understand best practices for using Cohere embeddings, especially concerning consistency with ingestion and query embedding.
-   **Questions**:
    -   Optimal model choice for book content.
    -   Token limits and chunking strategies.
    -   Performance considerations.
-   **Findings**:
    -   **Use Correct `input_type`**: Crucial for asymmetric models (Embed v3/v4). Use `search_document` for chunks and `search_query` for user questions.
    -   **Two-Stage Retrieval (Reranking)**: Most effective RAG uses Embed v3/v4 for initial retrieval (top 50-100 candidates) then Cohere Rerank (e.g., `rerank-english-v3.0`) for precise selection.
    -   **Optimized Chunking Strategy**: Aim for 300-500 tokens with 10-20% overlap. Semantic chunking preferred over fixed character counts.
    -   **Multimodal & Multilingual Capabilities**: Use `embed-multilingual-v3.0` or `v4.0` for multi-language data. `Embed v4` supports multimodal (text and images) embeddings.
    -   **Efficiency and Cost Optimization**: Quantization (int8, binary) for storage reduction (up to 80%). Matryoshka Embeddings (MRL) for truncating embeddings to reduce latency.
    -   **Production Architecture**: Combine Embedding Model (`embed-english-v3.0` or `v4.0`), Vector Database (Qdrant supporting `int8`), Reranker (`rerank-english-v3.0`), and Generation Model (`command-r-plus`).
    -   **Pro Tip (Chat endpoint with RAG)**: Pass retrieved documents directly into the `documents` parameter for inline citations and reduced hallucinations.
    -   Decision: Utilize Cohere Embed v3/v4 with appropriate `input_type` (`search_document` for chunks, `search_query` for queries). Implement a two-stage retrieval process with Cohere Rerank for improved precision. Employ an optimized chunking strategy (300-500 tokens, 10-20% overlap) with preference for semantic chunking.
    -   Rationale: These practices ensure high accuracy, efficiency, and robustness for the embedding and retrieval process, crucial for the RAG agent's performance.
    -   Alternatives Considered:
        -   Single-stage retrieval without reranking: Lower precision, higher risk of irrelevant context.
        -   Fixed character chunking without overlap: Potential loss of semantic meaning at chunk boundaries.
        -   Ignoring `input_type`: Sub-optimal embedding quality for RAG.

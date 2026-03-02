# ADR-001: RAG Agent Top_K Retrieval Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-27
- **Feature:** 008-rag-agent-retrieval
- **Context:** The RAG Agent feature requires retrieving relevant text chunks from a Qdrant vector store to provide context for AI agent responses. The number of chunks to retrieve (`top_k`) is a critical decision impacting system performance, cost, and the quality of generated answers.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

The RAG agent will retrieve 5 `top_k` relevant text chunks from Qdrant when processing a user query.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Provides a balanced amount of context to the agent, reducing prompt size and cost compared to larger `top_k` values.
- Reduces the risk of missing relevant information compared to smaller `top_k` values.
- Likely to improve the grounding of the agent's responses.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

- May still miss some relevant information if the optimal `top_k` is higher for certain queries.
- Could lead to higher costs and slower response times compared to a `top_k` of 1 or 3, though less than very high `top_k`.
- Requires careful tuning and monitoring to ensure it remains optimal as the dataset or query patterns change.

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- **`top_k` = 3:**
    - **Pros:** Lower cost, smaller prompt, faster processing.
    - **Cons:** Higher risk of missing relevant context, potentially leading to less accurate or incomplete answers, increased hallucination risk.
- **`top_k` = 10:**
    - **Pros:** More comprehensive context, lower risk of missing relevant information.
    - **Cons:** Higher cost due to larger prompt, slower processing, potential for increased noise in the context, potentially exceeding LLM context window limits.
- **Dynamic `top_k`:**
    - **Pros:** Potentially optimal retrieval for each query, adapting to varying information needs.
    - **Cons:** Significant implementation complexity, increased overhead for determining `top_k` dynamically, might introduce inconsistencies. (Considered a future enhancement).

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: `specs/008-rag-agent-retrieval/spec.md`
- Implementation Plan: null
- Related ADRs: null
- Evaluator Evidence: null <!-- link to eval notes/PHR showing graders and outcomes -->

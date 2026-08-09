# LangGraph checkpoint pain notes

- Sources:
  - https://github.com/langchain-ai/langgraph/issues/7714
  - https://github.com/langchain-ai/langgraph/issues/7263
  - https://github.com/langchain-ai/langgraph/issues/5790
  - https://github.com/langchain-ai/langgraph/issues/5672
  - https://github.com/langchain-ai/langgraph/issues/7417
- Date range: 2025-05-13 to 2026-05-05
- Family: ai-llm-demand
- Signal type: operational-risk
- Labels: M2 repeated pain, M3 competitor proof, M4 workaround evidence
- Notes: checkpoint serialization bloats storage and tokens; related issues show ignored persistent checkpointers, streaming state loss, and silent re-dispatch from checkpoint.

# LangGraph checkpoint pain notes

- Source: https://github.com/langchain-ai/langgraph/issues/7714
- Date: 2026-05-05
- Family: ai-llm-demand
- Signal type: operational-risk
- Labels: M2 repeated pain, M4 workaround evidence
- Notes: checkpoint serialization bloats storage and tokens; related issues show ignored persistent checkpointers, streaming state loss, and silent re-dispatch from checkpoint.

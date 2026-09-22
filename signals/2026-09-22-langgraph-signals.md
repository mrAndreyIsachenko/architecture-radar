# LangGraph Demand Signals 2026-09-22

- Family: `ai-llm-demand`
- Source date range: `2026-06-30` to `2026-09-22`
- Signal type: `operational-risk`
- Source class: `github`
- Signal types: `operational-risk`, `workaround-economy`
- Source classes: `docs`, `github`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: LangGraph continues to surface checkpoint, replay, and pruning pain, but the evidence still looks like internal operational glue rather than a clearly purchased outside audit workflow.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx | 2026-09-20 crawl | workaround-economy | docs | M4 workaround evidence | The docs explain persistent checkpointers, pruning, and cost-control workarounds. |
| https://github.com/langchain-ai/langgraph/issues/8234 | 2026-06-30 | operational-risk | github | M2 repeated pain | Crash recovery can restore inconsistent state when checkpoint ordering is not enforced. |
| https://github.com/langchain-ai/langgraph/issues/8358 | 2026-07-17 | operational-risk | github | M2 repeated pain | Protocol-v2 replay lacks a durable run/checkpoint boundary after thread hydration. |
| https://github.com/langchain-ai/langgraph/issues/8531 | 2026-08-05 | operational-risk | github | M2 repeated pain | Safe prune support for Postgres checkpointers is still an open product need. |

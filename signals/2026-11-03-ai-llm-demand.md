# 2026-11-03 ai-llm-demand

- Source date range: 2026-06-30 to 2026-11-03
- Family: `ai-llm-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Notes: RightNow / RunInfra is a launch seed for paid GPU inference infrastructure, while LangGraph issues and docs still show repeated checkpoint, replay, and persistence pain. This family still has clear technical pain, but the buyer-confirmed external audit wedge remains weak.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/rightnow | 2026-11-03 crawl | company-launch | launch | H hypothesis | RightNow is a launch seed for GPU infrastructure and pay-per-token model serving, but it is not direct proof of a buyer for an external audit wedge. |
| https://github.com/langchain-ai/langgraph/issues/8298 | 2026-07-08 | operational-risk | github | M2 repeated pain | Checkpoints never flush mid-session in `langgraph dev`, so clean shutdown is not enough for durability. |
| https://github.com/langchain-ai/langgraph/issues/8234 | 2026-06-30 | operational-risk | github | M2 repeated pain | `durability="sync"` ordering can restore inconsistent state after crash recovery. |
| https://github.com/langchain-ai/langgraph/issues/8458 | 2026-07-27 | operational-risk | github | M2 repeated pain | Replay from a subgraph checkpoint can rerun the whole subgraph from `__start__`. |
| https://github.com/langchain-ai/langgraph/issues/9245 | 2026-10-08 | operational-risk | github | M2 repeated pain | One failed checkpoint save can permanently drop state from a thread under default async durability. |
| https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx | 2026-11-02 crawl | workaround-economy | docs | M4 workaround evidence | The docs tell users to manage checkpoint size, retention, and storage behavior manually for production. |
| https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/checkpointers.mdx | 2026-11-03 crawl | workaround-economy | docs | M4 workaround evidence | The docs spell out durability tradeoffs and recovery limits, which is a sign the operational workflow is still being tuned by hand. |

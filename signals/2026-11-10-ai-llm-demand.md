# 2026-11-10 ai-llm-demand

- Source date range: 2026-06-30 to 2026-11-10
- Family: `ai-llm-demand`
Signal type: `paid-demand`
Source class: `product`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
Notes: RightNow and RunInfra make the paid agent-inference stack explicit, but LangGraph remains the stronger watchlist candidate because the pain repeats while the external spend wedge still looks too core.
- Topic family: `ai-llm-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/rightnow | 2026-11-10 crawl | company-launch | launch | H hypothesis | YC profile is a timing seed only; it shows a live launch around agent inference infrastructure, not buyer proof for a separate wedge. |
| https://runinfra.ai/ | 2026-11-10 crawl | paid-demand | product | M1 paid demand | RunInfra publishes paid hosted model APIs, agent-oriented routing, and measured cost/performance claims, which proves direct spend for inference infrastructure. |
| https://runinfra.ai/pricing | 2026-11-10 crawl | paid-demand | pricing | M1 paid demand | Public credit top-ups, model token prices, and enterprise terms make the spend model explicit. |
| https://github.com/langchain-ai/langgraph/issues | 2026-11-10 crawl | operational-risk | github | M2 repeated pain | The live issue feed keeps surfacing replay, checkpoint, and streaming failures across production LangGraph use. |
| https://github.com/langchain-ai/langgraph/issues/8234 | 2026-06-30 | operational-risk | github | M2 repeated pain | Crash recovery can restore inconsistent state when write/checkpoint ordering is not enforced. |
| https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/checkpointers.mdx | 2026-11-06 crawl | workaround-economy | docs | M4 workaround evidence | The docs still tell users to reason about checkpoint and replay behavior manually, which keeps the persistence layer inspectable but not yet commercially clean. |
- Topic family: `ai-llm-demand`

## Sources
- `https://www.ycombinator.com/companies/rightnow`
  - Signal: `company-launch`
  - Class: `launch`
  - Label: `H hypothesis`
  - Note: YC profile is a timing seed only; it shows a live launch around agent inference infrastructure, not buyer proof for a separate wedge.
- `https://runinfra.ai/`
  - Signal: `paid-demand`
  - Class: `product`
  - Label: `M1 paid demand`
  - Note: RunInfra publishes paid hosted model APIs, agent-oriented routing, and measured cost/performance claims, which proves direct spend for inference infrastructure.
- `https://runinfra.ai/pricing`
  - Signal: `paid-demand`
  - Class: `pricing`
  - Label: `M1 paid demand`
  - Note: Public credit top-ups, model token prices, and enterprise terms make the spend model explicit.
- `https://github.com/langchain-ai/langgraph/issues`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: The live issue feed keeps surfacing replay, checkpoint, and streaming failures across production LangGraph use.
- `https://github.com/langchain-ai/langgraph/issues/8234`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: Crash recovery can restore inconsistent state when write/checkpoint ordering is not enforced.
- `https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/checkpointers.mdx`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: The docs still tell users to reason about checkpoint and replay behavior manually, which keeps the persistence layer inspectable but not yet commercially clean.

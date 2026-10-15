# AI LLM Demand Signals - 2026-10-06

Date: 2026-10-06
Family: `ai-llm-demand`
Signal type: `operational-risk`
Source class: `github`
Labels: `M1 paid demand`, `M2 repeated pain`, `M3 competitor proof`, `M4 workaround evidence`
Notes: This note groups the current paid infrastructure seed, the LangGraph issue feed, and the replay and checkpoint docs into one family view.

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| RightNow YC profile | https://www.ycombinator.com/companies/rightnow | 2026-10-06 crawl | company-launch | launch | H hypothesis | Launch seed only; useful timing signal for GPU inference, not buyer proof for the external wedge. |
| RunInfra homepage | https://runinfra.ai/ | 2026-10-03 crawl | paid-demand | product | M3 competitor proof | Commercialized open-model inference stack shows a real buyer-facing product, but not a separate diagnostics wedge. |
| RunInfra pricing | https://runinfra.ai/pricing | 2026-10-03 crawl | paid-demand | pricing | M1 paid demand | Credits, pay-as-you-go tokens, and enterprise terms prove direct spend on inference infrastructure. |
| RunInfra L4 GPU page | https://runinfra.ai/gpu/l4 | 2026-09-10 publish | paid-demand | pricing | M1 paid demand | Published GPU-hour rates make capacity and optimization spend explicit. |
| LangGraph issues page | https://github.com/langchain-ai/langgraph/issues | 2026-10-06 crawl | operational-risk | github | M2 repeated pain | Current issue feed still shows active checkpoint, replay, and persistence pain across production use. |
| LangGraph issue 8458 | https://github.com/langchain-ai/langgraph/issues/8458 | 2026-07-27 | operational-risk | github | M2 repeated pain | Replay from a subgraph checkpoint reruns the whole subgraph from `__start__`. |
| LangGraph issue 8358 | https://github.com/langchain-ai/langgraph/issues/8358 | 2026-07-17 | operational-risk | github | M2 repeated pain | Agent Server protocol v2 still lacks a durable replay boundary after thread hydration. |
| LangGraph issue 6728 | https://github.com/langchain-ai/langgraph/issues/6728 | 2026-01-29 | operational-risk | github | M2 repeated pain | Duplicate subgraph execution can fork checkpoints under identical run identifiers. |
| LangGraph functional API docs | https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/functional-api.mdx | 2026-10-01 crawl | workaround-economy | docs | M4 workaround evidence | Docs explain manual replay and checkpoint behavior, which is itself evidence of tuning work at the boundary. |

## Notes
- M1 paid demand: RunInfra pricing proves direct spend on model-serving infrastructure.
- M2 repeated pain: LangGraph issues keep surfacing replay, checkpoint, and durability failures.
- M3 competitor proof: RunInfra is a commercial product, so the market exists even though the external audit wedge is not proven.
- M4 workaround evidence: LangGraph docs still teach users how to reason about replay and checkpoint restoration manually.

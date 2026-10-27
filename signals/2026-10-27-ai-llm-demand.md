# ai-llm-demand signal note, 2026-10-27

- Source date range: 2026-07-17 to 2026-10-27 crawl.
- Family: `ai-llm-demand`
Signal type: `paid-demand`
Source class: `pricing`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
Notes: RightNow and RunInfra prove paid AI-infrastructure spend, while LangGraph issues and docs show recurring checkpoint and replay pain. The wedge remains too core for a separate commercial service.
- Topic family: `ai-llm-demand`

## Sources

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| RightNow YC profile | https://www.ycombinator.com/companies/rightnow | 2026-10-27 crawl | company-launch | launch | `H hypothesis` | YC launch seed for RunInfra and GPU optimization; useful timing signal, not buyer proof. |
| RunInfra homepage | https://runinfra.ai/ | 2026-10-27 crawl | paid-demand | product | `M1 paid demand` | Public hosted model APIs, session-aware routing, and pay-as-you-go usage show direct spend. |
| RunInfra pricing | https://runinfra.ai/pricing | 2026-10-27 crawl | paid-demand | pricing | `M1 paid demand` | Public token pricing, enterprise terms, and credit top-ups make the monetized workflow explicit. |
| LangGraph checkpoint docs | https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/checkpointers.mdx | 2026-10-27 crawl | workaround-economy | docs | `M4 workaround evidence` | Docs describe checkpoint replay, retention, and manual saver choices. |
| LangGraph issue 8234 | https://github.com/langchain-ai/langgraph/issues/8234 | Opened Jul 2026 | operational-risk | github | `M2 repeated pain` | Crash recovery can restore inconsistent state when write and checkpoint ordering is not enforced. |
| LangGraph issue 8358 | https://github.com/langchain-ai/langgraph/issues/8358 | Opened Jul 2026 | operational-risk | github | `M2 repeated pain` | Protocol-v2 replay can miss a durable run/checkpoint boundary after thread hydration. |
| LangGraph issue 8458 | https://github.com/langchain-ai/langgraph/issues/8458 | Opened Jul 2026 | operational-risk | github | `M2 repeated pain` | Time travel to a subgraph checkpoint can rerun the whole subgraph from `__start__`. |

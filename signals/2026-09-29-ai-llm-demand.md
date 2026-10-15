# 2026-09-29 AI/LLM Demand Signals

- Family: `ai-llm-demand`
- Source date range: 2026-09-29 crawl, with one launch seed from 2026 YC batch page and current public docs/issues.
- Signal type: `operational-risk`
- Source class: `github`
- Signal types: `company-launch`, `paid-demand`, `operational-risk`, `workaround-economy`
- Source classes: `launch`, `product`, `pricing`, `github`, `docs`
- Market evidence labels: `H hypothesis`, `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `H hypothesis`, `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: RightNow / RunInfra is a real paid inference product, but the external wedge still looks too core to the buyer stack. LangGraph still shows repeated checkpoint and replay pain, but the evidence remains watchlist-grade rather than buyer-confirmed spend.

## Sources

- `https://www.ycombinator.com/companies/rightnow` | source class: `launch` | signal type: `company-launch` | evidence label: `H hypothesis` | note: YC profile confirms the company and positioning, but it is only a discovery seed and not demand proof.
- `https://runinfra.ai/` | source class: `product` | signal type: `paid-demand` | evidence label: `M1 paid demand` | note: RunInfra advertises hosted model APIs, optimization, and agent infrastructure as a commercial product.
- `https://runinfra.ai/pricing` | source class: `pricing` | signal type: `paid-demand` | evidence label: `M1 paid demand` | note: Published pricing and prepaid credits show direct spend for inference infrastructure.
- `https://github.com/langchain-ai/langgraph/issues/8358` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: Initial replay lacks a durable run/checkpoint boundary after thread hydration.
- `https://github.com/langchain-ai/langgraph/issues/8234` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: Checkpoint ordering can restore inconsistent state after crash recovery.
- `https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: The persistence docs discuss pruning and retention because checkpoint growth and replay cost still need manual attention.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/rightnow | 2026-09-29 crawl | company-launch | launch | H hypothesis | YC profile confirms the company and positioning, but it is only a discovery seed and not demand proof. |
| https://runinfra.ai/ | 2026-09-29 crawl | paid-demand | product | M1 paid demand | RunInfra advertises hosted model APIs, optimization, and agent infrastructure as a commercial product. |
| https://runinfra.ai/pricing | 2026-09-29 crawl | paid-demand | pricing | M1 paid demand | Published pricing and prepaid credits show direct spend for inference infrastructure. |
| https://github.com/langchain-ai/langgraph/issues/8358 | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | Initial replay lacks a durable run/checkpoint boundary after thread hydration. |
| https://github.com/langchain-ai/langgraph/issues/8234 | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | Checkpoint ordering can restore inconsistent state after crash recovery. |
| https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | The persistence docs discuss pruning and retention because checkpoint growth and replay cost still need manual attention. |

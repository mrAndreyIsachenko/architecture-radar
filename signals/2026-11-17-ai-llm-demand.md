# 2026-11-17 ai-llm-demand

- Source date range: 2026-11-13 to 2026-11-17
- Family: `ai-llm-demand`
- Signal type: `paid-demand`
- Source class: `pricing`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Notes: RightNow shows a live paid AI-infrastructure workflow, while LangGraph docs and issues still show checkpoint, memory, and replay pain. The commercial wedge remains too core to the underlying stack, so the family stays watchlisted.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/rightnow | 2026-11-17 crawl | company-launch | launch | H hypothesis | YC profile is a timing seed only; it shows a live company launch around model-serving infrastructure, not buyer proof for a separate wedge. |
| https://www.rightnowai.co/docs/open-models/pricing | 2026-11-13 | paid-demand | pricing | M1 paid demand | Public credit top-ups and published model rates prove direct spend for AI inference infrastructure. |
| https://www.rightnowai.co/docs/decision-model/pricing | 2026-11-13 | paid-demand | pricing | M1 paid demand | The decision-model docs expose explicit per-token and per-call pricing for a paid workflow. |
| https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx | 2026-11-12 crawl | workaround-economy | docs | M4 workaround evidence | The docs tell users to prune checkpoints and manage retention manually. |
| https://github.com/langchain-ai/langgraph/issues/8234 | 2026-10-30 crawl | operational-risk | github | M2 repeated pain | Crash recovery can restore inconsistent state when write/checkpoint ordering is not enforced. |

## Sources
- `https://www.ycombinator.com/companies/rightnow`
- `https://www.rightnowai.co/docs/open-models/pricing`
- `https://www.rightnowai.co/docs/decision-model/pricing`
- `https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx`
- `https://github.com/langchain-ai/langgraph/issues/8234`

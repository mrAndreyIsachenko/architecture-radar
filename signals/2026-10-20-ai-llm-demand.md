# 2026-10-20 ai-llm-demand

- Source date range: 2026-03-31 to 2026-10-20
- Family: `ai-llm-demand`
- Signal type: `paid-demand`
- Source class: `news`
- Evidence label: `M1 paid demand`
- Labels: `H hypothesis`, `M1 paid demand`, `M2 repeated pain`
- Signal types: `company-launch`, `paid-demand`, `operational-risk`
- Source classes: `launch`, `product`, `pricing`, `news`, `github`
- Evidence labels: `H hypothesis`, `M1 paid demand`, `M2 repeated pain`
- Notes: RightNow / RunInfra is a real paid inference signal and timing seed, but the external wedge still looks too core. LangGraph still shows repeated replay and checkpoint pain, but not direct standalone audit spend.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/rightnow | 2026-10-19 crawl | company-launch | launch | H hypothesis | YC profile confirms the company and positioning, but does not by itself prove buyer demand for an external wedge. |
| https://runinfra.ai/ | 2026-10-20 crawl | paid-demand | product | M1 paid demand | Hosted model APIs, agent-focused routing, and token pricing show direct spend on the inference stack. |
| https://runinfra.ai/pricing | 2026-10-20 crawl | paid-demand | pricing | M1 paid demand | Public top-ups, usage pricing, and enterprise terms make the spend model explicit. |
| https://runinfra.ai/news/inference-for-agents | 2026-10-01 publish | paid-demand | news | M1 paid demand | The news post reframes RunInfra around hosted inference for agents and codifies the buyer-facing product. |
| https://github.com/langchain-ai/langgraph/issues | 2026-10-20 crawl | operational-risk | github | M2 repeated pain | The live issue feed still shows new replay, checkpoint, and serialization pain. |
| https://github.com/langchain-ai/langgraph/issues/8234 | 2026-10-09 issue | operational-risk | github | M2 repeated pain | Replay vs. re-execute ordering can restore inconsistent state after crashes. |
| https://github.com/langchain-ai/langgraph/issues/9253 | 2026-10-09 issue | operational-risk | github | M2 repeated pain | A retry policy across subgraphs can resume into the wrong checkpoint boundary. |

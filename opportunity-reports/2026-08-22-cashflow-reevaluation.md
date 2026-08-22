# Opportunity Radar Cashflow Re-evaluation 2026-08-22

## Prerequisites And State
- This is a dry-run re-evaluation of existing opportunities after the cashflow-first rules were introduced.
- `opportunities.json` was migrated to `schema_version: 2`.
- Existing opportunities reviewed: 3.
- Selected opportunities after re-evaluation: 0.
- Watchlisted opportunities after re-evaluation: 3.

## Best Paths To First Transaction
None. No current opportunity clears the required combination of direct or near-direct money evidence, reachable buyer, concrete offer, manual delivery path, and `time_to_transaction_score >= 3`.

## Signal Counts
- Re-evaluated opportunities: 3
- Direct paid workflow evidence: 0
- Budget adjacency only: 2
- No money evidence: 1
- Promoted to sell-before-build: 0
- Demoted from sell-before-build: 1

## Selected Opportunities
None.

## Executive Summary
- The cashflow-first filter removes LangGraph from `sell-before-build` because its current proof is technical pain plus adjacent ecosystem budget, not direct checkpoint-audit spend.
- Tailscale stays watchlisted for the same reason: pricing and admin pain are real, but external routing diagnostics are not yet a proven paid workflow.
- ArduPilot stays watchlisted because the technical need is plausible but first transaction depends on private logs and operator trust.
- The strongest next action is to search for direct paid manual workflows, not to build any of the three tools.

## Signal Ledger
| Source | URL | Family | Signal type | Source class | Evidence label | Decision | Reason |
|---|---|---|---|---|---|---|---|
| LangGraph checkpoint issue | https://github.com/langchain-ai/langgraph/issues/7714 | `ai-llm-demand` | `operational-risk` | `github` | `M2 repeated pain` | watchlisted | Strong technical pain, but not direct paid workflow evidence. |
| Tailscale pricing page | https://tailscale.com/pricing | `privacy-networking-demand` | `paid-demand` | `pricing` | `M1 paid demand` | watchlisted | Shows adjacent networking budget, not payment for an external diagnostic. |
| ArduPilot log diagnosis forum | https://discuss.ardupilot.org/t/gsoc-2026-an-automated-log-diagnosis-engine/142949 | `drones-robotics-demand` | `workaround-economy` | `forum` | `M4 workaround evidence` | watchlisted | Shows interest in easier log review, but not external paid spend. |

## Interesting But Not Yet Commercial
- LangGraph remains interesting as agent-runtime operational pain, but it needs direct paid workflow evidence before another build-oriented recommendation.
- Tailscale remains interesting as privacy-networking admin friction, but the next proof must be paid admin work, procurement, or a buyer asking for a routing review.
- ArduPilot remains interesting as drone telemetry safety workflow, but private data access and operator trust block a fast first transaction.

## Topic Coverage
| Family | Signals reviewed | Best candidate | Decision | Reason |
|---|---:|---|---|---|
| `ai-llm-demand` | 1 | LangGraph Checkpoint Persistence And Cost Diagnostics | watchlisted | Technical pain remains strong, but the money evidence is budget adjacency rather than direct paid workflow spend. |
| `blockchain-demand` | 0 | None found | no fresh candidate | This dry-run only re-evaluated existing opportunities and did not run new blockchain discovery. |
| `privacy-networking-demand` | 1 | Tailscale Split-Tunnel Routing Exception Diagnostics | watchlisted | Admin pain is visible, but public evidence still lacks direct payment for an external routing diagnostic. |
| `drones-robotics-demand` | 1 | ArduPilot Telemetry Integrity And Failsafe Diagnostics | watchlisted | Telemetry pain is real, but first transaction is blocked by private log access and missing paid review evidence. |
| `document-ai-demand` | 0 | None found | no fresh candidate | This dry-run only re-evaluated existing opportunities and did not run new document AI discovery. |

## Commercial Delta
| Opportunity | Previous stage | Current stage | Commercial delta | Decision |
|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | sell-before-build | watchlisted | New cashflow filter reclassifies GitHub issues plus public hiring and adjacent platform budget as budget adjacency, not direct spend. | demoted to watchlist |
| Tailscale Split-Tunnel Routing Exception Diagnostics | watchlisted | watchlisted | No new direct buyer, procurement, freelance, or paid diagnostic signal was added; adjacent admin budget remains insufficient. | carried-forward |
| ArduPilot Telemetry Integrity And Failsafe Diagnostics | watchlisted | watchlisted | No direct operator spend was found, and useful validation still appears to require private logs. | carried-forward |

## Structural Candidate Ranking
| Rank | Opportunity | Ecosystem | Score | Why now | Manual workflow | Wedge |
|---|---|---|---|---|---|---|
| 1 | LangGraph Checkpoint Persistence And Cost Diagnostics | LangGraph agent runtime and observability ecosystem | 6 | Production LangGraph usage, platformization, and public checkpoint issues clustered in 2025-2026, making this a recent agent-runtime fragmentation problem. | Engineers manually inspect issues, checkpoint payloads, trace exports, storage growth, and replay behavior to choose saver settings and diagnose duplicate execution. | Checkpoint audit report for one exported workflow that compares storage growth, replay fidelity, duplicate execution risk, and saver configuration. |
| 2 | Tailscale Split-Tunnel Routing Exception Diagnostics | Tailscale overlay-network and VPN administration ecosystem | 5 | Tailscale routing primitives, pricing, and docs became more productized in 2025-2026, but public threads still show split-tunnel and exception confusion. | Admins manually compare docs, issue threads, device routing tables, DNS behavior, and policy settings to explain why traffic exits through the wrong path. | Routing-policy review report for one exit-node, split-DNS, or app-connector scenario that predicts likely exception failures. |
| 3 | ArduPilot Telemetry Integrity And Failsafe Diagnostics | ArduPilot drone telemetry and failsafe operations ecosystem | 4 | Recent public work around telemetry counters and log diagnosis makes the workflow more inspectable, but the market timing remains weaker than the AI/runtime case. | Operators manually inspect logs, forum guidance, telemetry counters, and mission events to decide whether packet loss or telemetry gaps affected safety. | Telemetry-integrity report for one uploaded log set that flags packet loss, failsafe transitions, and suspicious telemetry gaps. |

## Structural Score Breakdown
| Opportunity | Fragmentation | Manual pain | Economic value | Objective measurability | Execution potential | Timing | Competition gap | Prototype feasibility | Total |
|---|---|---|---|---|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | 4 | 5 | 4 | 4 | 4 | 4 | 3 | 4 | 8 |
| Tailscale Split-Tunnel Routing Exception Diagnostics | 4 | 4 | 3 | 3 | 3 | 3 | 2 | 3 | 6 |
| ArduPilot Telemetry Integrity And Failsafe Diagnostics | 3 | 4 | 2 | 3 | 2 | 3 | 2 | 2 | 5 |

## Commercial Filter
| Opportunity | Fragmented providers | Multi-provider user | Boundary workflow | Build-vs-buy | Internal build likelihood | Money flow | Permissionless validation | Smallest wedge | Decision |
|---|---|---|---|---|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | LangGraph runtime, checkpointer packages, LangSmith observability, hosted platform paths, and storage backends create several operational provider surfaces rather than one stable workflow. | LangGraph production teams commonly combine the LangGraph runtime, LangSmith traces, and a separate checkpoint store or deployment platform, so the audit sits across more than one provider boundary. | Teams reconcile checkpoint records, trace exports, storage growth, replay behavior, issue evidence, and platform settings across runtime, observability, and persistence boundaries. | A narrow audit could be bought by small teams or consultants because it is repeated operational glue, but larger platform teams could build internal diagnostics themselves. | medium | Money flows through LangChain products, cloud storage, and agent engineering labor, but direct external checkpoint-audit spend remains unproven. | A first report can be tested with public examples, synthetic checkpoint traces, and exported local workflows before asking for private customer traces. | Checkpoint audit report for one exported workflow that compares storage growth, replay fidelity, duplicate execution risk, and saver configuration. | watchlisted |
| Tailscale Split-Tunnel Routing Exception Diagnostics | Tailscale, Mullvad-style VPN use, OS routing tables, DNS controls, app connectors, and legacy VPN expectations create fragmented networking surfaces. | Admins and power users can combine Tailscale with other VPNs, OS routing, DNS providers, and app-specific exceptions, but direct budgeted multi-provider diagnostic demand remains weak. | The boundary workflow is explaining route, DNS, exit-node, browser, and app-connector behavior across overlay network, VPN, OS, and SaaS policy layers. | A policy review is non-core admin glue for small teams, but Tailscale or incumbent network tooling could absorb the diagnostic path upstream. | medium | Money flows through Tailscale paid plans, enterprise network administration, and VPN subscriptions, but direct external routing-diagnostic spend is not proven. | A first test can use public docs, synthetic route tables, sample DNS policies, and local repro scripts without needing private production networks. | Routing-policy review report for one exit-node, split-DNS, or app-connector scenario that predicts likely exception failures. | watchlisted |
| ArduPilot Telemetry Integrity And Failsafe Diagnostics | ArduPilot firmware, ESC telemetry, DShot or BDShot counters, ground-control software, logs, failsafe configuration, and operator procedures fragment the evidence surface. | Drone operators bridge flight-controller firmware, ESC hardware telemetry, ground-control tools, log analyzers, and integrator practices, but paid multi-vendor buyer evidence is weak. | The boundary workflow is reconciling flight logs, telemetry counters, failsafe events, hardware behavior, and operator annotations after flights or tests. | This is close to operational safety and integrator know-how, so serious operators may prefer internal scripts unless an external report proves trust and accuracy. | high | Money flows through drone operations, integrator work, hardware, and safety review time, but direct public spend on external telemetry diagnostics was not found. | Useful validation likely needs representative private flight logs; public-only examples can show format handling but not operator-grade usefulness. | Telemetry-integrity report for one uploaded log set that flags packet loss, failsafe transitions, and suspicious telemetry gaps. | watchlisted |

## Opportunity Reviews
### LangGraph Checkpoint Persistence And Cost Diagnostics
- M2 repeated pain: remains strong across checkpoint bloat, replay drift, crash recovery, and duplicated execution.
- The old `sell-before-build` decision was too permissive because it treated public hiring and LangChain platform spend as if they proved demand for an independent checkpoint audit.
- New decision: watchlisted until a buyer asks for or pays for a manual checkpoint review.

### Tailscale Split-Tunnel Routing Exception Diagnostics
- M2 repeated pain: remains visible across exit nodes, split DNS, app exclusions, and routing workarounds.
- The direct money path is still missing: paid Tailscale plans prove network budget, not willingness to buy external routing diagnostics.
- New decision: watchlisted until public paid admin work, procurement, or a reachable buyer confirms the review.

### ArduPilot Telemetry Integrity And Failsafe Diagnostics
- M2 repeated pain: remains visible around telemetry counters and missing logs.
- M4 workaround evidence: remains visible around forum-based manual diagnosis.
- The first transaction is weak because useful validation likely needs private flight logs and operator trust.
- New decision: watchlisted until direct operator spend or paid log-review demand appears.

## Build Readiness
| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |
|---|---|---|---|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | Potentially reduce engineering time and infrastructure waste from checkpoint bloat and replay failures, but the paid workflow is not yet proven. | Public LangGraph community channels, hiring pages, and direct outreach to agent teams; no validated buying channel yet. | public-only | medium | report | unclear | A buyer pays for one manual checkpoint audit, or three reachable teams confirm this is a recurring paid workflow rather than adjacent platform spend. | watchlisted |
| Tailscale Split-Tunnel Routing Exception Diagnostics | Reduce admin time spent debugging split-tunnel, exit-node, and DNS routing failures before rollout. | Admin-facing report or CLI, sold through a public landing page and shared in Tailscale-adjacent communities. | unclear | high | report | unclear | Three admins confirm they would use an external routing review before rollout, or one team asks for a paid routing audit. | watchlisted |
| ArduPilot Telemetry Integrity And Failsafe Diagnostics | Reduce manual time spent proving whether telemetry is trustworthy after flight or during tuning. | Report or CLI shared with operators and integrators, but the acquisition path still depends on direct operator validation. | private-data-required | medium | report | unclear | At least three operators share representative logs for analysis, or one integrator asks for a paid telemetry integrity review. | watchlisted |

## Money Readiness
| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |
|---|---|---|---|---|---|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | 5 | 1 | 3 | 3 | 4 | Agent platform teams, internal automation teams, and consultants shipping production LangGraph workflows. | Public hiring and LangChain paid products show adjacent budget for agent infrastructure, but not direct spend on checkpoint audit reports. | Do not sell a product yet; first ask reachable LangGraph teams for a paid manual checkpoint audit and require one paid request before promotion. | github, docs, job, news | watchlisted |
| Tailscale Split-Tunnel Routing Exception Diagnostics | 4 | 1 | 2 | 3 | 3 | IT admins, security-conscious teams, and power users managing laptops, phones, and exit-node policies. | Tailscale paid plans and admin labor prove adjacent networking budget, but direct external routing-diagnostic spend is not visible. | Ask admins for a paid manual routing review only after finding direct evidence that teams buy this kind of pre-rollout diagnostic. | github, docs, pricing, product | watchlisted |
| ArduPilot Telemetry Integrity And Failsafe Diagnostics | 4 | 1 | 2 | 2 | 2 | UAV operators, robotics labs, integrators, and flight-test engineers using ArduPilot. | Public forum work shows manual diagnosis effort, and a 2026 ArduPilot log-diagnosis project suggests interest in automated review, but no direct public spend is visible. | Ask for representative logs and willingness to pay only after finding direct operator demand or manual log-analysis spend. | github, forum | watchlisted |

## Recommended Next Test
Search for public paid manual workflows in freelance marketplaces, agency service pages, procurement, job posts, and app marketplaces. Promote none of the current three until at least one direct paid workflow or buyer request is found.

## Rejected Or Deferred Signals
- Rejected LangGraph `sell-before-build`: budget adjacency and repeated technical pain are insufficient under schema version 2.
- Deferred Tailscale routing diagnostics: the diagnostic could be useful, but buyer and spend evidence are not direct enough.
- Deferred ArduPilot telemetry diagnostics: technical pain is visible, but private-log access blocks fast commercial validation.

## Evidence Gaps
- No direct checkpoint-audit buyer or paid request was found for LangGraph.
- No external routing-diagnostic spend was found for Tailscale.
- No paid third-party telemetry-integrity review evidence was found for ArduPilot.
- No first-transaction path currently reaches `time_to_transaction_score >= 3`.

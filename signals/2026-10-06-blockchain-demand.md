# Blockchain Demand Signals - 2026-10-06

Date: 2026-10-06
Family: `blockchain-demand`
Signal type: `paid-demand`
Source class: `pricing`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
Notes: This note groups the Blockscout paid deployment pages and issue feed that still show the boundary work around explorer rollout.

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Blockscout issues page | https://github.com/blockscout/blockscout/issues | 2026-10-04 crawl | integration-gap | github | M2 repeated pain | Current issue feed shows indexing gaps, websocket drops, and import/test requests that still need manual reconciliation. |
| Autoscout | https://autoscout.blockscout.com/ | 2026-08-06 crawl | paid-demand | product | M1 paid demand | Paid explorer hosting with posted plans makes chain deployment spend explicit. |
| Blockscout DevPortal | https://dev.blockscout.com/ | 2026-10-05 crawl | paid-demand | product | M1 paid demand | DevPortal exposes paid API and explorer deployment entry points. |
| Explorer-as-a-Service | https://eaas.blockscout.com/ | 2026-09-10 crawl | paid-demand | product | M1 paid demand | Managed explorer hosting shows direct workflow spend for the same outcome. |
| Going PRO API | https://www.blog.blockscout.com/going-pro-api/ | 2026-06-24 publish | paid-demand | news | M1 paid demand | The PRO API transition makes onchain data access monetized and explicit. |
| July 1 is Pro API day | https://www.blog.blockscout.com/news-july-1-is-pro-api-day/ | 2026-07-01 publish | paid-demand | news | M1 paid demand | Public announcement confirms the universal PRO API rollout and customer-facing paid workflow. |
| Deploy Blockscout | https://deploy.blockscout.com/ | 2026-08-06 crawl | paid-demand | product | M1 paid demand | One-click deployment keeps explorer setup in a paid, productized workflow. |

## Notes
- M1 paid demand: Blockscout sells hosted explorers, API access, and managed deployment.
- M2 repeated pain: the issue feed still shows the boundary work between explorer deployment, indexing, and verification.
- M3 competitor proof: Blockscout customer stories and PRO API productization show the workflow is already monetized.
- M4 workaround evidence: teams still rely on framework plugins and custom rollout wiring at the boundary.

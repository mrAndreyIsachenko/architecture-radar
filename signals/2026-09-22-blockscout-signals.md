# Blockscout Demand Signals 2026-09-22

- Family: `blockchain-demand`
- Source date range: `2026-06-24` to `2026-09-22`
- Signal type: `paid-demand`
- Source class: `pricing`
- Signal types: `paid-demand`, `competitor-proof`, `integration-gap`, `workaround-economy`
- Source classes: `product`, `pricing`, `docs`, `news`, `github`
- Evidence labels: `M1 paid demand`, `M3 competitor proof`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M3 competitor proof`, `M4 workaround evidence`
- Notes: Blockscout still monetizes explorer deployment and API access, while the frontend, indexer, and tx-interpretation flow keep exposing manual boundary work that can justify a paid review.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://deploy.blockscout.com/ | 2026-09-22 crawl | paid-demand | product | M1 paid demand | Autoscout shows one-click explorer deployment and a paid deployment workflow. |
| https://eaas.blockscout.com/ | 2026-09-22 crawl | paid-demand | product | M1 paid demand | EaaS still sells hosted explorer deployment and managed hosting. |
| https://dev.blockscout.com/ | 2026-09-22 crawl | paid-demand | product | M1 paid demand | DevPortal still exposes paid API access and pricing for multichain data. |
| https://www.blog.blockscout.com/going-pro-api/ | 2026-03-13 | paid-demand | news | M1 paid demand | The PRO API transition makes paid onchain-data access explicit. |
| https://github.com/blockscout/frontend/issues/3471 | 2026-05-20 | integration-gap | github | M4 workaround evidence | The tx-interpretation migration shows boundary work between blockscout and Noves. |
| https://github.com/blockscout/frontend/blob/main/docs/ENVS.md | 2026-09-22 crawl | workaround-economy | docs | M4 workaround evidence | The env docs expose provider switches for transaction interpretation and live config. |
| https://github.com/blockscout/blockscout/blob/master/apps/indexer/README.md | 2026-09-22 crawl | workaround-economy | docs | M4 workaround evidence | Indexer docs show the manual setup and tuning burden around real-time indexing. |
| https://mail.blockscout.com/p/news-july-1-is-pro-api-day | 2026-07-01 | competitor-proof | news | M3 competitor proof | The mail announcement says the universal PRO API replaced per-instance APIs. |

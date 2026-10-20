# 2026-10-20 blockchain-demand

- Source date range: 2026-03-13 to 2026-10-20
- Family: `blockchain-demand`
- Signal type: `paid-demand`
- Source class: `news`
- Evidence label: `M1 paid demand`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Signal types: `paid-demand`, `integration-gap`, `operational-risk`, `workaround-economy`
- Source classes: `news`, `github`, `docs`
- Evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Blockscout still exposes an explicit paid explorer/API workflow while the current issue and docs surface show manual verification and indexing glue at the boundary.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.blog.blockscout.com/going-pro-api/ | 2026-03-13 publish | paid-demand | news | M1 paid demand | The PRO API announcement exposes public pricing and a clear paid workflow. |
| https://www.blog.blockscout.com/news-api-discovery/ | 2026-10-09 publish | paid-demand | news | M1 paid demand | The news post says thousands of developers are discovering the Pro API. |
| https://www.blog.blockscout.com/switch-to-the-blockscout-pro-api/ | 2026-06-24 publish | paid-demand | news | M1 paid demand | The migration post makes the paid API switchover and multichain endpoint explicit. |
| https://github.com/blockscout/blockscout/issues | 2026-10-20 crawl | operational-risk | github | M2 repeated pain | The issue feed still shows indexing gaps, websocket drops, and rollout failures. |
| https://github.com/blockscout/frontend/issues/3471 | 2026-05-20 issue | integration-gap | github | M4 workaround evidence | The tx-interpretation migration issue shows boundary work still being wired manually. |
| https://github.com/blockscout/docs/blob/main/docs.json | 2026-10-08 crawl | workaround-economy | docs | M4 workaround evidence | The docs tree exposes verification, RPC, and deployment guidance because the workflow remains fragmented. |

# 2026-11-03 blockchain-demand

- Source date range: 2026-03-13 to 2026-11-03
- Family: `blockchain-demand`
- Signal type: `paid-demand`
- Source class: `news`
- Evidence labels: `M1 paid demand`, `M2 repeated pain`, `M3 competitor proof`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M3 competitor proof`, `M4 workaround evidence`
- Notes: Blockscout continues to show explicit paid explorer/API workflows, current deployment packaging, and current issue feed pain around indexing and transaction interpretation. This remains the only family with a clear sell-before-build path.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.blog.blockscout.com/going-pro-api/ | 2026-03-13 | paid-demand | news | M1 paid demand | Blockscout introduced the PRO API with visible pricing and a paid migration story. |
| https://www.blog.blockscout.com/switch-to-the-blockscout-pro-api/ | 2026-06-24 | paid-demand | news | M1 paid demand | The migration guide makes the paid API switchover and multichain endpoint explicit. |
| https://www.blog.blockscout.com/news-api-discovery/ | 2026-10-09 | competitor-proof | news | M3 competitor proof | The post says builders are discovering and using the PRO API, with current signup growth. |
| https://www.blog.blockscout.com/like-magic-explorer-deployment-with-autoscout-wizard/ | 2026-09-23 | paid-demand | news | M1 paid demand | Autoscout pricing and wizard flow show a currently sold deployment workflow. |
| https://eaas.blockscout.com/ | 2026-11-03 crawl | paid-demand | launch | M1 paid demand | EaaS packages explorer hosting, support, and deployment as a commercial offering. |
| https://github.com/blockscout/frontend/issues/3471 | 2026-05-20 | integration-gap | github | M4 workaround evidence | The tx-interpretation migration still requires manual cross-tool wiring. |
| https://github.com/blockscout/blockscout/issues/14869 | 2026-09-25 | operational-risk | github | M2 repeated pain | A mainnet explorer is missing blocks even though indexing status says 100%. |
| https://github.com/blockscout/blockscout/issues/14748 | 2026-08-26 | operational-risk | github | M2 repeated pain | WebSocket block subscriptions drop during high-throughput L2 traffic surges. |

# blockchain-demand signal note, 2026-10-27

- Source date range: 2026-06-24 to 2026-10-27 crawl.
- Family: `blockchain-demand`
Signal type: `paid-demand`
Source class: `news`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
Notes: Blockscout still exposes paid explorer and multichain API spend while the live issue feed shows manual verification and indexing boundary work. This remains the only sell-before-build path.
- Topic family: `blockchain-demand`

## Sources

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Blockscout issue feed | https://github.com/blockscout/blockscout/issues | 2026-10-27 crawl | operational-risk | github | `M2 repeated pain` | Live feed still shows indexing, websocket, and contract-processing failures. |
| Blockscout issue 14869 | https://github.com/blockscout/blockscout/issues/14869 | Opened Sep 2026 | operational-risk | github | `M2 repeated pain` | Explorer missing thousands of blocks while indexing-status reports 100 percent. |
| Blockscout issue 14798 | https://github.com/blockscout/blockscout/issues/14798 | Opened Sep 2026 | operational-risk | github | `M2 repeated pain` | `/api/v2/smart-contracts` times out when sorted. |
| Blockscout issue 10488 | https://github.com/blockscout/blockscout/issues/10488 | Opened Jul 2024 | integration-gap | github | `M4 workaround evidence` | Users still need docs for automated smart-contract-verification over websocket notifications. |
| Blockscout Going PRO | https://www.blog.blockscout.com/going-pro-api/ | 2026-03-13 | paid-demand | news | `M1 paid demand` | PRO API page makes multichain paid access explicit, with public pricing tiers. |
| Blockscout Supporting Developer Access | https://www.blog.blockscout.com/supporting-developer-access/ | 2026-05-07 | paid-demand | news | `M1 paid demand` | Post frames paid developer access as a response to tighter upstream free tiers. |
| Blockscout Autoscout wizard | https://www.blog.blockscout.com/like-magic-explorer-deployment-with-autoscout-wizard/ | 2026-09-27 | paid-demand | news | `M1 paid demand` | Explorer deployment is sold as a paid, rapid setup path with published hourly pricing. |
| Blockscout docs README | https://github.com/blockscout/blockscout/blob/master/apps/explorer/README.md | 2026-10-27 crawl | workaround-economy | docs | `M4 workaround evidence` | Docs lay out the ETL, verification, and event-handling workflow teams still wire together. |

# 2026-09-29 Blockchain Demand Signals

- Family: `blockchain-demand`
- Source date range: 2026-09-29 crawl, with current Blockscout docs, pricing, launch coverage, and issue feed.
- Signal type: `paid-demand`
- Source class: `news`
- Signal types: `paid-demand`, `integration-gap`, `workaround-economy`, `operational-risk`
- Source classes: `news`, `product`, `github`, `docs`
- Market evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Blockscout still exposes a paid explorer/API ecosystem, and the manual boundary-work around verification and multichain indexing remains visible. The paid workflow is real; the missing piece is still a fresh buyer-confirmed manual review.

## Sources

- `https://www.blog.blockscout.com/going-pro-api/` | source class: `news` | signal type: `paid-demand` | evidence label: `M1 paid demand` | note: Blockscout explicitly markets the PRO API and compares it to current API needs.
- `https://dev.blockscout.com/` | source class: `product` | signal type: `paid-demand` | evidence label: `M1 paid demand` | note: DevPortal shows paid developer access and a monetized API entry point.
- `https://www.blog.blockscout.com/switch-to-the-blockscout-pro-api/` | source class: `news` | signal type: `paid-demand` | evidence label: `M1 paid demand` | note: The API migration post shows the universal PRO API as the current paid path.
- `https://github.com/blockscout/frontend/issues/3387` | source class: `github` | signal type: `integration-gap` | evidence label: `M4 workaround evidence` | note: The llms.txt rework discussion shows the API/docs path still requires boundary decisions and integration cleanup.
- `https://github.com/blockscout/frontend/blob/main/docs/ENVS.md` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: Environment variables and verification wiring remain manually configurable across deployment surfaces.
- `https://github.com/blockscout/blockscout/issues` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: The open issue feed shows active indexing, verification, and API friction still landing in 2026.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.blog.blockscout.com/going-pro-api/ | 2026-03-13 | paid-demand | news | M1 paid demand | Blockscout explicitly markets the PRO API and compares it to current API needs. |
| https://dev.blockscout.com/ | 2026-09-29 crawl | paid-demand | product | M1 paid demand | DevPortal shows paid developer access and a monetized API entry point. |
| https://www.blog.blockscout.com/switch-to-the-blockscout-pro-api/ | 2026-09-29 crawl | paid-demand | news | M1 paid demand | The API migration post shows the universal PRO API as the current paid path. |
| https://github.com/blockscout/frontend/issues/3387 | 2026-09-29 crawl | integration-gap | github | M4 workaround evidence | The llms.txt rework discussion shows the API/docs path still requires boundary decisions and integration cleanup. |
| https://github.com/blockscout/frontend/blob/main/docs/ENVS.md | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | Environment variables and verification wiring remain manually configurable across deployment surfaces. |
| https://github.com/blockscout/blockscout/issues | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | The open issue feed shows active indexing, verification, and API friction still landing in 2026. |

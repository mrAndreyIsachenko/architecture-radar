# 2026-10-13 blockchain-demand

- Source date range: 2026-05-05 to 2026-10-13
- Family: `blockchain-demand`
Signal type: `paid-demand`
Source class: `news`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
Notes: Blockscout publishes explicit API pricing and managed explorer paths, and the current issue feed still shows verification and indexing boundary work. This is the only family that still clears the sell-before-build threshold.
- Topic family: `blockchain-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.blog.blockscout.com/going-pro-api/ | 2026-03-13 | paid-demand | news | M1 paid demand | Blockscout publishes the PRO API pricing and migration story as an explicit monetized workflow. |
| https://www.blog.blockscout.com/switch-to-the-blockscout-pro-api/ | 2026-06-24 | paid-demand | news | M1 paid demand | The migration post makes the paid API switchover and multi-chain endpoint explicit. |
| https://github.com/blockscout/frontend/issues/3471 | 2026-05-20 | integration-gap | github | M4 workaround evidence | The tx-interpretation migration issue shows cross-tool boundary work still being wired manually. |
| https://github.com/blockscout/blockscout/issues | 2026-10-13 crawl | operational-risk | github | M2 repeated pain | The live issue feed still includes indexing and websocket reliability failures on current chains. |
| https://github.com/blockscout/docs/blob/main/docs.json | 2026-10-08 crawl | workaround-economy | docs | M4 workaround evidence | The docs tree exposes verification, RPC, and deployment guidance because the workflow remains fragmented. |
- Topic family: `blockchain-demand`

## Sources
- `https://www.blog.blockscout.com/going-pro-api/`
  - Signal: `paid-demand`
  - Class: `news`
  - Label: `M1 paid demand`
  - Note: Blockscout publishes the PRO API pricing and migration story as an explicit monetized workflow.
- `https://www.blog.blockscout.com/switch-to-the-blockscout-pro-api/`
  - Signal: `paid-demand`
  - Class: `news`
  - Label: `M1 paid demand`
  - Note: The migration post makes the paid API switchover and multi-chain endpoint explicit.
- `https://github.com/blockscout/frontend/issues/3471`
  - Signal: `integration-gap`
  - Class: `github`
  - Label: `M4 workaround evidence`
  - Note: The tx-interpretation migration issue shows cross-tool boundary work still being wired manually.
- `https://github.com/blockscout/blockscout/issues`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: The live issue feed still includes indexing and websocket reliability failures on current chains.
- `https://github.com/blockscout/docs/blob/main/docs.json`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: The docs tree exposes verification, RPC, and deployment guidance because the workflow remains fragmented.

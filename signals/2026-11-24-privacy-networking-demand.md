# 2026-11-24 privacy-networking-demand

- Source date range: 2026-04-08 to 2026-11-24
- Family: `privacy-networking-demand`
- Signal type: `paid-demand`
- Source class: `pricing`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Topic family: `privacy-networking-demand`

Notes: Tailscale remains a paid networking stack, but the public issue feed still shows recurring DNS and split-tunnel edge cases. The external diagnostic wedge is still not buyer-confirmed.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing | 2026-11-24 crawl | paid-demand | pricing | M1 paid demand | The pricing page shows a live self-serve networking budget attached to the core product. |
| https://tailscale.com/blog/pricing-v4 | 2026-04-08 | paid-demand | news | M1 paid demand | The pricing update makes the business/premium packaging shift explicit. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 | incumbent-friction | github | M2 repeated pain | MagicDNS and SplitDNS break when Tailscale is used alongside another VPN. |
| https://github.com/tailscale/tailscale/issues/21997 | 2026-10-27 | incumbent-friction | github | M2 repeated pain | Android DNS resolution still breaks for local mDNS with MagicDNS enabled. |
| https://github.com/tailscale/tailscale/issues | 2026-11-24 crawl | operational-risk | github | M2 repeated pain | The live issue feed still includes DNS, routing, and tunnel stability complaints. |

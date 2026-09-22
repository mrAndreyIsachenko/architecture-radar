# Privacy Networking Demand Signals 2026-09-22

- Family: `privacy-networking-demand`
- Source date range: `2026-03-27` to `2026-09-22`
- Signal type: `paid-demand`
- Source class: `pricing`
- Signal types: `paid-demand`, `incumbent-friction`, `workaround-economy`
- Source classes: `pricing`, `docs`, `github`
- Evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale shows visible paid plans and recurring routing pain, but the public evidence still points to internal admin troubleshooting rather than an outside diagnostic market.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing | 2026-09-22 crawl | paid-demand | pricing | M1 paid demand | Seat-based plans and enterprise bundling make the underlying networking budget explicit. |
| https://tailscale.com/kb/1054/dns/?q=split+dns | 2025-12-22 validated | workaround-economy | docs | M4 workaround evidence | The DNS docs explain split DNS, override settings, and per-nameserver behavior. |
| https://github.com/tailscale/tailscale/issues/19336 | 2026-04-11 | incumbent-friction | github | M2 repeated pain | Split-DNS health warnings can be false positives after client upgrades. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 | incumbent-friction | github | M2 repeated pain | MagicDNS and split DNS break when Tailscale is used alongside another VPN. |

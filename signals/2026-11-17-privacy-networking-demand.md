# 2026-11-17 privacy-networking-demand

- Source date range: 2025-02-04 to 2026-11-17
- Family: `privacy-networking-demand`
- Signal type: `paid-demand`
- Source class: `pricing`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale has explicit paid plans and recurring routing/DNS edge cases, but the external diagnostics wedge is still not clearly budgeted.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing | 2026-11-17 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing and plan tiers prove direct spend on the base networking stack. |
| https://tailscale.com/features | 2026-11-16 crawl | incumbent-friction | product | M2 repeated pain | The feature page shows split tunneling, routing, ACLs, and device posture as recurring admin surfaces. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 | incumbent-friction | github | M2 repeated pain | MagicDNS and SplitDNS break when Tailscale is used alongside another VPN app. |
| https://github.com/tailscale/tailscale/issues/19541 | 2026-07-30 crawl | incumbent-friction | github | M2 repeated pain | The DNS override / Mullvad interaction still produces resolver breakage and documented workarounds. |
| https://tailscale.com/docs/reference/faq/other-vpns | 2026-11-17 crawl | workaround-economy | docs | M4 workaround evidence | The docs explain how to make Tailscale coexist with other VPNs and split-tunnel DNS. |

## Sources
- `https://tailscale.com/pricing`
- `https://tailscale.com/features`
- `https://github.com/tailscale/tailscale/issues/20383`
- `https://github.com/tailscale/tailscale/issues/19541`
- `https://tailscale.com/docs/reference/faq/other-vpns`

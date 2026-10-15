# 2026-09-29 Privacy Networking Demand Signals

- Family: `privacy-networking-demand`
- Source date range: 2026-09-29 crawl, with current pricing/docs and recent issue reports.
- Signal type: `incumbent-friction`
- Source class: `github`
- Signal types: `paid-demand`, `workaround-economy`, `incumbent-friction`
- Source classes: `pricing`, `docs`, `github`
- Market evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale is clearly monetized, but the public evidence still reads as operational friction around split DNS, multiple VPNs, and route handling rather than a proven external diagnostics spend.

## Sources

- `https://tailscale.com/pricing` | source class: `pricing` | signal type: `paid-demand` | evidence label: `M1 paid demand` | note: Seat-based pricing and enterprise tiers show direct spend on the networking platform.
- `https://tailscale.com/docs/reference/dns-in-tailscale?_rsc=173fs&tab=windows` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: The DNS docs describe split DNS behavior and the manual configuration users must manage.
- `https://tailscale.com/docs/reference/faq/other-vpns` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: The FAQ explains userspace networking, split tunnel DNS, and the limits when Tailscale coexists with other VPNs.
- `https://github.com/tailscale/tailscale/issues/20383` | source class: `github` | signal type: `incumbent-friction` | evidence label: `M2 repeated pain` | note: MagicDNS and SplitDNS break when another VPN is also in the path.
- `https://github.com/tailscale/tailscale/issues/19336` | source class: `github` | signal type: `incumbent-friction` | evidence label: `M2 repeated pain` | note: Split-DNS health warnings can be false positives after a client upgrade.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing | 2026-09-29 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing and enterprise tiers show direct spend on the networking platform. |
| https://tailscale.com/docs/reference/dns-in-tailscale?_rsc=173fs&tab=windows | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | The DNS docs describe split DNS behavior and the manual configuration users must manage. |
| https://tailscale.com/docs/reference/faq/other-vpns | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | The FAQ explains userspace networking, split tunnel DNS, and the limits when Tailscale coexists with other VPNs. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-09-29 crawl | incumbent-friction | github | M2 repeated pain | MagicDNS and SplitDNS break when another VPN is also in the path. |
| https://github.com/tailscale/tailscale/issues/19336 | 2026-09-29 crawl | incumbent-friction | github | M2 repeated pain | Split-DNS health warnings can be false positives after a client upgrade. |

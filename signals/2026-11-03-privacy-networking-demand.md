# 2026-11-03 privacy-networking-demand

- Source date range: 2026-10-13 to 2026-11-03
- Family: `privacy-networking-demand`
- Signal type: `incumbent-friction`
- Source class: `pricing`
- Evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale clearly has paid usage and recurring routing/DNS issues, but the current evidence still looks like admin pain rather than a buyer-confirmed external diagnostic service.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing | 2026-11-03 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing shows money already flows through the networking stack. |
| https://tailscale.com/docs/reference/dns-in-tailscale | 2026-10-22 last validated | workaround-economy | docs | M4 workaround evidence | The docs explain split DNS, MagicDNS, and manual DNS setup. |
| https://tailscale.com/docs/features/exit-nodes | 2026-10-03 crawl | workaround-economy | docs | M4 workaround evidence | Exit-node routing is a documented policy surface that admins still manage explicitly. |
| https://github.com/tailscale/tailscale/issues/21996 | 2026-10-27 | incumbent-friction | github | M2 repeated pain | A macOS route-listener failure leaves DNS pointed at Tailscale until restart. |
| https://github.com/tailscale/tailscale/issues/21330 | 2026-10-03 | incumbent-friction | github | M2 repeated pain | Chrome/Edge stall when Tailscale DNS is on and built-in DNS gets empty nameservers. |

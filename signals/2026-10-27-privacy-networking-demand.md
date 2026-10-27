# privacy-networking-demand signal note, 2026-10-27

- Source date range: 2026-03-27 to 2026-10-27 crawl.
- Family: `privacy-networking-demand`
Signal type: `paid-demand`
Source class: `pricing`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`
Notes: Tailscale is already monetized, but the live routing and DNS issue stream still points to painful boundary work rather than a proven external diagnostics market.
- Topic family: `privacy-networking-demand`

## Sources

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Tailscale pricing | https://tailscale.com/pricing | 2026-10-27 crawl | paid-demand | pricing | `M1 paid demand` | Seat-based pricing, enterprise packaging, and support add-ons show direct spend on the base networking stack. |
| Tailscale issue 20383 | https://github.com/tailscale/tailscale/issues/20383 | Opened Jul 2026 | incumbent-friction | github | `M2 repeated pain` | MagicDNS and SplitDNS break when Tailscale is used alongside another VPN. |
| Tailscale issue 19336 | https://github.com/tailscale/tailscale/issues/19336 | Opened Mar 2026 | incumbent-friction | github | `M2 repeated pain` | Split-DNS false positive regression appears after a client upgrade. |
| Tailscale issue 21154 | https://github.com/tailscale/tailscale/issues/21154 | Opened Sep 2026 | operational-risk | github | `M2 repeated pain` | Hostname rename can trigger Funnel DNS failures and authoritative NXDOMAIN behavior. |
| Tailscale changelog | https://tailscale.com/changelog | 2026-10-27 crawl | incumbent-friction | news | `M2 repeated pain` | Changelog records a DNS regression fix, confirming the routing surface still needs continual repair. |

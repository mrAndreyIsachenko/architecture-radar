# 2026-10-20 privacy-networking-demand

- Source date range: 2026-01-05 to 2026-10-20
- Family: `privacy-networking-demand`
- Signal type: `paid-demand`
- Source class: `pricing`
- Evidence label: `M1 paid demand`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Signal types: `paid-demand`, `workaround-economy`, `incumbent-friction`, `integration-gap`
- Source classes: `pricing`, `docs`, `github`
- Evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale clearly has paying customers and admin-facing controls, but the external diagnostic wedge is still not proven as something buyers buy separately.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing?plan=business | 2026-09-20 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing and enterprise packaging prove direct spend on the networking stack. |
| https://tailscale.com/docs/features/client/android-app-split-tunneling | 2026-01-05 validated | workaround-economy | docs | M4 workaround evidence | App-based split tunneling requires explicit admin and user rules. |
| https://tailscale.com/docs/reference/troubleshooting/mobile/force-or-bypass-apps | 2026-10-20 crawl | workaround-economy | docs | M4 workaround evidence | The troubleshooting guide exists because admins need a way to force or bypass apps manually. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 issue | incumbent-friction | github | M2 repeated pain | MagicDNS and SplitDNS break when Tailscale is used alongside another VPN app. |
| https://github.com/tailscale/tailscale/issues/19336 | 2026-04-11 issue | incumbent-friction | github | M2 repeated pain | Split-DNS health warnings can regress after upgrades even when the setup is valid. |
| https://github.com/tailscale/tailscale/issues/19229 | 2026-04-03 issue | incumbent-friction | github | M2 repeated pain | App split tunneling plus DNS produces a reproducible Android failure path. |
| https://github.com/tailscale/tailscale/issues/20467 | 2026-07-15 issue | integration-gap | github | M2 repeated pain | App Connector DNS resolution can fail at the boundary between connector, DNS, and client routing. |

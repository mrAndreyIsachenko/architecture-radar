# Privacy Networking Demand Signals - 2026-10-06

Date: 2026-10-06
Family: `privacy-networking-demand`
Signal type: `incumbent-friction`
Source class: `github`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
Notes: This note groups the current Tailscale pricing, DNS docs, and routing issue feed that expose the same split-tunnel pain.

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Tailscale pricing | https://tailscale.com/pricing | 2026-10-06 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing and enterprise packaging make the underlying networking budget explicit. |
| DNS in Tailscale | https://tailscale.com/kb/1054/dns/?q=split+dns | 2026-09-30 crawl | workaround-economy | docs | M4 workaround evidence | Docs expose the split-DNS and override settings admins still have to manage manually. |
| Issue 19336 | https://github.com/tailscale/tailscale/issues/19336 | 2026-04-11 | incumbent-friction | github | M2 repeated pain | False-positive DNS health warnings keep appearing in split-DNS mode. |
| Issue 20383 | https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 | incumbent-friction | github | M2 repeated pain | MagicDNS and split DNS break when Tailscale runs alongside another VPN. |
| Issue 21154 | https://github.com/tailscale/tailscale/issues/21154 | 2026-09-08 | incumbent-friction | github | M2 repeated pain | macOS wake-from-sleep can stall DNS when upstream dials route into the tunnel. |
| Issue 19951 | https://github.com/tailscale/tailscale/issues/19951 | 2026-06-03 | incumbent-friction | github | M2 repeated pain | Windows split-DNS suffixes can fail through the usual resolver path. |
| Issue 19229 | https://github.com/tailscale/tailscale/issues/19229 | 2026-04-07 | incumbent-friction | github | M2 repeated pain | The new app split-tunneling mode still fails when Tailscale DNS is enabled on Android. |

## Notes
- M1 paid demand: Tailscale pricing proves budgeted spend already exists in the ecosystem.
- M2 repeated pain: recent issues keep surfacing split-DNS and mixed-VPN friction.
- M4 workaround evidence: the docs still require manual selection of DNS and routing behavior.
- The external diagnostic wedge remains unproven because the buyer path is still fuzzy.

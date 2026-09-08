# Privacy Networking Signals 2026-09-08

- Family: `privacy-networking-demand`
- Source date range: 2025-04-03 to 2026-01-12
- Signal type: `incumbent-friction`
- Source class: `docs`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale has real routing friction and documented workarounds, but the external diagnostic wedge is still adjacent.

## Sources
- `M2 repeated pain` | `incumbent-friction` | `github` | https://github.com/tailscale/tailscale/issues/15521 | Users ask for domain exclusions on exit nodes and describe the current workaround as suboptimal.
- `M4 workaround evidence` | `manual-comparison` | `product` | https://tailscale.com/blog/app-connectors-explained | App connectors route specific domains through designated infrastructure.
- `M4 workaround evidence` | `manual-comparison` | `docs` | https://tailscale.com/docs/features/client/android-app-split-tunneling | Android split-tunneling docs show the manual routing surface.
- `M4 workaround evidence` | `manual-comparison` | `docs` | https://tailscale.com/docs/features/exit-nodes | Exit-node docs show the full-tunnel boundary and manual choices.

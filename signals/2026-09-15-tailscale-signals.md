# Tailscale Demand Signals 2026-09-15

- Family: `privacy-networking-demand`
- Source date range: 2026-01-10 to 2026-09-15
- Signal type: `incumbent-friction`
- Source class: `github`
- Evidence labels: `M2 repeated pain`, `M1 paid demand`, `I interpretation`
- Labels: `M2 repeated pain`, `M1 paid demand`, `I interpretation`
- Notes: Tailscale has explicit paid plans, but the public evidence for a standalone routing-diagnostics wedge is still adjacent rather than direct.

## Sources
- `M2 repeated pain` | `incumbent-friction` | `github` | https://github.com/tailscale/tailscale/issues/18828 | Windows NRPT state can break DNS resolution after client changes.
- `M2 repeated pain` | `incumbent-friction` | `github` | https://github.com/tailscale/tailscale/issues/20083 | IPv6 fragments can be silently dropped by the packet filter, creating hard-to-debug routing behavior.
- `M2 repeated pain` | `incumbent-friction` | `github` | https://github.com/tailscale/tailscale/issues/20325 | macOS package installs can fail before the CLI starts, showing rollout friction.
- `M2 repeated pain` | `incumbent-friction` | `github` | https://github.com/tailscale/tailscale/issues/19290 | Funnel reports success while public requests still stall on TLS handshake.
- `M1 paid demand` | `paid-demand` | `pricing` | https://tailscale.com/pricing | Tailscale pricing proves budget attachment for the underlying networking workflow, though not for diagnostics specifically.

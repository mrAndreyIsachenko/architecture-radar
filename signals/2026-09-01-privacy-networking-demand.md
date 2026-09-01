# Privacy Networking Demand Signals 2026-09-01

- Family: `privacy-networking-demand`
- Source date range: 2026-01-06 to 2026-09-01
- Signal type: incumbent-friction
- Source class: docs
- Evidence labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Tailscale has real paid usage and recurring DNS or routing friction, but the external review wedge remains adjacent to the core product.

## Sources
- `M1 paid demand` | `paid-demand` | `pricing` | https://tailscale.com/pricing | Tailscale pricing shows a real budget surface for private networking.
- `M4 workaround evidence` | `manual-comparison` | `docs` | https://tailscale.com/docs/reference/dns-in-tailscale | DNS settings and split-DNS configuration remain a manual admin surface.
- `M2 repeated pain` | `incumbent-friction` | `github` | https://github.com/tailscale/tailscale/issues/18340 | Split DNS latency complaint shows recurring operational friction.
- `M4 workaround evidence` | `manual-comparison` | `docs` | https://tailscale.com/docs/reference/faq/other-vpns | Exit-node and other-VPN coexistence docs show the workaround boundary.

## Notes
- The ecosystem clearly has spend, but the external routing-diagnostics wedge is still only adjacent to that spend.
- Keep this family watchlisted until a buyer explicitly asks for a paid pre-rollout routing review.

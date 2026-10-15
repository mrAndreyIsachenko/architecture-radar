# 2026-10-13 privacy-networking-demand

- Source date range: 2026-04-08 to 2026-10-13
- Family: `privacy-networking-demand`
Signal type: `paid-demand`
Source class: `pricing`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
Notes: Tailscale's pricing makes the networking budget explicit, but the external routing-diagnostics wedge is still not backed by public evidence of purchase behavior. The family remains watchlisted.
- Topic family: `privacy-networking-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing?plan=business | 2026-10-13 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing and enterprise packaging prove direct spend on the base networking stack. |
| https://tailscale.com/docs/kubernetes-operator/connector | 2026-10-13 crawl | workaround-economy | docs | M4 workaround evidence | The connector docs show operators still reasoning about exit nodes, subnet routing, and cluster bridging manually. |
| https://tailscale.com/docs/features/client/android-app-split-tunneling | 2026-10-13 crawl | workaround-economy | docs | M4 workaround evidence | App-based split tunneling is documented because admins still need explicit per-app routing control. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 | incumbent-friction | github | M2 repeated pain | MagicDNS and SplitDNS break when Tailscale is used alongside another VPN. |
| https://github.com/tailscale/tailscale/issues/19336 | 2026-04-11 | incumbent-friction | github | M2 repeated pain | A split-DNS false positive regression still appears after a recent client upgrade. |
- Topic family: `privacy-networking-demand`

## Sources
- `https://tailscale.com/pricing?plan=business`
  - Signal: `paid-demand`
  - Class: `pricing`
  - Label: `M1 paid demand`
  - Note: Seat-based pricing and enterprise packaging prove direct spend on the base networking stack.
- `https://tailscale.com/docs/kubernetes-operator/connector`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: The connector docs show operators still reasoning about exit nodes, subnet routing, and cluster bridging manually.
- `https://tailscale.com/docs/features/client/android-app-split-tunneling`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: App-based split tunneling is documented because admins still need explicit per-app routing control.
- `https://github.com/tailscale/tailscale/issues/20383`
  - Signal: `incumbent-friction`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: MagicDNS and SplitDNS break when Tailscale is used alongside another VPN.
- `https://github.com/tailscale/tailscale/issues/19336`
  - Signal: `incumbent-friction`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: A split-DNS false positive regression still appears after a recent client upgrade.

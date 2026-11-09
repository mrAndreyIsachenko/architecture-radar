# 2026-11-10 privacy-networking-demand

- Source date range: 2026-01-05 to 2026-11-10
- Family: `privacy-networking-demand`
Signal type: `paid-demand`
Source class: `pricing`
Evidence label: `M1 paid demand`
Labels: `M1 paid demand`, `M2 repeated pain`, `M4 workaround evidence`
Notes: Tailscale clearly has paid spend and recurring routing controls, but the external diagnostic wedge still looks like admin glue rather than a proven standalone purchase.
- Topic family: `privacy-networking-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://tailscale.com/pricing?plan=business | 2026-10-13 crawl | paid-demand | pricing | M1 paid demand | Seat-based pricing and enterprise packaging prove direct spend on the core networking stack. |
| https://tailscale.com/kb/1444/android-app-split-tunneling | 2026-01-05 | workaround-economy | docs | M4 workaround evidence | Tailscale documents app-based split tunneling because admins still need explicit per-app routing control. |
| https://tailscale.com/docs/reference/troubleshooting/mobile/force-or-bypass-apps | 2026-11-10 crawl | workaround-economy | docs | M4 workaround evidence | The troubleshooting guide exists because app-based routing exceptions need explicit admin handling. |
| https://github.com/tailscale/tailscale/issues/20383 | 2026-07-09 | incumbent-friction | github | M2 repeated pain | MagicDNS and SplitDNS break when Tailscale is used alongside another VPN. |
| https://tailscale.com/docs/features/tailscale-system-policies | 2026-11-10 crawl | workaround-economy | docs | M4 workaround evidence | System-policies docs show that route control and client policy remain explicit admin work. |
- Topic family: `privacy-networking-demand`

## Sources
- `https://tailscale.com/pricing?plan=business`
  - Signal: `paid-demand`
  - Class: `pricing`
  - Label: `M1 paid demand`
  - Note: Seat-based pricing and enterprise packaging prove direct spend on the core networking stack.
- `https://tailscale.com/kb/1444/android-app-split-tunneling`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: Tailscale documents app-based split tunneling because admins still need explicit per-app routing control.
- `https://tailscale.com/docs/reference/troubleshooting/mobile/force-or-bypass-apps`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: The troubleshooting guide exists because app-based routing exceptions need explicit admin handling.
- `https://github.com/tailscale/tailscale/issues/20383`
  - Signal: `incumbent-friction`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: MagicDNS and SplitDNS break when Tailscale is used alongside another VPN.
- `https://tailscale.com/docs/features/tailscale-system-policies`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: System-policies docs show that route control and client policy remain explicit admin work.

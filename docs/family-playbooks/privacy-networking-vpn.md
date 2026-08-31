# Privacy Networking VPN Playbook

## Family

`privacy-networking-vpn`

Use this playbook for VPN, private networking, secure tunnel, mesh networking, access-control, censorship-resistance, and network-observability candidates.

## Mechanisms To Search

- Split tunnel and route exception reconciliation.
- DNS leak prevention, captive portal detection, and route leak detection.
- Kill switch enforcement and recovery after reconnect.
- Peer, key, credential, and policy lifecycle management.
- NAT traversal, relay fallback, multi-hop path selection, and degraded transport recovery.
- Capability-scoped access to networks, hosts, services, and admin workflows.
- Privacy-preserving observability that avoids unnecessary content capture.

## Evidence Bar

- Source evidence for how routes, DNS, keys, and policies are applied.
- Tests or operational docs for reconnect, revoke, route leak, DNS leak, and blocked transport behavior.
- Threat model, security notes, or maintainer discussion for sensitive traffic handling.
- Explicit failure modes for misconfiguration, stale credentials, degraded relay paths, and partial policy rollout.

## Selection Bias

Prefer control-plane, policy, recovery, and observability mechanisms over consumer-facing clients. Select a dependency only when it has a narrow integration surface, active maintenance, tests, and clear operational behavior.

## Rejection Triggers

- UI or CLI wrapper around WireGuard/OpenVPN with no policy, recovery, or leak-prevention mechanism.
- Marketing claims without tests, threat model, or implementation paths.
- Traffic-inspection designs that capture more content than necessary.
- Projects that only rank or compare consumer VPN services.

## Validation Evidence

- Route/DNS state before and after connect, reconnect, and disconnect.
- Key revoke and rotation behavior under active sessions.
- Split tunnel exception tests.
- Kill switch behavior under transport failure.
- NAT traversal and relay fallback traces.
- Minimal telemetry showing health without content capture.

## Useful Search Seeds

- `wireguard-ui`, `wireguard control plane`, `tailscale DERP`, `headscale routes`, `netbird policy`, `openziti edge`, `sing-box routing`, `xray-core routing`, `dns leak test`, `network extension vpn`, `nftables killswitch`

# openzro/openzro

- Repository: https://github.com/openzro/openzro
- Review date: 2026-11-27
- Current commit reviewed: `43ee3574da0c423d88d88f115ab28ddd6850b42b`
- Commit date: 2026-10-23T00:57:31-03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `privacy-networking-vpn`, especially route ownership, reconnect recovery, and relay behavior across a clustered control plane. The reusable mechanism is the route-reconciliation loop that survives pod boundaries by forwarding destination-framed traffic and reconciling pod membership through discovery.

## Verified Flow

`management/client/rest/routes.go` exposes CRUD for route resources -> `client/internal/routeselector/routeselector.go` persists the selected route IDs and filters them atomically -> `relay/server/cluster/discovery.go` watches the headless service and reconciles pod IP membership -> `relay/server/cluster/forwarder.go` sends local peers directly or prefixes `PeerID || msg` for remote forwarding -> `management/client/rest/routes_test.go` and `relay/server/cluster/forwarder_test.go` verify CRUD, local dispatch, remote dispatch, and nil-safe selector persistence -> `client/internal/connect_test.go` covers reconnect-related state handling.

- E1 source verified: `management/client/rest/routes.go` implements route CRUD and route-state updates.
- E1 source verified: `client/internal/routeselector/routeselector.go` persists selected and deselected route IDs and filters them atomically.
- E1 source verified: `relay/server/cluster/discovery.go` watches the headless service and reconciles pod membership.
- E1 source verified: `relay/server/cluster/forwarder.go` preserves the destination peer ID across local and remote forwarding hops.
- E2 test verified: `management/client/rest/routes_test.go` verifies route CRUD behavior.
- E2 test verified: `relay/server/cluster/forwarder_test.go` verifies local dispatch, remote dispatch, and forwarding behavior.
- E2 test verified: `client/internal/connect_test.go` exercises reconnect-related state handling and selector persistence.

## Architecture

Principal components:

- REST route management surface for control-plane route resources.
- Persisted route selector for the chosen route set.
- Cluster discovery loop for pod membership reconciliation.
- Forwarder that preserves destination identity across pod-to-pod relay hops.
- Tests that pin CRUD, dispatch, and persistence behavior.

Most interesting mechanism: the relay path does not trust the local pod boundary. It explicitly frames the destination peer into the forwarded message and reconstructs the target on the receiving side, which keeps route ownership intact across cluster turnover.

Baseline comparison: a simpler VPN control plane would assume a route stays local or would forward opaque payloads without destination framing. This repository separates route selection, discovery, and hop routing so the cluster can reconcile changes instead of guessing.

## Reuse Guidance

Reusable:

- Persist route selection separately from the forwarding transport.
- Use explicit discovery reconciliation for pod membership changes.
- Frame the destination identity into forwarded messages so remote peers can dispatch deterministically.

Do not copy:

- Do not copy the product surface or install workflow as the mechanism.
- Do not assume local-only routing semantics remain correct in a clustered deployment.
- Do not treat the tests as proof of live multi-pod churn recovery.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Route CRUD and forwarding behavior are test-covered.
- Discovery and relay concerns are split into separate modules.
- The cluster path keeps destination identity explicit instead of implicit.

Experimental or incomplete for our needs:

- Live multi-pod reconnect churn still needs validation.
- The forwarded envelope and discovery loop are coupled to the cluster topology.
- The review did not validate pod turnover under sustained traffic.

Hidden costs and failure modes:

- Discovery lag can route traffic to stale pod membership.
- A bad destination envelope can misroute traffic across the cluster.
- Route selector drift can leave the forwarded state inconsistent with the management API.

Adoption experiment:

Run a two-pod deployment, force one peer to move or restart, and confirm the route selector and forwarder continue to deliver traffic to the current owner without leaving stale pod membership in the cluster view.

## Candidate Patterns

- `Policy-Guarded Route Reconciliation Loop`
- `cluster-forwarded route reconciliation`
- `destination-framed relay envelope`
- `headless-service peer discovery reconcile loop`

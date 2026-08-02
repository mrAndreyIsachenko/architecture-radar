# Architecture Radar Supplement: 2026-08-02

## Prerequisites And State

- Run date: 2026-08-02 Europe/Moscow.
- Existing daily report present: `reports/2026-08-02.md`.
- Supplement required by CI context: yes.
- Supplement scope change after the existing daily report: `docs/architecture-radar-agent.md`, `interests.md`.
- Required workspace verified: `interests.md`, `radar.json`, `reports/`, `repositories/`, and `patterns/` exist.
- `interests.md` remained the authoritative source for project priorities.
- Temporary clones were placed under `/tmp/architecture-radar-candidates`.
- CI constraint observed: no commits, pushes, remote edits, or pull requests were created by the agent.

## Candidate Counts

Highest stage reached:

- `triaged`: 20
- `source-inspected`: 8
- `deeply-reviewed`: 8

## Selected Repositories

- `DeusData/codebase-memory-mcp` at `d6be58ef9d43c574a2d1b0827ecc1e3c4846f0fe`
- `cocoindex-io/cocoindex` at `5aa593f4c5ca5e982d4c6df8e40d60510b69c2ef`
- `firezone/firezone` at `2b4ffb54ec248ca26cb327af2717f7f8801e3b2f`
- `netbirdio/netbird` at `f2318a8fef230219110c9eeb58ca7f60e247ad98`
- `PX4/PX4-Autopilot` at `43cccdea0e57cf92a58562d2d7a1cba0854395f7`
- `mavlink/qgroundcontrol` at `de77da5f84aa95a8dcafd314eb45072e6810dfe6`
- `fystack/multichain-indexer` at `90f4b3156c36bf048ec513e395f7dadef66f32e1`
- `graphprotocol/graph-node` at `2adda68a79dff3703ab444ac8d846c189d9ce3c0`

## Candidate Ledger

| Repository | URL | Commit | Discovery source | Family | Stage | Categories | Activity signal | Mechanism signal | Relevance signal | Decision | Rejection or deferral reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `DeusData/codebase-memory-mcp` | https://github.com/DeusData/codebase-memory-mcp | `d6be58ef9d43c574a2d1b0827ecc1e3c4846f0fe` | GitHub code/search for codebase intelligence | `ai-llm-systems` | deeply-reviewed | codebase intelligence; incremental indexing | Recent commit 2026-07-31; rich tests and docs | `index_repository`, `search_graph`, `trace_path`, `dump_verify` | Direct fit for codebase intelligence and evidence-aware search | selected | Clear reusable mechanism and strong test surface |
| `cocoindex-io/cocoindex` | https://github.com/cocoindex-io/cocoindex | `5aa593f4c5ca5e982d4c6df8e40d60510b69c2ef` | GitHub ecosystem search for incremental context engines | `ai-llm-systems` | deeply-reviewed | incremental indexing; context construction | Recent commit 2026-07-30; engine/tests/docs | target-state providers, memoization invalidation, live FS reconciliation | Direct fit for delta-oriented context refresh | selected | Strong source-backed delta mechanism |
| `firezone/firezone` | https://github.com/firezone/firezone | `2b4ffb54ec248ca26cb327af2717f7f8801e3b2f` | GitHub search for policy-controlled tunnels | `privacy-networking-vpn` | deeply-reviewed | VPN; access control; secure tunnels | Recent commit 2026-08-01; Rust + Elixir tests | gateway eventloop, portal queue durability, DNS/routing mutation | Direct fit for least-privilege tunnel control | selected | Policy-driven control-plane/data-plane split cleared the bar |
| `netbirdio/netbird` | https://github.com/netbirdio/netbird | `f2318a8fef230219110c9eeb58ca7f60e247ad98` | GitHub search for overlay networking | `privacy-networking-vpn` | deeply-reviewed | mesh networking; observability; access control | Recent commit 2026-08-02; client tests | normalized connectivity status snapshot | Direct fit for network observability and route/DNS state | selected | Status-model mechanism is reusable and well tested |
| `PX4/PX4-Autopilot` | https://github.com/PX4/PX4-Autopilot | `43cccdea0e57cf92a58562d2d7a1cba0854395f7` | GitHub search for autonomy safety stacks | `drones-robotics-autonomy` | deeply-reviewed | autonomy safety; mission planning; failsafe | Recent commit 2026-08-01; mission/failsafe tests | commander ACK matrix, sensor-loss recovery tests | Direct fit for safety-aware autonomy | selected | High-signal command/failsafe path |
| `mavlink/qgroundcontrol` | https://github.com/mavlink/qgroundcontrol | `de77da5f84aa95a8dcafd314eb45072e6810dfe6` | GitHub search for ground-control workflows | `drones-robotics-autonomy` | deeply-reviewed | ground control; telemetry observability; mission workflow | Recent commit 2026-08-01; log tests | cancel-safe log controller, FTP/message fallback | Direct fit for telemetry recovery and operator workflows | selected | Strong operator-side recovery mechanism |
| `fystack/multichain-indexer` | https://github.com/fystack/multichain-indexer | `90f4b3156c36bf048ec513e395f7dadef66f32e1` | GitHub search for blockchain deposit detection | `blockchain-intelligence` | deeply-reviewed | transaction interpretation; incremental indexing; reorg recovery | Recent commit 2026-07-10; worker tests | worker-ring recovery, bloom-filter fanout, persisted checkpoints | Direct fit for transaction interpretation and deposit monitoring | selected | Reorg-safe worker model and restart safety are clear |
| `graphprotocol/graph-node` | https://github.com/graphprotocol/graph-node | `2adda68a79dff3703ab444ac8d846c189d9ce3c0` | GitHub search for blockchain indexing | `blockchain-intelligence` | deeply-reviewed | blockchain indexing; deterministic materialization; queryable logs | Commit 2026-07-20; source/tests/docs | reorg-threshold block stream, bounded cache cleanup, log-store API | Direct fit for finalized/provisional split | selected | Strong reference model for reorg-safe indexing |
| `sourcebot-dev/sourcebot` | https://github.com/sourcebot-dev/sourcebot | `39bf1a02a8753eede6add0095fca12e87fd1700a` | GitHub repo search for code search systems | `ai-llm-systems` | triaged | code search; repo intelligence | Recent commit 2026-07-31 | code search/navigation product surface | Related to codebase intelligence | rejected | Product-heavy; weaker inspectable mechanism than selected codebase repos |
| `harshkedia177/axon` | https://github.com/harshkedia177/axon | `99b6409a97e2ea940b4a77a52af9e9cb6020f363` | GitHub search for code graph / memory systems | `ai-llm-systems` | triaged | code graph; memory | Activity last seen 2026-03-25 | graph/memory indexing surface | Some relevance to codebase intelligence | rejected | Older activity and weaker source/test depth |
| `suatkocar/codegraph` | https://github.com/suatkocar/codegraph | `856739a1a528cfae9f9232566ae5c043ef8cfaf5` | GitHub search for code graph systems | `ai-llm-systems` | triaged | code graph; repository analytics | Activity last seen 2026-03-03 | graph visualization / analysis surface | Some relevance to codebase intelligence | rejected | Older activity and less reusable mechanism signal |
| `tailscale/tailscale` | https://github.com/tailscale/tailscale | `4c4d1c35f83a21c6069ae09de69b246ed1993f3e` | GitHub search for VPN baselines | `privacy-networking-vpn` | triaged | overlay networking; access control | Recent commit 2026-08-01; very active | broad tunnel/control-plane stack | Baseline comparison only | deferred | Broader baseline; Firezone and NetBird had clearer mechanism focus |
| `DefGuard/defguard` | https://github.com/DefGuard/defguard | `334fcf33a27013a7dab88989b2d86cc6babd0b06` | GitHub search for VPN control planes | `privacy-networking-vpn` | triaged | VPN; access control | Recent commit 2026-07-31 | control-plane + access management | Relevant but secondary | deferred | Good alternative, but lower signal than Firezone/NetBird |
| `mullvad/mullvadvpn-app` | https://github.com/mullvad/mullvadvpn-app | `c516040c8eed6148009b193e1266d535af847b9a` | GitHub search for VPN clients | `privacy-networking-vpn` | triaged | VPN client; privacy networking | Recent commit 2026-07-31 | consumer client surface | Weak fit for radar priorities | deferred | Product/client focus rather than reusable control-plane mechanism |
| `ArduPilot/ardupilot` | https://github.com/ArduPilot/ardupilot | `d2dbff2e8f5188a36c5d220b8702837be8dbfc85` | GitHub search for autonomy stacks | `drones-robotics-autonomy` | triaged | autonomy; mission planning; safety | Recent commit 2026-08-01 | embedded flight stack | Relevant baseline | deferred | Strong project, but PX4 had clearer validated safety path this run |
| `mavlink/MAVSDK-Python` | https://github.com/mavlink/MAVSDK-Python | `d35791847152980ec0aae1953de056693421027f` | GitHub search for MAVLink SDKs | `drones-robotics-autonomy` | triaged | SDK; mission control | Commit 2026-07-22 | Python SDK wrapper | Utility layer, not full mechanism | deferred | SDK wrapper rather than a broader reusable autonomy mechanism |
| `alireza787b/mavsdk_drone_show` | https://github.com/alireza787b/mavsdk_drone_show | `b00a0599f172510700808862f260af786412ebed` | GitHub search for drone-show examples | `drones-robotics-autonomy` | triaged | demo; drone choreography | Commit 2026-07-28 | demo mission scripts | Low direct relevance | rejected | Demo-heavy and not production-grade enough for the radar |
| `subsquid/squid-sdk` | https://github.com/subsquid/squid-sdk | `26f7703e127604a40522449eedff3823d6183662` | GitHub search for blockchain indexing SDKs | `blockchain-intelligence` | triaged | blockchain SDK; ETL | Recent commit 2026-07-30 | multi-chain ETL toolkit | Relevant but broad | deferred | Useful baseline, but weaker reorg/materialization focus than selected repos |
| `apibara/dna` | https://github.com/apibara/dna | `491bacd2e9c9e8d0360910a0be80ca336f9de680` | GitHub search for chain data streaming | `blockchain-intelligence` | triaged | chain streaming; reorg handling | Commit 2026-05-18 | ingestion/specs around reorg-safe data | Relevant but older | deferred | Interesting, but older and less direct than selected blockchain pair |
| `EXCCoin/exccdata` | https://github.com/EXCCoin/exccdata | `a9c5b998e55a91631d2d8e100436c3e7fe1bf5a6` | GitHub search for explorer/indexer systems | `blockchain-intelligence` | triaged | explorer; monitoring; data collection | Recent commit 2026-07-31 | block explorer / data collection stack | Related, but not as focused | deferred | Explorer baseline; stronger transaction-interpretation candidates were selected |

## Executive Summary

This supplement extends the radar beyond the AI lineage/agent set from the daily report and covers the families that were still missing or under-covered there:

- Codebase intelligence and incremental context assembly: `DeusData/codebase-memory-mcp` and `cocoindex-io/cocoindex`.
- Privacy networking and tunnel control: `firezone/firezone` and `netbirdio/netbird`.
- Drones and autonomy safety: `PX4/PX4-Autopilot` and `mavlink/qgroundcontrol`.
- Blockchain transaction interpretation and reorg-safe indexing: `fystack/multichain-indexer` and `graphprotocol/graph-node`.

The strongest cross-repo mechanism extracted in this supplement is [Reorg-Safe Materialization Windows](../patterns/reorg-safe-materialization-windows.md), which compares a threshold-based block stream with a worker-ring recovery model.

## Material Changes Since The Previous Run

- The daily report already covered evidence envelopes for agent/runtime and lineage systems.
- This supplement adds the four topic families that were not represented there.
- A new standalone blockchain pattern was extracted because two independent indexers converged on the same provisional/finalized split.

## Detailed Reviews

- [DeusData/codebase-memory-mcp](../repositories/deusdata-codebase-memory-mcp.md)
- [cocoindex-io/cocoindex](../repositories/cocoindex-io-cocoindex.md)
- [firezone/firezone](../repositories/firezone-firezone.md)
- [netbirdio/netbird](../repositories/netbirdio-netbird.md)
- [PX4/PX4-Autopilot](../repositories/PX4-PX4-Autopilot.md)
- [mavlink/qgroundcontrol](../repositories/mavlink-qgroundcontrol.md)
- [fystack/multichain-indexer](../repositories/fystack-multichain-indexer.md)
- [graphprotocol/graph-node](../repositories/graphprotocol-graph-node.md)

## Extracted Or Updated Patterns

- Added [Reorg-Safe Materialization Windows](../patterns/reorg-safe-materialization-windows.md).

## Relevance To Explicit Problems In `interests.md`

- `ai-llm-systems`: codebase intelligence, incremental indexing, and declarative reconciliation.
- `privacy-networking-vpn`: privileged tunnel control, route/DNS mutation, and normalized connectivity state.
- `drones-robotics-autonomy`: command acknowledgment, mission recovery, telemetry teardown, and sensor-loss tests.
- `blockchain-intelligence`: reorg-safe indexing, transaction interpretation, deposit detection, and restart-safe materialization.

## Recommended Next Action

Prototype a small blockchain deposit monitor that persists latest block checkpoints, splits live work from catchup/manual recovery, and injects one simulated reorg to confirm downstream crediting remains idempotent.

## Notable Rejected Or Deferred Candidates

- `tailscale/tailscale` was deferred as a broader VPN baseline; `firezone/firezone` and `netbirdio/netbird` had clearer policy/control-plane mechanics for this run.
- `DefGuard/defguard` and `mullvad/mullvadvpn-app` were deferred as narrower alternatives after the stronger privacy-networking candidates were found.
- `ArduPilot/ardupilot` and `mavlink/MAVSDK-Python` were deferred because PX4 plus QGroundControl already covered both safety and operator workflow.
- `subsquid/squid-sdk`, `apibara/dna`, `EXCCoin/exccdata`, and `graphprotocol/graph-node` were deferred or selected according to the strength of the reorg-safe indexing evidence.

## Unresolved Evidence Gaps

- No local test suite was run.
- The privacy-networking reviews stayed at the control-plane and status-model layers, not full deployment verification.
- The drone reviews did not exercise hardware or simulator runs locally.
- Blockchain indexer adoption still needs a real reorg-injection test and an idempotent downstream sink before production use.

# Blockscout Verification And Indexing Review

## Opportunity Summary
Public Blockscout docs, pricing, and customer stories show a paid ecosystem around hosted explorer deployment, multichain API access, managed hosting, and contract verification. The sell-before-build wedge is a manual review that checks whether one chain or explorer rollout will break on verification, websocket delivery, or indexer configuration before engineering time is committed.

## Evidence
- M1 paid demand: Blockscout publishes paid Autoscout explorer plans starting at $349/mo, a PRO API with public tiers starting at $49/mo, $199/mo, and $999/mo, and EAAS managed hosting.
- M1 paid demand: the PRO API page says one account covers multichain onchain data with higher limits, predictable pricing, and a single billing account.
- M2 repeated pain: issue `#10488` asks for documentation on automated solutions around the verification API, which means users are still assembling the workflow manually.
- M2 repeated pain: the verification docs and websocket docs exist because teams need to wire verification and event handling across multiple entry points.
- M3 competitor proof: Onyx and Kinto deployment stories plus Blockscout's managed-hosting pages show the workflow is already used by real chains.
- M4 workaround evidence: users can verify through Hardhat, Foundry, Remix, Sourcify, or custom API wiring, which implies repeated glue work at the boundary.

## Structural Pattern
Control and review layer for explorer deployment, verification events, and multichain indexing.

## Primitive Growth
Blockscout has added Autoscout hosting, EAAS managed hosting, PRO API access, websocket events, and multichain infrastructure while EVM chains and L2s kept proliferating through 2024-2026.

## Fragmentation
Teams still juggle explorer hosting, chain RPCs, verification methods, websocket/event handling, and per-chain rollout settings.

## Manual Workflow
People read docs, wire Hardhat/Foundry/Sourcify verification, and manually reconcile event delivery or indexer settings across chains.

## Objective Function
Minimize rollout risk and verification failure while maximizing deployment speed and predictable multichain coverage.

## Execution Ladder
- Observe: read docs, pricing, issue threads, and rollout settings.
- Recommend: identify missing hooks, webhook gaps, and indexer pitfalls.
- Choose: rank verification/indexer options against setup cost and rollout risk.
- Execute: deliver a manual review before implementation.

## Economic Pain
Wrong setup delays explorer launches, breaks verification flows, and burns engineer time on chain-by-chain debugging.

## Timing Reason
Recent productization around Autoscout, EAAS, and PRO API, plus continuing multichain growth, made the workflow more valuable in 2025-2026.

## Competitors
- Autoscout
- PRO API
- Blockscout docs
- Hardhat / Foundry / Sourcify wiring
- custom explorer deploy scripts

## Structural Scores
- Fragmentation: 4
- Manual pain: 4
- Economic value: 4
- Objective measurability: 4
- Execution potential: 3
- Timing: 4
- Competition gap: 3
- Prototype feasibility: 4
- Total: 8

## Repeated Pain Or Demand Signal
Teams want a way to know whether explorer deployment, verification wiring, or event delivery will fail before they ship a chain rollout.

## Likely User Or Buyer
Chain operators, explorer/platform teams, and protocol teams shipping EVM or multichain explorers.

## Current Workaround Or Money Signal
Users combine docs, APIs, framework plugins, and trial-and-error to get verification and indexing working.

## Money Evidence Type
direct_workflow_spend

## Money Evidence
Blockscout publishes paid Autoscout hosting plans, PRO API pricing, EAAS managed hosting, and enterprise-style explorer offerings for the same workflow family.

## Existing Paid Workflow
Teams already pay for hosted explorer deployment, verification APIs, multichain onchain data access, and managed explorer hosting.

## Current Workaround
Teams wire Hardhat, Foundry, Remix, or Sourcify verification paths, read docs, and manually debug webhook/indexer behavior.

## Current Cost
Autoscout starts at $349/mo; PRO API tiers start at $49/mo, $199/mo, and $999/mo, plus managed-hosting and engineering time.

## Why Buy From Us
A manual review compresses doc-reading and trial-and-error into one explicit risk report before the team commits engineering time.

## Why Buyer Would Buy From Us
A manual review compresses doc-reading and trial-and-error into one explicit risk report before the team commits engineering time.

## Build-vs-buy Reason
This is non-core but necessary cross-company coordination, not the chain's differentiating IP.

## Smallest Sellable Outcome
One manual Blockscout verification/indexer risk report for a single chain or explorer deployment.

## Manual First Delivery
Read the public docs and, if needed, a sanitized config dump, then return the top failure points, missing webhook wiring, and a rollout checklist.

## One-Sentence Offer
Send me your Blockscout verification setup and receive a 48-hour rollout-risk report within 48 hours for $750.

## Price Hypothesis
$750 manual report

## Buyer Acquisition Path
Public chain launch pages, Blockscout customer stories, explorer operators listed in docs and blogs, and protocol teams asking verification questions in public issues.

## Time To Transaction
4

## Time To Transaction Reason
Public pricing and docs make the workflow legible, and the first deliverable is a manual report that does not need private code or hardware.

## Productization Path
Turn repeated reviews into a small config checker or hosted audit that flags verification, webhook, and indexer gaps.

## Cashflow Falsification Test
If three reachable chain teams decline a paid review or say they would rather build it internally, keep it watchlisted.

## Technology Shift
- What changed: Blockscout added Autoscout, PRO API, websocket events, managed hosting, and customer deployment stories while more chains and L2s multiplied.
- When: 2024-2026, with the strongest commercial evidence in 2025-2026.
- Old constraint: teams had to stitch together custom explorer deployments, verification hooks, and per-chain integrations.
- New capability: teams can buy hosted explorer deployment, use a single multichain API key, rely on managed hosting, and wire verification/event delivery from public docs.
- Cost delta: Autoscout, EAAS, and PRO API tiers make the spend visible instead of implicit.
- Quality delta: fewer integration mistakes and faster onboarding are possible.
- Latency delta: faster initial deployment and verification-event handling.
- Accessibility delta: public docs, pricing, and launch pages make buyers reachable.
- Affected workflows: explorer deployment, contract verification automation, indexer setup, multichain event consumption.

## Buyer
Chain operators, explorer/platform teams, and protocol teams shipping EVM or multichain explorers.

## Expensive Workflow
Deploying a multichain explorer, wiring contract verification, and keeping verification events and indexers reliable across chains.

## Existing Spend
Autoscout, EAAS, and PRO API pricing show direct spend on explorer deployment and multichain onchain data; customer stories show real deployments.

## Paid Experiment
Offer a 48-hour manual review of one Blockscout verification/indexer setup to three public chain teams at a starter price and count one paid request as success.

## Money-First Scores
- Pain: 4
- Spend: 4
- Reachability: 4
- Timing: 4
- Buildability: 4

## Source Classes
- github
- docs
- pricing
- launch
- news

## Fragmented Providers
Blockscout explorers, chain RPC providers, verification frameworks like Hardhat, Foundry, Remix, and Sourcify, websocket consumers, and hosted explorer tiers.

## Multi-Provider User
Explorer and chain teams routinely combine Blockscout, chain RPCs, verification frameworks, and separate deployment or analytics tools.

## Boundary Workflow
The boundary workflow is wiring verification, websocket events, and multichain indexing between explorer, chain, and developer tooling surfaces.

## Build-vs-Buy Reason
This is non-core but necessary cross-company coordination, not the chain's differentiating IP.

## Internal Build Likelihood
medium

## Money Flow
Blockscout charges for Autoscout, EAAS, and PRO API access; chain teams pay RPC and infra vendors plus engineer time to integrate verification.

## Recurrence
Each new chain, explorer rollout, verification method, or websocket integration revives the same setup and debugging work.

## Permissionless Validation
A manual review can be done from public docs, pricing, and a sanitized config or publicly described chain setup.

## Smallest Wedge
One chain's verification/indexer rollout review that flags missing docs, webhook gaps, and event wiring issues.

## Intermediary Maturity
Partial: Blockscout already sells hosted explorers and APIs, but independent verification/setup review tooling is still immature.

## Paid Wedge
Save chain teams time and failed launches on explorer and verification setup.

## Distribution Channel
Sell directly to public chain launches, explorer operators, and Blockscout customers through public docs and blogs.

## Private Data Barrier
public-only

## OSS Commoditization Risk
medium

## Product Shape
report

## Pricing Hypothesis
pro

## Do Not Build Until
One buyer pays for a manual Blockscout verification/indexer review or three teams ask for the report after seeing the sample.

## Proposed Offer
Send me your Blockscout verification setup and receive a 48-hour rollout-risk report within 48 hours for $750.

## Success Threshold
One buyer pays for a manual Blockscout verification/indexer review or three teams ask for the report after seeing the sample.

## Falsification Threshold
If three reachable chain teams decline a paid review or say they would rather build it internally, keep it watchlisted.

## Evidence Gaps
- Blockscout still needs one real buyer to confirm the manual review is worth paying for.

## Labels
- M1 paid demand
- M2 repeated pain
- M3 competitor proof
- M4 workaround evidence
- I interpretation

## Decision
Sell-before-build. The paid workflow is already visible, the buyer is reachable, and the first delivery can be manual.

# Tailscale Split-Tunnel Routing Exception Diagnostics

## Opportunity Summary
Public Tailscale issues repeatedly ask for domain, app, and device exceptions to exit-node and DNS routing behavior. The opportunity is a routing-policy diagnostic that explains what will break before users deploy mixed VPN or split-tunnel setups.

## Evidence
- M2 repeated pain: `#6912` (2023-01-08) asks for Android split tunneling so specific apps can bypass the VPN.
- M2 repeated pain: `#13677` (2024-10-03) asks for website-based/IP-based split tunneling on macOS.
- M2 repeated pain: `#18378` (2026-01-10) reports an Android regression where excluded apps lose network access after update.
- M2 repeated pain: `#15521` (2025-04-03) asks to exclude certain domains from Mullvad exit-node routing.
- M4 workaround evidence: `#15521` also describes using an App Connector as a suboptimal workaround for domain exclusions.
- M4 workaround evidence: `#3506` (2021-12-05) shows users disabling Tailscale DNS settings or manually manipulating DNS search order to cope.
- M3 competitor proof: the macOS split-tunneling request explicitly points to PIA as an open-source example that already implements the feature.

## Structural Pattern
Routing-policy audit layer for VPN and overlay-network fragmentation across exit nodes, split DNS, app connectors, and competing VPN behaviors.

## Primitive Growth
Tailscale has expanded visible routing primitives around exit nodes, app connectors, split DNS, ACL policy, and paid team or enterprise plans.

## Fragmentation
Admin choices are fragmented across OS routing, Tailscale exit-node behavior, DNS overrides, app connectors, browser or app exceptions, and legacy VPN expectations.

## Manual Workflow
Admins manually compare docs, issue threads, device routing tables, DNS behavior, and policy settings to explain why traffic exits through the wrong path.

## Objective Function
Minimize broken routing and DNS exceptions while preserving security policy, expected app reachability, and administrator control.

## Execution Ladder
- Observe: Read public policy snippets, device route state, DNS configuration, app connector settings, and exit-node selection rules.
- Recommend: Explain mismatched routes, DNS exceptions, and risky split-tunnel assumptions before rollout.
- Choose: Rank routing-policy alternatives against reachability, privacy, security, and admin-maintenance constraints.
- Execute: Generate review output or policy diffs for admin approval; automatic network changes remain outside the first wedge.

## Economic Pain
The cost is admin rollout time, productivity loss from broken access, and security risk when users bypass or misconfigure routing policy.

## Timing Reason
Tailscale routing primitives, pricing, and docs became more productized in 2025-2026, but public threads still show split-tunnel and exception confusion.

## Competitors
- Tailscale admin console
- Tailscale docs and community support
- network-debugging scripts
- incumbent VPN management consoles

## Structural Scores
- Fragmentation: 4
- Manual pain: 4
- Economic value: 3
- Objective measurability: 3
- Execution potential: 3
- Timing: 3
- Competition gap: 2
- Prototype feasibility: 3
- Total: 6

## Repeated Pain Or Demand Signal
Users want fine-grained control over where traffic goes, but the current model still forces coarse app exclusion, DNS hacks, or alternative VPNs for everyday web traffic.

## Likely User Or Buyer
IT admins, security-conscious teams, and power users managing laptops, phones, and home or office exit-node policies.

## Current Workaround Or Money Signal
People disable MagicDNS, use App Connectors, exclude the browser, or switch to other VPN products when Tailscale routing does not fit the workflow.

## Money Evidence Type
budget_adjacency

## Money Evidence
Pricing pages and admin issue threads show adjacent budget and operational pain, not a direct paid diagnostic workflow.

## Existing Paid Workflow
Teams pay for VPN or network administration, but public evidence does not show payment for external split-tunnel diagnostics.

## Current Workaround
Admins read docs, compare route state, toggle DNS or app connector settings, and manually test excluded apps.

## Current Cost
Admin time, rollout delay, and productivity loss; direct diagnostic spend is not public.

## Why Buyer Would Buy From Us
A buyer would buy only if a pre-rollout report prevents support tickets or security bypasses better than internal admin work.

## Smallest Sellable Outcome
Manual routing-policy review for one exit-node, split-DNS, or app-connector scenario.

## Manual First Delivery
Collect a public or synthetic policy description, review expected routes and DNS behavior, and send an exception-risk report.

## One-Sentence Offer
Manual review of one Tailscale routing setup with likely split-tunnel and DNS failure points within 48 hours.

## Price Hypothesis
unclear until an admin confirms paid review demand.

## Buyer Acquisition Path
Find admins in Tailscale-adjacent communities, paid network-admin tasks, and small-team security forums.

## Time To Transaction
2

## Time To Transaction Reason
Low: the pain is reachable, but a standalone buyer and purchase path are not yet proven.

## Productization Path
Only after paid reviews repeat, encode common route and DNS checks into a local CLI or report template.

## Cashflow Falsification Test
If three admins reject a paid review or cannot name a budget owner, keep it in watchlist.

## Technology Shift
- What changed: Tailscale's exit-node, app-connector, and DNS docs now formalize routing choices, while pricing and enterprise plans make the product a budgeted admin tool.
- When: 2025-12-05 through 2026-08-11, with pricing and documentation refreshed in 2026.
- Old constraint: routing exceptions were debugged with ad hoc DNS changes, browser exclusions, or forum workarounds.
- New capability: admins can now reason about exit nodes, app connectors, split DNS, and plan-level features from public docs and pricing pages.
- Cost delta: unclear; public pricing proves budget attachment, but no dedicated diagnostic spend is visible.
- Quality delta: better routing control exists, but the public issues still show mismatch and regression risk.
- Latency delta: unclear.
- Accessibility delta: public docs and issue threads make the problem reachable, but the buyer path is still fuzzy.
- Affected workflows: exit-node rollout validation, split-tunnel policy debugging, DNS override troubleshooting, and mixed VPN administration.

## Buyer
IT admins, security-conscious teams, and power users managing laptops, phones, and exit-node policies.

## Expensive Workflow
Admins lose rollout time diagnosing split-tunnel routing exceptions, DNS behavior, and mixed-VPN conflicts.

## Existing Spend
Tailscale paid plans and admin labor prove adjacent networking budget, but direct external routing-diagnostic spend is not visible.

## Paid Experiment
Ask admins for a paid manual routing review only after finding direct evidence that teams buy this kind of pre-rollout diagnostic.

## Money-First Scores
- Pain: 4
- Spend: 1
- Reachability: 2
- Timing: 3
- Buildability: 3

## Source Classes
- github
- docs
- pricing
- product

## Fragmented Providers
Tailscale, Mullvad-style VPN use, OS routing tables, DNS controls, app connectors, and legacy VPN expectations create fragmented networking surfaces.

## Multi-Provider User
Admins and power users can combine Tailscale with other VPNs, OS routing, DNS providers, and app-specific exceptions, but direct budgeted multi-provider diagnostic demand remains weak.

## Boundary Workflow
The boundary workflow is explaining route, DNS, exit-node, browser, and app-connector behavior across overlay network, VPN, OS, and SaaS policy layers.

## Build-vs-buy Reason
A policy review is non-core admin glue for small teams, but Tailscale or incumbent network tooling could absorb the diagnostic path upstream.

## Internal Build Likelihood
medium

## Money Flow
Money flows through Tailscale paid plans, enterprise network administration, and VPN subscriptions, but direct external routing-diagnostic spend is not proven.

## Recurrence
The workflow recurs during rollout, device enrollment, routing-policy changes, app-connector changes, DNS changes, and mixed-VPN troubleshooting.

## Permissionless Validation
A first test can use public docs, synthetic route tables, sample DNS policies, and local repro scripts without needing private production networks.

## Smallest Wedge
Routing-policy review report for one exit-node, split-DNS, or app-connector scenario that predicts likely exception failures.

## Intermediary Maturity
Partial to high: admin consoles and docs exist, so an external review wedge has high commoditization risk unless buyers confirm pain.

## Paid Wedge
Unclear; public issues show repeated routing pain, but not a specific budget owner or paid diagnostic workflow.

## Distribution Channel
Likely CLI or report for admins, but the buying and installation path is still unproven.

## Private Data Barrier
unclear

## OSS Commoditization Risk
high

## Product Shape
report

## Pricing Hypothesis
unclear

## Do Not Build Until
At least 3 admins confirm they would use an external diagnostic before rollout, or 1 team asks for a paid routing review.

## Proposed Offer
A free routing-policy linter that checks a Tailscale configuration and explains whether it will need app split tunneling, domain exceptions, DNS overrides, or an App Connector.

## Success Threshold
At least 5 public users or admins run the linter in one week and report that it caught a real routing conflict before rollout.

## Falsification Threshold
Users say the current app-level workarounds are good enough, or they do not recognize split-tunnel friction as a recurring operational problem.

## Evidence Gaps
- No procurement or job-post evidence yet.
- Need better proof that admins would pay for diagnostics rather than rely on community knowledge.

## Decision
Watchlisted. Do not build until the paid wedge and distribution channel are validated outside issue threads.

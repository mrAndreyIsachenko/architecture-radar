## 1. Reproduce And Repair Identity Mismatch

- [x] 1.1 Reconcile the implementation baseline with current main without discarding local changes; record the tested base SHA and reproduce the September 25 mismatch in an isolated regression fixture.
- [x] 1.2 Extend structured report repair to expand unambiguous bare repository names consistently in ledger and backlog tables; tests must cover `bumblebee`, idempotence, reordered columns, Markdown code formatting, owner conflicts, same-name repositories, forge collisions, and missing evidence.
- [x] 1.3 Add canonical-identity and full-validator instructions to the research prompt; verify prompt tests and retain the independent workflow validation gate.

## 2. Preserve Failed Output

- [x] 2.1 Stage allowlisted regular research files with run/base/date provenance, excluding symlinks, credentials, raw logs, scratch clones, and unrelated files; verify positive and negative fixture tests.
- [x] 2.2 Upload the recovery bundle with seven-day retention after an executed research run fails, including downstream validation failure; test failure conditions, skipped cadence, no output, and unchanged failed conclusion/publication blocking.
- [x] 2.3 Document recovery and limitations; verify documented commands match the artifact layout and do not rerun paid research or publish automatically.

## 3. Recover And Validate The Incident

- [x] 3.1 Inspect run 36121754617 log patches as data and reconstruct complete allowlisted output at base e8e7441cb82e03ef52f71133615d38aa4ef40a70 in isolation; produce a per-file completeness inventory, explicitly identifying any missing or truncated output.
- [x] 3.2 Apply the identity repair to recovered output and run the full radar validator; retain the exact result and any remaining concrete blockers without fabricating research or spending API credits.
- [x] 3.3 Run the full unit suite, strict OpenSpec validation, shell syntax checks, relevant state validators, and diff whitespace checks; record results and keep failed checks unresolved.
- [x] 3.4 After explicit publication/run authorization, exercise a no-model CI failure fixture and verify a downloadable recovery artifact, failed workflow conclusion, and no invalid PR publication; record the run URL and leave this item open until verified.

## 1. Revision And Receipt Identity

- [x] 1.1 Include immutable head SHA in discovery and both PR summaries, pin report reads to that SHA, and detect a moving head; verify mocked concurrent-update and missing-SHA cases never yield a mixed-revision receipt identity.
- [x] 1.2 Implement the destination-scoped SQLite receipt store with version validation and transactional idempotent writes; test persistence, repository/thread isolation, concurrent acknowledgements, corrupt state, and write failures using temporary paths.
- [x] 1.3 Add explicit acknowledgement CLI options and message-reference validation; test that ordinary helper reads never create receipts, missing fields fail, and acknowledging an old SHA cannot suppress a new head.

## 2. Pending Reviews And Operational Status

- [x] 2.1 Filter repeated content only by exact matching receipts and expose pending/delivered review metadata for both families; test unchanged unacknowledged PRs, new commits, both-family queues, missing scope, and first-run state.
- [x] 2.2 Keep workflow failures, schedule waits, and concrete CI blockers independent of content delivery; test acknowledged PR plus failed run, blocked CI plus pending analysis, and no-pending-review output without falsely claiming no open PR exists.
- [x] 2.3 Update heartbeat integration documentation with the explicit visible-message acknowledgement protocol and scope/state commands; verify examples through CLI tests, including interrupted response and next-invocation acknowledgement. Do not claim automatic platform delivery confirmation or change active automation settings without authorization.

## 3. Acceptance

- [x] 3.1 Run the complete unit suite, Python compilation, strict OpenSpec validation, relevant existing validators, and whitespace checks; record results and any failures in validation evidence.
- [x] 3.2 Exercise a deterministic end-to-end delivery fixture: two pending PRs, printed but unacknowledged response, explicit receipt after visible delivery evidence, restart, suppression of that exact revision, and reappearance after a new SHA; additionally run a read-only live check without fabricating receipts and record the remaining live caller-adoption boundary.

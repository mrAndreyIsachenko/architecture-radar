# nasa/cFS

- Repository: https://github.com/nasa/cFS
- Review date: 2026-10-10
- Current commit reviewed: `ca14a5cce6954c1cbc464c536ea681b6798d3b44`
- Commit date: 2026-10-09T06:58:22-04:00
- Branch: `dev`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially delayed-connectivity command/telemetry loops, CFDP file transfer, table-driven flight configuration, and safe recovery from late or missing acknowledgements. The reusable mechanism is the CFDP engine and its transaction state machine, not the broader cFS bundle branding.

## Verified Flow

`CF_ValidateConfigTable()` and `CF_ManageTables()` validate and import the CF application config table -> `CF_CFDP_EncodeStart()` and `CF_CFDP_DecodeStart()` reset the codec state and clamp the payload window to the encapsulation header -> `CF_CFDP_S_SendFileData()` seeks, reads, chunks, and CRCs outbound data before sending a file-data PDU -> `CF_CFDP_R_ProcessFd()` seeks, writes, and records received chunks so the gap list can be updated -> `CF_CFDP_R_SubstateRecvEof()` and `CF_CFDP_R_CheckComplete()` manage EOF handling, ack/nak counting, CRC checking, and completeness detection -> `cf_cfdp_tests.c` covers the codec, timer, transaction, send/receive, and engine-cycle paths.

- E1 source verified: `apps/cf/fsw/src/cf_app.c:50-240,278-278` implements table-driven configuration import and validation.
- E1 source verified: `apps/cf/fsw/src/cf_cfdp.c:68-146,177-253,1057-1238` implements PDU start, timer arming, ack/nak counting, and receive dispatch.
- E1 source verified: `apps/cf/fsw/src/cf_cfdp_r.c:79-250,636-677,897-905,989-989` implements receive-side completeness, file-data processing, EOF handling, and transaction completion checks.
- E1 source verified: `apps/cf/fsw/src/cf_cfdp_s.c:49-220,229-258,1030-1030` implements outbound file-data chunking, early-FIN cancellation, and FIN handling.
- E2 test verified: `apps/cf/unit-test/cf_cfdp_tests.c:37-214,184-214,1952-2046` covers codec setup, transaction setup, receive/send helpers, engine cycle, and the registered CFDP test suite.

## Architecture

Principal components:

- Table-driven CF application configuration and channel import.
- CFDP encoder/decoder helpers with bounded message windows.
- Send-side and receive-side CFDP transaction state machines.
- Chunk tracking and gap detection for partial file receipt.
- Unit tests that pin the codec, transaction, timer, and lifecycle paths.

Most interesting mechanism: the transfer engine is explicit about timer windows, ack/nak limits, chunk offsets, and recovery from partial receipt. That makes delayed-connectivity file transfer and retransmit behavior visible instead of implicit.

Baseline comparison: a simple file-transfer app would copy bytes in one shot and assume the link is reliable. This implementation models retransmit timing, incomplete receipt, early FIN cancellation, and receive-side gap tracking.

## Reuse Guidance

Reusable:

- Treat file transfer as a transaction with explicit state, not a one-off copy.
- Use bounded chunk sizes and compare them to remaining PDU space.
- Track gaps on the receive side so completeness can be proven from state, not assumption.
- Keep config table validation strict enough to reject unsafe timing and chunk sizes early.

Do not copy:

- Do not copy the whole cFS bundle if the only need is the CFDP transaction model.
- Do not treat the fixed-size channel and transaction structures as generic application state.
- Do not assume the transaction logic is sufficient without a live delayed-connectivity run.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Configuration is table-driven and validated before it is imported.
- CFDP send and receive code separate codec setup from transfer logic.
- The unit-test suite covers a wide range of codec, timer, and transaction cases.
- Early-FIN, CRC mismatch, seek/write failures, and ack/nak limits are explicit failure modes.

Experimental or incomplete for our needs:

- The review did not run an integrated bundle with live delayed acknowledgements or packet reordering.
- The CFDP logic still depends on mission-specific tables and channel configuration.
- The top-level bundle is a demo distribution, not a fully verified operational system.

Hidden costs and failure modes:

- Timer and ack/nak limits can exhaust quickly if the channel is misconfigured.
- Seek/write failures hard-stop the transaction and rely on higher-level recovery.
- The transaction engine assumes its surrounding mission tables and channels remain coherent.

Adoption experiment:

Run the CFDP app inside the integrated cFS bundle with delayed acknowledgements and out-of-order returns, then confirm that chunk tracking, EOF completion, and cancellation behave as the transaction state machine predicts.

## Candidate Patterns

- `bounded CFDP transaction engine`
- `chunked delayed-transfer state machine`
- `table-driven CFDP configuration`
- `gap-tracked file receive path`

# JosefHobler/stm32-ccsds-node

- Repository: https://github.com/JosefHobler/stm32-ccsds-node
- Review date: 2026-10-19
- Current commit reviewed: `838f4d5b5a800489ccf33b0e7b00c7124652e680`
- Commit date: 2026-06-07T16:02:53+02:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `satellites-space-systems` through a command/telemetry loop that survives framing errors and stalled tasks. The useful mechanism is the watchdog-gated TM/TC path, not the demo board branding or the fact that it is built around one specific STM32 target.

## Verified Flow

`app_start` creates the UART mutex, alive event group, and sensor queue, then starts sensor, telemetry, telecommand, and watchdog tasks -> `HAL_UART_RxCpltCallback` re-arms the UART receive interrupt and forwards bytes into the telecommand path -> `telecommand_task` accumulates bytes in a stream buffer, computes frame length, decodes CCSDS packets, dispatches commands, sends ACKs, and slips past invalid CRCs or headers -> `telemetry_task` emits housekeeping telemetry and refreshes its heartbeat on a bounded period -> `watchdog_task` refreshes the hardware watchdog only when every task has checked in.

- E1 source verified: `Core/Src/app.c::app_start`, `::watchdog_task`, and `HAL_UART_RxCpltCallback` create the task set, enforce the heartbeat window, and feed single-byte UART interrupts into the telecommand path.
- E1 source verified: `Core/Src/telecommand_task.c::telecommand_task`, `::dispatch`, `::framed_total`, and `telecommand_uart_rx_isr` implement stream-buffer framing, command dispatch, ACKs, reboot handling, and byte-slip resynchronization.
- E1 source verified: `Core/Src/telemetry_task.c::telemetry_task`, `::tm_set_period_ms`, and `::emit_hk` implement periodic housekeeping and heartbeat pacing.
- E2 test verified: `cpp/tests/conformance_test.cpp` covers round-trip encoding, byte-identical encode/decode, corrupted CRC rejection, truncation rejection, wrong-version rejection, and out-of-range field rejection.
- E2 test verified: `cpp/tests/framer_test.cpp` covers complete frames, split frames, garbage-prefix slip, corrupted-frame recovery, back-to-back frames, and truncated-frame buffering.
- E2 test verified: `cpp/tests/differential_test.cpp` cross-checks decode/re-encode against Python-generated frames, and `cpp/tests/codec_test.cpp` pins CRC and fixture behavior.

## Architecture

Principal components:

- FreeRTOS task set for sensor, telemetry, telecommand, and watchdog responsibilities.
- UART interrupt hook and stream buffer for command intake.
- CCSDS codec and framer for packet encode/decode.
- Python ground station and C++ tests for cross-implementation conformance.

Most interesting mechanism: the watchdog only refreshes when all tasks have checked in, so a stuck telemetry or telecommand path deliberately becomes a reset condition. Combined with byte-slip framing, that turns malformed or partial input into a recoverable state instead of a permanent stall.

Baseline comparison: a simple serial control loop would assume clean bytes and keep running as long as the UART ISR fires. This implementation makes framing recovery explicit and ties board liveness to task health rather than to raw interrupt activity.

## Reuse Guidance

Reusable:

- Keep one task responsible for framing and one for telemetry emission.
- Use byte-slip resynchronization instead of assuming headers are aligned.
- Gate watchdog refresh on explicit task heartbeats.
- Keep cross-language codec conformance tests so firmware, ground station, and host tooling agree on wire format.

Do not copy:

- Do not copy the demo serial REPL as a production ground station.
- Do not assume the conformance tests prove hardware timing or UART noise tolerance.
- Do not rely on reboot ACKs without an external operator or harness verifying the restart path.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The firmware, ground station, and codec tests all describe the same wire format.
- The watchdog path and slip-resync path are explicit in source, not implicit in comments.

Experimental or incomplete for our needs:

- Real flashed-board runtime behavior still needs proof.
- The review did not validate watchdog recovery under induced noise or reboot churn.

Hidden costs and failure modes:

- A stuck task will deliberately let the watchdog reset the board.
- Framing state can drift if the UART path is noisy and the host never drains the queue.
- Runtime safety depends on the telemetry heartbeat staying below the watchdog window.

Adoption experiment:

Flash the firmware to target hardware, connect the Python ground station, inject malformed and partial frames, and confirm the watchdog and slip-resync paths recover without deadlocking the control loop.

## Candidate Patterns

- `watchdog-gated TM/TC loop`
- `byte-slip frame resynchronization`
- `cross-implementation packet conformance`

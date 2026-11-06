# JosefHobler/stm32-ccsds-node

- Repository: https://github.com/JosefHobler/stm32-ccsds-node
- Review date: 2026-11-06
- Current commit reviewed: `838f4d5b5a800489ccf33b0e7b00c7124652e680`
- Commit date: 2026-06-07
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially delayed-connectivity command/telemetry loops, framing recovery, and watchdog-supervised liveness. The reusable mechanism is a small CCSDS TM/TC loop that keeps the firmware alive with explicit alive bits, slip-resync parsing, and wire-format conformance tests spanning both C and C++ implementations.

## Verified Flow

UART RX interrupt -> `telecommand_uart_rx_isr` pushes bytes into a stream buffer -> `telecommand_task` reconstructs CCSDS frames, validates header length and CRC, and dispatches commands -> `telemetry_task` emits heartbeat and periodic HK telemetry from the queue -> `watchdog_task` refreshes the IWDG only when all alive bits are present -> `ccsds_encode` / `ccsds_decode` provide the framing and checksum boundary -> C++ conformance tests prove byte-identical wire output and reject corrupted frames.

- E1 source verified: `Core/Src/app.c:22-96` serializes UART transmission, creates the telemetry/telecommand/watchdog tasks, and re-arms the UART RX interrupt path.
- E1 source verified: `Core/Src/telecommand_task.c:24-170` feeds the stream buffer from ISR bytes, slip-resyncs on invalid framing, dispatches command handling, and sends ACK/version/reboot responses.
- E1 source verified: `Core/Src/telemetry_task.c:11-55` clamps the telemetry period, emits HK telemetry from the sensor queue, and keeps the watchdog heartbeat alive.
- E1 source verified: `Core/Src/ccsds.c:4-71` implements CRC-16/CCITT-FALSE, CCSDS packet encoding, and decode-time validation of version, length, and CRC.
- E2 test verified: `cpp/tests/conformance_test.cpp:80-188` covers encode/decode round-trips, byte-identical fixtures, re-encode equality, and rejection of corrupted or malformed frames.

## Architecture

Principal components:

- Firmware-side UART interrupt handling and packet serialization.
- Telecommand parser with stream-buffer recovery and slip-resync.
- Telemetry task with runtime-adjustable period and heartbeat emission.
- Watchdog task that enforces liveness across all task groups.
- C++ codec conformance suite that guards the wire contract.

Most interesting mechanism: the firmware does not treat framing, liveness, and recovery as separate concerns. The UART path, packet parser, watchdog, and tests all protect the same end-to-end CCSDS contract, which makes the implementation useful beyond its specific board.

Baseline comparison: a simpler UART telemetry loop would usually decode bytes directly and rely on a single periodic task. This code adds watchdog supervision, slip-resync parsing, and cross-language byte-for-byte conformance checks.

## Reuse Guidance

Reusable:

- Keep a separate watchdog task that observes task-level alive bits.
- Make the parser slip-resync instead of aborting on the first bad frame.
- Verify codec behavior across at least two implementations.
- Bound telemetry emission with a minimum heartbeat so the watchdog cannot starve.

Do not copy:

- Do not copy the firmware command set as a generic abstraction.
- Do not assume the watchdog logic is sufficient without live hardware or emulator proof.
- Do not depend on this exact task split unless the target scheduler and UART path look the same.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The firmware keeps UART, telemetry, telecommand, and watchdog responsibilities separate.
- The parser validates length, version, and CRC before dispatch.
- The C++ tests check both fixture identity and failure cases.

Experimental or incomplete for our needs:

- The review still needs runtime proof on hardware or an emulator.
- The code is intentionally minimal, so integration behavior under packet loss and watchdog stalls is still an open question.

Hidden costs and failure modes:

- A stalled telemetry task can trip the watchdog even if the rest of the firmware is healthy.
- Slip-resync protects the parser, but it can hide repeated framing errors if the transport degrades badly.
- The code assumes the UART and RTOS timing model remain stable.

Adoption experiment:

Run the firmware on hardware or an emulator, inject corrupted UART frames and long task stalls, and confirm the parser recovers by slip-resync while the watchdog only resets on genuine liveness failure.

## Candidate Patterns

- `watchdog-supervised CCSDS TM/TC loop`
- `slip-resync framing`
- `cross-language packet conformance`

## Previous Reviews

First review. The runtime/hardware validation gap is recorded in the backlog and remains open.

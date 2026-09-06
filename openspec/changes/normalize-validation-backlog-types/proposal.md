# Normalize Validation Backlog Types

## Why

Architecture Radar strict validation rejects `experiments/failure-injection-backlog.yml`
when a generated backlog item writes a descriptive or combined `validation_type`
instead of one schema enum value. A previous scheduled run failed on
`runtime validation and failure-injection`, which is a recoverable formatting
error rather than bad research evidence.

## What Changes

- Make the Architecture Radar prompt explicitly list the allowed
  `validation_type` enum values.
- Add deterministic repair for known descriptive or combined validation type
  phrases before strict validation.
- Keep unknown validation types as validation failures.

## Non-Goals

- Do not expand the validation type schema.
- Do not weaken backlog validation.
- Do not alter generated research artifacts unrelated to validation backlog
  structure.

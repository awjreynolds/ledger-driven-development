---
name: ldd-verify
description: Run /ldd:verify for an implemented LDD child ticket. Use when the user says /ldd:verify or wants to verify child-ticket closure readiness after implementation completion.
---

# /ldd:verify

Verify whether one implemented child work item is ready for human-approved closure.

This command is a standalone, agent-agnostic LDD command. Follow this file directly; do not require any other installed skill.

## Reads

- child ticket `ledger.yml`
- child ticket body
- parent ticket `ledger.yml`
- approved parent PRD
- approved parent SDD
- approved parent plan
- implementation evidence
- check evidence
- external drift metadata when configured

## Writes

- `verification.md` in the child ticket directory
- child ledger `artifacts.verification`
- child ledger `closure.status`
- compact child ledger events for verification pass or failure

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Verification is specific to child-ticket closure. It is not a general repository healthcheck.
- Keep implementation completion separate from ticket closure.
- Treat external tracker state as a projection. If external metadata shows unresolved drift, block closure and ask for human reconciliation.
- Do not mutate external trackers, archive child tickets, close external tickets, push branches, or create PRs from this command.
- Recommend closure only when the child acceptance criteria, approved parent artifacts, implementation evidence, check evidence, and drift checks all support closure.
- If evidence is missing or checks failed, write the blocking reason to `verification.md` and leave `closure.status` unclosed.

## Package Surface Contract

This initial package surface establishes `/ldd:verify` as an installable command. Later LDD slices may expand the detailed report contract, but they must preserve these invariants:

- repo-local `ledger.yml` remains the machine-readable source of truth
- `verification.md` remains the human-readable verification report
- verification may recommend closure but must not perform human-confirmed external mutations
- child-ticket closure stays separate from implementation completion

## Stop Conditions

- missing child ticket
- missing approved parent PRD, SDD, or plan
- missing implementation evidence
- failed or missing check evidence
- unresolved external drift
- requested external mutation without human confirmation

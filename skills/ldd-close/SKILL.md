---
name: ldd-close
description: Run /ldd:close for a verified LDD child ticket. Use when the user says /ldd:close or wants to apply human-approved closure after /ldd:verify passed.
---

# /ldd:close

Apply closure for one verified child work item.

This command is a standalone, agent-agnostic LDD command. It does not decide whether implementation is correct; `/ldd:verify` owns that gate.

## Inputs

```text
/ldd:close <child-ticket-id>
```

If no child ticket ID is provided, stop and ask for one.

## Reads

- child ticket `ledger.yml`
- child `verification.md`
- parent ticket `ledger.yml`
- `.ldd/config.yml`
- external drift metadata when configured

## Writes

- child ledger `closure.status`
- parent ledger child status and `execution_context`
- archive location under configured `archive_directory`
- external tracker close/sync only after explicit human confirmation

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Close only child work items. Parent Product Requirement closure remains a separate roll-up decision unless explicitly requested.
- Require `artifacts.verification.status: passed` and `closure.status: verified` before closing.
- Require a readable `verification.md` report before closing.
- Refuse closure when verification is missing, pending, failed, or `override_required`.
- Refuse closure when external tracker drift is unresolved.
- Archive locally; do not delete evidence. This command may archive child tickets only after local ledger updates are ready.
- Preserve the child ledger, ticket body, verification report, and implementation evidence.
- Update `/ldd:next` state by pointing the parent ledger to the next close, verify, implement, decompose, or done gate.

## Workflow

1. Resolve the child ticket directory and read its `ledger.yml`.
2. Read the parent ledger and configured archive directory.
3. Confirm verification passed:
   - `artifacts.verification.status: passed`
   - `closure.status: verified`
   - `verification.md` exists
4. Check external drift metadata. If drift is unresolved, stop.
5. If an external tracker is configured, ask for explicit confirmation before mutating it.
6. Update the child ledger:
   - set `closure.status: archived` for local-only closure
   - set `archived_at`
   - add a `child_archived` event
   - set `external_closed_at` only if an external close actually occurred
7. Move the child directory to `docs/tickets/_archive/<child-id>-<slug>/` or the configured archive directory.
8. Update the parent ledger child entry to `archived` and point `path` to the archive location.
9. Recompute parent `execution_context`:
   - verified but unarchived child: `/ldd:close <child-id>`
   - implemented but unverified child: `/ldd:verify <child-id>`
   - ready child: `/ldd:implement <child-id>`
   - approved plan with no children: `/ldd:decompose`
   - all children archived: report parent ready for final review or done
10. Report the closure result and next command.

## Ledger Update Contract

After local-only closure, child ledger state should be equivalent to:

```yaml
closure:
  status: archived
  verified_at: 2026-05-13T00:00:00Z
  archived_at: 2026-05-13T00:00:00Z
  external_closed_at: null
  override_reason: null
events:
  - at: 2026-05-13T00:00:00Z
    type: child_archived
    actor: agent
```

Parent ledger child entry should be equivalent to:

```yaml
children:
  - id: LDD-0001-001
    status: archived
    path: docs/tickets/_archive/LDD-0001-001-slug/ledger.yml
```

Preserve existing unrelated ledger fields and events.

## External Tracker Rule

If the child has an external tracker projection, `/ldd:close` may close or sync it only after explicit human confirmation in the current turn. If confirmation is missing, close locally only when safe and report the pending external action, or stop if the requested operation requires external consistency.

If external drift exists, stop and ask the human to reconcile before closing.

## Stop Conditions

- missing child ticket
- missing parent ledger
- missing `verification.md`
- `artifacts.verification.status` is not `passed`
- `closure.status` is not `verified`
- unresolved external drift
- external close requested without explicit human confirmation
- archive move would overwrite an existing archive directory

---
name: ldd-refine
description: Run /ldd:refine for an LDD ticket. Use when the user says /ldd:refine or wants to sharpen an LDD PRD for engineering handoff and review.
---

# /ldd:refine

Polish `prd.md` in the active draft or promoted ticket directory for the Product-to-engineering handoff, then use human approval as the gate that turns the draft into a real Product Requirement ticket.

## Owns

- Testable acceptance criteria
- Measurable success metrics
- Resolved or explicitly owned open questions
- Clear dependencies
- Removal of vague or solution-smuggling language

## Rules

- Repo-local ledger is canonical. External trackers are optional sync/review surfaces.
- External mutations require human confirmation.
- Product Manager command: do not read the codebase as a design input.
- Use the PRD template's quality bar and handoff checklist before proposing a PRD PR.
- Do not expand scope or add technical design.
- Preserve the Product Manager boundary: acceptance criteria describe required product/workflow outcomes, not the engineering solution that will satisfy them.
- Commit locally after refinement.
- End refinement with an explicit approval prompt: `Reply approve PRD to promote the committed PRD to a stable ticket and create or sync the external Product Requirement ticket when a tracker is configured.`
- If the human has already approved the refined PRD in the current turn, do not stop at a refined draft. Promote it immediately.
- Promotion assigns the stable ticket ID, moves the draft directory out of `_drafts`, updates `ledger.yml` and PRD frontmatter links/IDs, marks the PRD approved, and commits the promotion.
- In `local` tracker mode, the promoted repo-local ledger directory is the real Product Requirement ticket.
- In an external tracker mode, promotion creates or binds the external Product Requirement ticket and records its ID/URL in `ledger.yml`.
- External Product Requirement tickets must be readable without opening the repo. Use `.ldd/templates/issue-body-prd.md` and include the PRD problem, goals, non-goals, users, user stories, acceptance criteria, success metrics, dependencies, open questions, and LDD links.
- Before updating an existing external ticket, re-read it. If its body changed since the last recorded sync hash or timestamp, stop and ask the human to reconcile the external contribution.
- PRD PR reviewer prompt: "Is this ready for engineering design?"

## Stop Conditions

- missing elaborated PRD
- acceptance criteria cannot be made testable
- open questions lack owner or resolution
- refinement reveals a scope problem, which returns to `/ldd:scope`

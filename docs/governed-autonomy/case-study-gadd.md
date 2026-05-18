# Case Study: GADD

GADD is a case study in Governed Autonomy applied to software delivery.

It does not define the full scope of Governed Autonomy. It shows how the philosophy can become a concrete methodology for one complex business process: moving software work from intake to verified closure.

![GADD case study map](assets/gadd-case-study-map.svg)

## Business Process

GADD governs the software-delivery process from unclassified intake through requirements, design, planning, implementation, verification, closure, and optional archive cleanup.

## Roles

| Governed Autonomy concern | GADD expression |
| --- | --- |
| Process owner | Team or organization adopting GADD |
| Product authority | Product Manager and Product Requirement lane |
| Technical authority | EM, Tech Lead, Architect, and Technical Design lane |
| Operator | Software Engineer and `/gadd:implement` |
| Reviewer | Engineering Review and `/gadd:verify` |
| Approver | Human approval through `/gadd:approve` and closure confirmation |
| Autonomous system | Agent executing bounded `/gadd:*` skills |

## Boundaries

GADD keeps boundaries explicit through:

- triage outcomes
- Product Requirement scope
- Software Design Documents
- implementation plans
- child Work Items
- verification reports
- closure decisions

Each boundary defines what the agent may do next and what evidence or approval is required before progression.

## Evidence

GADD uses repo-local artifacts as evidence:

- `ledger.yml` for canonical workflow state
- `research.md` where pre-scope investigation is needed
- `prd.md` for product scope
- `sdd.md` for technical design
- `plan.md` and `plan.html` for implementation planning
- child Work Item files for vertical slices
- implementation evidence from code, tests, and documentation impact
- `verification.md` for closure readiness

## Existing Systems

GADD treats external planning and review tools as projection surfaces unless explicitly configured otherwise.

GitHub Issues, Jira, Linear, Asana, and similar systems can be useful collaboration surfaces, but GADD's repo-local ledger remains canonical workflow state in the current model.

## Risk Mitigation

| Uncontrolled AI risk | GADD mitigation |
| --- | --- |
| Chat as a control plane | `ledger.yml` stores canonical workflow state |
| Unbounded delegation | `/gadd:*` skills have command-specific contracts and input gates |
| Role collapse | Product, design, implementation, verification, and closure are separate lanes |
| Evidence drift | PRD, SDD, plan, Work Item, and verification artifacts record evidence |
| Approval theater | `/gadd:approve` approves specific PRD, SDD, or plan gates |
| Tool sprawl | external systems are projections, not hidden sources of truth |
| Scope creep at machine speed | scope gates and decomposition boundaries reset unauthorized expansion |

## What This Shows

GADD demonstrates the Governed Autonomy pattern in a domain where autonomous execution can otherwise collapse planning, design, implementation, and review into one chat loop.

The broader lesson is not software-specific: autonomy becomes safer when the process defines roles, boundaries, evidence, escalation, approval, and canonical state before execution accelerates.

## Read Next

- [Related Landscape](related-landscape.md) positions Governed Autonomy alongside adjacent AI and process-governance disciplines.
- [References](references.md) lists the standards, research, and market writing that informed the framing.
- [Governed Autonomy overview](README.md) returns to the main section index.

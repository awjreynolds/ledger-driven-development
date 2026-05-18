# Uncontrolled AI risk patterns

Uncontrolled AI is rarely a problem of bad answers. The harder problem is that it can change how a business process actually runs, faster than the organization can see, explain, or correct.

![Uncontrolled AI compared with Governed Autonomy](assets/uncontrolled-ai-vs-governed-autonomy.svg)

The patterns below are the recurring shapes that show up when autonomy starts escaping process design. Most teams will recognize at least three.

## Chat as a control plane

When process state (decisions, approvals, evidence, current status) lives in a chat thread, the organization loses the ability to see where things are. Recovery, audit, and handover all depend on scrolling, and there is no canonical record of who approved what. The fix is unglamorous: pick a durable system of record and treat chat as an interaction surface rather than the source of truth.

## Unbounded delegation

The system goes from advising to acting, without anyone having drawn a line between the two. Tool access expands, execution rights expand, and no one wrote down where it should stop. A helpful assistant turns into an uncontrolled operator one Slack thread at a time. Boundaries (allowed actions, prohibited actions, escalation conditions, approval points) have to exist *before* the tools are wired up, not after the first incident.

## Role collapse

*One AI session quietly becomes analyst, operator, designer, reviewer, approver, and auditor.*

Separation of duties depends on those roles being held by different actors. When a single system proposes a change, executes it, signs off on the result, and writes the record, the controls that depended on independence are gone, even if no one announced their removal. AI can assist several roles. It cannot consolidate them.

## Evidence drift

**What it looks like:** Actions land faster than the rationale, source data, and checks behind them can be captured.

**Why it creates risk:** Reviewers reconstruct after the fact instead of inspecting at the time. Audit collapses into guesswork.

**Response:** Make evidence a required output of each governed step, not a downstream artifact.

## Approval theater

**What it looks like:** A human clicks Approve on a large bundle of AI-generated work, without clear evidence, alternatives, risk summary, or scope boundary in front of them.

**Why it creates risk:** Oversight exists in form but not in substance, and the org gets the worst of both worlds: slow process *and* unchecked autonomy.

**Response:** Place approvals at meaningful transitions and give them the context required to be a real decision, not a signoff ritual.

## Tool sprawl

Autonomous work touches a planning system, a ticketing system, a few documents, two dashboards, and a chat channel. Each of them has *some* of the truth. None of them holds the canonical state, and no one has been asked to decide which one should. Planning, execution, review, and reporting then drift away from each other in slow motion. Assigning canonical state (even arbitrarily, even temporarily) matters more than picking the "right" tool.

## Accountability gaps

*When an AI-driven action causes harm or confusion, no named person can explain the decision or accept responsibility for correcting it.*

This is what "the system did it" looks like in practice. Accountability has migrated from people and roles into an opaque execution path, usually without anyone deciding that this is what they wanted. Every delegated step needs a human role that owns it: owns the purpose, the outcome, and the cleanup.

## Scope creep at machine speed

A narrow request expands sideways because the system infers adjacent tasks and just does them. The diff is bigger than the brief, the change touches systems that weren't in the conversation, and by the time anyone notices, the new behavior is in production. Scope, non-goals, stop conditions, and explicit boundary-reset triggers are not bureaucratic overhead here. They're the only thing keeping a five-minute request from turning into a three-day rollback.

## Post-hoc governance

*Controls show up after an AI workflow already exists and is already producing operational effects.*

By that point, governance is cleanup work, reverse-engineering policies onto a running system that grew without them. The earlier these controls land, the cheaper and more honest they are. Designing them in before autonomy increases is the only version of this that doesn't carry a debt.

## Read next

- [Operating model](operating-model.md) defines the controls that mitigate these patterns.
- [Case study: GADD](case-study-gadd.md) shows these risks mitigated in one software-delivery process.
- [Governed Autonomy overview](README.md) returns to the main section index.

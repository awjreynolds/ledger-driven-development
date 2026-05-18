# Governed Autonomy

Governed Autonomy is what's left of business-process discipline once autonomous systems start doing real work inside the process. It names who is accountable, what the system is allowed to do, what evidence has to exist before a step counts as done, and when a human has to approve.

The disciplines underneath are not new: process management, Responsible AI, risk management, auditability, operating model design. Governed Autonomy is a lens for applying them once an autonomous system is one of the actors.

## ELI5

Let AI help do the work. Keep people in charge of what matters, what counts as done, and who has to sign off.

## Why this matters

AI transformation gets framed as task automation. The real exposure is upstream of that. An autonomous system can change how work flows through an organization faster than anyone can inspect, explain, or correct it.

Asking "can AI do this task?" is the wrong unit. The useful question is whether a business process can safely delegate a step, under what boundaries, with what evidence, with what escalation, and with whose approval.

Governed Autonomy is a synthesis. It doesn't replace existing governance or process-improvement work. It's the part of that work that becomes load-bearing once autonomy enters the loop.

## The business process is the unit of design

This isn't a software pattern or a vertical-specific framework. Anywhere work moves through a process (approvals, case handling, compliance review, procurement, incident response, support) the same questions apply. Understand the process, decide where autonomy can participate, and design the controls that keep humans accountable for purpose, risk, and outcome.

## What must stay governed

![Governed Autonomy loop](assets/governed-autonomy-loop.svg)

- Purpose: what the process is trying to achieve.
- Authority: who or what is allowed to act.
- Scope: what is inside and outside the delegated work.
- Evidence: what must be recorded so decisions can be reviewed.
- Escalation: when the autonomous system must stop or ask for help.
- Approval: which transitions need explicit human consent.
- Closure: how completion is verified and accepted.

## Where GADD fits

GADD is the first documented case study in this repository. It's a software-delivery methodology that applies Governed Autonomy to intake, requirements, design, planning, implementation, verification, and closure. It's one process. Governed Autonomy is the broader pattern.

## Read next

- [Operating model](operating-model.md)
- [Process assessment](process-assessment.md)
- [Uncontrolled AI risk patterns](uncontrolled-ai-risk-patterns.md)
- [GADD case study](case-study-gadd.md)
- [Related landscape](related-landscape.md)
- [References](references.md)

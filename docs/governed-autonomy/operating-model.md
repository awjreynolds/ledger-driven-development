# Governed Autonomy operating model

This is the working layer beneath the philosophy. It turns Governed Autonomy from a principle into a repeatable way to design, improve, and govern business processes that include autonomous systems, so that those processes remain inspectable, accountable, and reversible as autonomy increases.

## 1. Roles and decision rights

Name the roles in the process before assigning autonomy to anything.

- Process owner: accountable for process outcomes.
- Domain owner: accountable for policy, service, or business correctness.
- Operator: performs or supervises work.
- Reviewer: checks evidence and quality.
- Approver: authorizes a governed transition.
- Auditor or assurance role: inspects traceability after the fact.
- Autonomous system: executes bounded work but does not own accountability.

For each role, write down what it can decide, what it can delegate, and what it must escalate.

## 2. Authority boundaries

What an autonomous system is allowed to do without further approval should be documented, not inferred. That means:

- allowed actions and prohibited actions
- spending, risk, policy, or customer-impact limits
- systems it may read, and the (usually narrower) set it may write
- conditions that require human intervention

Anything not listed is out of scope. If the agent has to ask "am I allowed to do this?", the answer needs to live in the document, not in the model.

## 3. Input quality gates

A step shouldn't start just because a prompt exists. Decide up front what counts as a viable input: source of request, desired outcome, constraints, relevant records, sensitivity or policy concerns, known risks, and owner or approver.

Weak input routes to clarification, research, or human decision. It does not route to silent execution.

## 4. Scope and execution boundaries

Boundaries prevent a narrow request from quietly expanding into unmanaged operational change.

For each delegated step, state:

- what is in scope
- what is out of scope
- what assumptions are allowed
- what changes require a boundary reset
- when the system must stop

## 5. Risk and blast radius

Autonomy should be proportional to what the step can break. Walk the obvious axes: customer or citizen impact, financial impact, legal or regulatory exposure, reversibility, data sensitivity, operational dependency, and cross-team or cross-system reach.

Higher blast radius requires stronger evidence, more approvals, real monitoring, and a rollback path that someone has actually tried.

## 6. Evidence requirements

Evidence is what makes a governed step reviewable later. The reviewable artifact varies by process, but typically includes the input received, the data sources consulted, the assumptions made, the decision rationale, the action taken, and the resulting system change. It should be captured as the step runs, not reconstructed afterward.

## 7. Escalation and approval

These get conflated and shouldn't be. Escalation is the system saying "I've hit a boundary, I need help." Approval is a human authorizing a transition the process explicitly reserves for a human. Both need to be defined before deployment, and they should not be the same person clicking the same button.

## 8. State and auditability

Important process state should not live only in chat. Governed processes need a durable source of truth for current state, evidence, approvals, and closure. Other systems can stay as collaboration surfaces, but the operating model has to be unambiguous about which record is canonical.

## 9. Projection into existing systems

Most organizations don't get to invent a new stack. Planning systems, ticketing systems, case-management tools, spreadsheets, workflow platforms, and documents can project status and review information from the canonical record. They will drift into being treated as the source of truth unless the operating model says, in writing, that they aren't.

## Read next

- [Process assessment](process-assessment.md) turns this model into an assessment path for a real business process.
- [Uncontrolled AI risk patterns](uncontrolled-ai-risk-patterns.md) names the failure modes this operating model is meant to prevent.
- [Governed Autonomy overview](README.md) returns to the main section index.

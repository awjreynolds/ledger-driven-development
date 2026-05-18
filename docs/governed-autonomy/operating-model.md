# Governed Autonomy Operating Model

The operating model turns Governed Autonomy from a principle into a repeatable way to design, improve, and govern business processes that include AI or autonomous systems.

The value is not that AI does work. The value is that autonomous execution becomes governable at organizational scale.

## 1. Roles And Decision Rights

Name the roles in the process before assigning autonomy.

- Process owner: accountable for process outcomes.
- Domain owner: accountable for policy, service, or business correctness.
- Operator: performs or supervises work.
- Reviewer: checks evidence and quality.
- Approver: authorizes a governed transition.
- Auditor or assurance role: inspects traceability after the fact.
- Autonomous system: executes bounded work but does not own accountability.

For each role, define what it can decide, what it can delegate, and what it must escalate.

## 2. Authority Boundaries

Authority boundaries define what an autonomous system may do without further approval.

Document:

- allowed actions
- prohibited actions
- spending, risk, policy, or customer-impact limits
- systems the autonomous system may read or write
- conditions that require human intervention

## 3. Input Quality Gates

A process step should not start just because a prompt exists.

Define the minimum input needed for safe action:

- source of request
- desired outcome
- constraints
- relevant records
- sensitivity or policy concerns
- known risks
- owner or approver

Weak input should route to clarification, research, or human decision rather than silent execution.

## 4. Scope And Execution Boundaries

Boundaries prevent a narrow request from expanding into unmanaged operational change.

Each delegated step should state:

- what is in scope
- what is out of scope
- what assumptions are allowed
- what changes require a boundary reset
- when the system must stop

## 5. Risk And Blast Radius

Autonomy should be proportional to risk.

Assess:

- customer or citizen impact
- financial impact
- legal, regulatory, or policy exposure
- reversibility
- data sensitivity
- operational dependency
- reputational risk
- cross-team or cross-system impact

Higher blast radius requires stronger evidence, approvals, monitoring, and rollback paths.

## 6. Evidence Requirements

Governed autonomy requires evidence that can be reviewed.

Evidence may include:

- input received
- data sources consulted
- assumptions made
- decision rationale
- action taken
- system changes made
- checks performed
- escalation or approval records
- final outcome

## 7. Escalation And Approval

Escalation and approval are different.

Escalation means the autonomous system has reached a boundary and needs help. Approval means an accountable human authorizes a transition or action.

Define both before deployment.

## 8. State And Auditability

Important process state should not live only in chat.

Governed processes need a durable source of truth for current state, evidence, approvals, and closure. Existing systems can remain collaboration surfaces, but the process must make clear which record is canonical.

## 9. Projection Into Existing Systems

Governed Autonomy should usually work with the tools an organization already uses.

Planning systems, ticketing systems, case-management tools, spreadsheets, workflow platforms, and documents can project status and review information. They should not become accidental sources of truth unless the operating model explicitly assigns that role.

# Governed Autonomy process assessment

Run this before introducing or expanding AI autonomy in a business process. It's a structured way to decide which steps can be delegated safely, which need human judgment, and which controls have to exist before autonomy increases.

The work moves from the as-is process to the to-be process by making decision rights, handoffs, controls, evidence, and autonomy boundaries explicit.

## 1. Map the as-is process

Capture how work actually happens today:

- trigger
- requester
- current roles
- systems used
- handoffs
- approvals
- evidence produced
- common exceptions
- current pain points
- failure modes

## 2. Identify decision rights

For each decision in the process, ask:

- who owns the decision today?
- who is accountable if it goes wrong?
- what policy, law, standard, or business rule constrains it?
- can the decision be recommended by AI, drafted by AI, or executed by AI?
- what would require human review?

## 3. Classify autonomy level

![Business process autonomy ladder](assets/business-process-autonomy-ladder.svg)

A simple ladder is usually enough:

| Level | Pattern | Human role |
| --- | --- | --- |
| 1 | Assist | AI helps a human do the work |
| 2 | Recommend | AI proposes an option |
| 3 | Draft | AI prepares work for review |
| 4 | Execute with approval | AI acts only after explicit approval |
| 5 | Execute within limits | AI acts inside defined boundaries |
| 6 | Autonomous with monitoring | AI acts continuously with monitoring, audit, and escalation |

For high-risk steps, don't skip levels.

## 4. Define the to-be process

For each step, define:

- role owner
- autonomy level
- allowed action
- required input
- required evidence
- escalation condition
- approval condition
- completion condition

## 5. Design controls into the process

Controls should be part of the process design, not added once automation is already running.

Useful control types include:

- input quality gates
- authority limits
- dual approval
- evidence checklists
- policy checks
- audit sampling
- exception queues
- rollback or correction paths
- periodic review

## 6. Measure outcomes

Measure both efficiency and control. Without the second half, the first half eats the process:

- cycle time
- rework
- escalation rate
- approval quality
- evidence completeness
- exception rate
- policy breaches
- user or citizen satisfaction
- cost-to-serve
- audit findings

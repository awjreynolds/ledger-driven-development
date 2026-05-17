# GitHub Projection Report

## Disposable Issues

- PRD projection: https://github.com/awjreynolds/gadd/issues/12
- CAD SDD projection: https://github.com/awjreynolds/gadd/issues/13
- Render SDD projection: https://github.com/awjreynolds/gadd/issues/14

## Result

- Created all three issues with `gh issue create`.
- Attached both SDD issues as native GitHub sub-issues under the PRD issue with
  `POST /repos/awjreynolds/gadd/issues/12/sub_issues`.
- Verified the PRD issue reported `sub_issues_summary.total: 2`.
- Closed both child issues.
- Verified the PRD issue reported `sub_issues_summary.completed: 2` and
  `percent_completed: 100`.
- Closed the PRD issue.

No GitHub token material was stored in this repository.

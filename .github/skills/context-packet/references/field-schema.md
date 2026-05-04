# Context Packet Field Schema

Use this schema when deciding whether a context packet is ready to become a
GitHub issue.

## Blocking Fields

These fields must be present before issue creation. Blank values, `TBD`,
`TODO`, `see above`, `unknown`, and `not sure` do not satisfy blocking fields.

| Field | Purpose | Validation | Issue mapping |
|---|---|---|---|
| `target_repo` | Repository where the issue will be created | `owner/repo` form | Tool owner and repo |
| `title` | One-line task summary | Specific, action-oriented, 10-80 characters | Issue title |
| `work_type` | Classifies the work | feature, bugfix, refactor, chore, docs, security, investigation | Label or body metadata |
| `desired_outcome` | User, business, or system result | Complete sentence with outcome and reason | Body |
| `scope_in` | What the implementer should do | At least one concrete item | Body |
| `scope_out` | Adjacent work excluded from this issue | At least one concrete exclusion | Body |
| `proof_of_done` | Verifiable acceptance criteria | At least two pass/fail criteria | Body checklist |
| `dependencies_affected` | Systems, services, teams, APIs, data, or dependencies | Explicit list; `None identified` is valid | Body |
| `risks` | Known risks and mitigations | Risk plus mitigation; `None identified` is valid only when intentional | Body and risk tier |
| `roll_forward_path` | Recovery or containment path | Actionable sentence, not just "revert" | Body |
| `ownership` | Human owner for review and risk | Named person, team, or GitHub username | Body and optional assignee |
| `risk_tier` | Review depth routing | low, medium, or high | Label or body metadata |

## Strongly Recommended Fields

Warn when these fields are missing, but do not block creation unless the task is
high-risk.

| Field | Purpose | Default |
|---|---|---|
| `handoff_evidence` | Evidence required in PR or handoff | Standard evidence checklist |
| `domain_context` | Business rules and vocabulary | `Not provided` |
| `architecture_refs` | ADRs, diagrams, specs, or design docs | `Not provided` |
| `repo_context` | Files, modules, APIs, commands, or systems | `Not provided` |
| `test_context` | Existing tests and validation commands | `Not provided` |
| `agent_suitability` | Whether the task is bounded enough for an agent | Warn if unclear |

## Optional Fields

Use these when known:

- labels
- assignees
- milestone
- project
- issue type
- related issues
- feature flag
- telemetry signals
- estimated complexity
- open questions
- duplicate or parent issue links

## Quality Heuristics

Flag weak values:

- Title is a generic noun such as `bug`, `issue`, `task`, or `fix`.
- Desired outcome describes only an implementation, not the result.
- Scope says "everything" or "do whatever is needed".
- Out of scope says only "don't break anything".
- Acceptance criteria say "works correctly" or "looks good".
- Risks say only "low risk" without rationale.
- Recovery says only "revert the PR".
- References say "see the docs", "previous PR", or "the logs" without a link,
  path, or issue number.

## Recommended Review Message

When validation fails, report all failures together:

```text
The packet is close, but I should not create the issue yet. These blocking
fields need more detail:

1. Proof of done - add at least two testable acceptance criteria.
2. Roll-forward path - describe how to recover if this causes trouble.
3. Owner - name the human who owns review risk.
```

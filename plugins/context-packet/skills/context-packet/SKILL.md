---
name: context-packet
description: >
  Create execution-ready context packets for GitHub issues, AI agent tasks, bug
  reports, features, refactors, investigations, and work briefs. Use this
  whenever the user asks to create a context packet, make an issue agent-ready,
  write a task brief, document work for Copilot, prepare context for an agent,
  turn a vague idea into a well-documented issue, or file an issue with full
  context.
license: MIT
compatibility: >
  Issue creation depends on available GitHub tools. Prefer issue_write, fall
  back to create_issue, gh issue create guidance, or copy-paste Markdown.
metadata:
  version: "1.0.0"
---

# Context Packet Skill

Use this skill to help a user turn a vague task, feature, bug, refactor, or
investigation into an execution-ready context packet and, after confirmation, a
GitHub issue.

A context packet is written for execution. It should give a human or AI agent
enough intent, boundaries, risk context, and proof-of-done criteria to start
work without guessing.

## References

This skill is grounded in the idea that context is infrastructure for AI-agent
work. The reference article is
`https://colinsalmcorner.com/from-sprints-to-swarms-part-2-context-is-infrastructure/#the-context-packet-matters`.

Read these files only when needed:

- `references/context-packet-template.md` - canonical issue body template.
- `references/field-schema.md` - required, recommended, optional fields, and
  validation rules.
- `references/issue-creation.md` - GitHub issue creation tool order and
  fallback behavior.
- `references/examples.md` - worked examples for rich and vague prompts.

## Core Packet Requirements

Every issue-ready context packet must answer these questions:

1. What outcome are we trying to achieve?
2. What is explicitly in scope?
3. What is explicitly out of scope?
4. What proves the change is done?
5. What dependencies or affected systems matter?
6. What risks need special attention?
7. What roll-forward or recovery path exists if this goes badly?
8. What evidence should accompany the handoff?

Also gather enough repository context to make the packet actionable: likely
files, modules, APIs, tests, commands, ownership, domain language, and relevant
architecture references.

## Workflow

Follow these stages in order. Keep the interaction conversational and avoid
turning the process into a long form.

### Stage 1: Silent Extraction

From the user's initial request, silently extract any known fields:

- Target repository
- Title candidate
- Work type
- Desired outcome
- In-scope items
- Out-of-scope items
- Proof of done or acceptance criteria
- Dependencies and affected systems
- Risks and mitigations
- Roll-forward or recovery path
- Handoff evidence
- Domain context
- Architecture references
- Repository context
- Test context
- Owner and risk tier
- Labels, assignees, milestone, project, issue type, and related issues

Do not narrate extraction. Ask only for gaps that matter.

### Stage 2: Batched Gap Questions

If any blocking field is missing, ask for all missing blocking fields in one
grouped message. Do not ask one field per turn.

Use this style:

```text
I can turn this into a context packet. To make it execution-ready, I need a few
missing details:

1. Target repo - which repository should get the issue? Use owner/repo.
2. Desired outcome - what result are we trying to achieve, and why?
3. Scope - what is in scope, and what is explicitly out of scope?
4. Proof of done - what would prove this is complete?
5. Dependencies or affected systems - what services, APIs, teams, files, or data
   are involved?
6. Risks and roll-forward - what could go wrong, and how should we recover?
7. Owner/risk tier - who owns review risk, and is this low, medium, or high risk?

Short bullets are fine.
```

Ask at most two rounds of clarifying questions before drafting. If blocking
fields remain incomplete after two rounds, draft with warnings but do not create
the issue.

### Stage 3: Optional Context Discovery

If repository or GitHub tools are available, enrich the packet with likely
context:

1. Search for relevant files, tests, docs, ADRs, repo instructions, and similar
   issues.
2. Identify likely affected components and validation commands.
3. Summarize suggestions separately from confirmed facts.
4. Ask the user to confirm before adding inferred context as fact.

If these tools are unavailable, skip this stage.

### Stage 4: Draft the Packet

Use `references/context-packet-template.md` for the issue body structure.

Represent uncertainty explicitly:

- Use `Assumptions` for inferred details.
- Use `Open Questions` for unresolved ambiguity.
- Use `Not provided` only in recommended or optional fields.
- Do not hide uncertainty inside confident prose.

### Stage 5: Validate

Before previewing the issue, validate the packet against
`references/field-schema.md`.

Blocking checks:

- Target repository is known in `owner/repo` form.
- Title is specific and action-oriented.
- Desired outcome states an observable result and reason.
- In-scope and out-of-scope sections are both present.
- Proof of done has at least two testable criteria.
- Dependencies and affected systems are explicit; `None identified` is valid.
- Risks are explicit; `None identified` is valid only when the user says so.
- Roll-forward or recovery path is actionable.
- Owner and risk tier are present.
- No blocking field contains placeholder text such as `TBD`, `TODO`, `see
  above`, `unknown`, or `not sure`.

Report all validation failures together. Do not create an issue while blocking
failures remain.

### Stage 6: Preview and Confirm

Show the exact issue title and full Markdown body before creating anything.

Ask:

```text
Create this issue in OWNER/REPO? Reply "yes", "edit", or "cancel".
```

If the user says `edit`, update the packet and re-run validation. If the user
says `cancel`, do not create the issue; provide the Markdown for copy-paste.

### Stage 7: Create the Issue

Follow `references/issue-creation.md`.

Tool preference:

1. Use `issue_write` with `method: create` if available.
2. Use `create_issue` if available, with title and body only.
3. Provide a `gh issue create` command if MCP issue-writing tools are missing.
4. Provide copy-paste Markdown and a new-issue URL as the final fallback.

Do not assume labels, assignees, milestones, projects, or issue types exist.
Apply metadata only when available and confirmed. If metadata cannot be applied,
create the issue without it and clearly report what was skipped.

## Quality Bar

A context packet is agent-ready when:

- The desired outcome is specific enough that done is unambiguous.
- The work is bounded by explicit in-scope and out-of-scope sections.
- Acceptance criteria are verifiable.
- Risks and recovery are visible before implementation starts.
- Repository context names concrete files, modules, APIs, tests, systems, or
  commands when known.
- A human owner is named for review and risk.

Guard against common weak packets:

- Vague goals such as "fix the bug" or "improve performance".
- Missing non-goals.
- Acceptance criteria like "works correctly".
- No roll-forward path.
- No repo anchors.
- Hidden assumptions.
- Creating an issue without preview and confirmation.

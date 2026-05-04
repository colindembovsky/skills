# Issue Creation Guidance

Create a GitHub issue only after the user has reviewed the full issue preview
and explicitly confirmed creation.

## Tool Order

Prefer this order:

1. `issue_write` with `method: create`
2. `create_issue`
3. `gh issue create`
4. Copy-paste Markdown and a new-issue URL

## MCP `issue_write`

Use this when metadata matters and the tool is available.

Required fields:

- `method: create`
- `owner`
- `repo`

Recommended fields:

- `title`
- `body`
- `labels`, only after confirming they exist
- `assignees`, only after confirming they are valid collaborators
- `milestone`, only after resolving the milestone number
- `type`, only after confirming issue types exist for the organization

## MCP `create_issue`

Use this when `issue_write` is not available.

Required fields:

- `owner`
- `repo`
- `title`

Optional field:

- `body`

This tool does not support labels, assignees, milestones, projects, or issue
types. If metadata is important, create the issue first and then update it with
another available tool, or tell the user which metadata was skipped.

## GitHub CLI Fallback

If MCP issue-writing tools are unavailable, provide this command:

```bash
gh issue create \
  --repo "OWNER/REPO" \
  --title "ISSUE TITLE" \
  --body-file "context-packet.md"
```

If the user wants browser preview instead of direct creation:

```bash
gh issue create \
  --repo "OWNER/REPO" \
  --title "ISSUE TITLE" \
  --body-file "context-packet.md" \
  --web
```

Do not pass labels, assignees, or milestones unless they are known to exist and
the user has asked for them.

## Failure Handling

| Situation | Response |
|---|---|
| Missing repo | Ask for `owner/repo`; do not create issue |
| 403 forbidden | Explain that write access or token scope is missing and provide draft Markdown |
| 404 not found | Ask the user to check repo spelling or access |
| 410 gone | Explain that issues are disabled and offer a copy-paste fallback |
| 422 validation | Report the likely invalid field and preserve the draft |
| User cancels | Do not create issue; provide the draft Markdown |

## Success Message

After creation, include:

- Issue URL
- Issue number when available
- Metadata applied
- Metadata skipped and why

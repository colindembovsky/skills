# Context Packet Examples

## Example 1: Rich Initial Prompt

User:

```text
Create a context packet for acme/storefront. Checkout crashes with a
NullPointerException in CartService.java when the user has an empty cart and
applies a promo code. Expected: validation error. Actual: 500. In scope: fix
empty-cart promo handling and add tests. Out of scope: changing promo rules or
checkout redesign. Risk: shared checkout path. Owner: @checkout-lead. Risk tier:
medium.
```

Expected behavior:

- Extract most blocking fields without asking.
- Ask only for missing proof-of-done detail and roll-forward path.
- Draft an issue with concrete scope, risks, and acceptance criteria.
- Preview the issue before creating it.

## Example 2: Vague Prompt Improved by Batched Questions

User:

```text
Something is broken with login. Make an issue for Copilot.
```

Good response:

```text
I can turn this into a context packet. To make it execution-ready, I need a few
missing details:

1. Target repo - which repository should get the issue? Use owner/repo.
2. Desired outcome - what should login do when this is fixed?
3. Scope - what login flow is in scope, and what should not be changed?
4. Proof of done - what would prove this is complete?
5. Dependencies or affected systems - SSO, auth service, identity provider,
   frontend, backend, or data?
6. Risks and roll-forward - what could go wrong, and how should we recover?
7. Owner/risk tier - who owns review risk, and is this low, medium, or high risk?

Short bullets are fine.
```

Expected behavior:

- Do not create an issue from the vague prompt.
- Ask grouped questions instead of one-at-a-time questions.
- Preserve any user-provided details verbatim, especially errors or logs.

## Example 3: Refactor Request

User:

```text
Write a task brief for refactoring the billing worker retry code. It is spread
across worker.py and retry_policy.py. I want it easier to test.
```

Expected behavior:

- Treat it as a context packet request even though the phrase "context packet"
  is absent.
- Ask for explicit non-goals because refactors are prone to scope creep.
- Ask for proof of done beyond "easier to test".
- Ask for risk and recovery because billing workers can affect money movement.

## Example 4: User Only Wants Markdown

User:

```text
Draft the packet but do not create the GitHub issue yet.
```

Expected behavior:

- Create the packet as Markdown.
- Run validation and flag missing blocking fields.
- Do not call issue-writing tools.
- Provide a ready-to-paste issue body when the user is satisfied.

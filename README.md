# Context Packet Skill

This repository contains the `context-packet` skill for turning vague ideas,
bug reports, feature requests, refactors, investigations, and work briefs into
execution-ready GitHub issue context.

The skill is based on the principle that context is infrastructure for effective
AI-agent work. For the motivation behind context packets, see
[The Context Packet Matters](https://colinsalmcorner.com/from-sprints-to-swarms-part-2-context-is-infrastructure/#the-context-packet-matters)
in my "From Sprints to Swarms" series.

## What the skill does

`context-packet` helps a user produce a bounded, reviewable task brief with:

- a desired outcome
- in-scope and out-of-scope boundaries
- proof-of-done acceptance criteria
- affected systems and dependencies
- risks, mitigations, and recovery guidance
- handoff evidence expected from the implementer
- repository, architecture, and validation context when available

The skill can draft Markdown only, or after user preview and confirmation, guide
creation of a GitHub issue.

## Repository layout

```text
plugins/
  context-packet/
    .github/
      plugin/
        plugin.json
    skills/
      context-packet/
        SKILL.md
        references/
        evals/
    README.md
.github/
  extensions/
    context-packet/
      extension.mjs
scripts/
  package-context-packet-skill.py
dist/
  context-packet.skill
```

`plugins/context-packet/.github/plugin/plugin.json` is the plugin manifest used
by plugin-aware installers. `SKILL.md` contains the trigger metadata and runtime
instructions. The `references/` files hold the canonical packet template, field
schema, issue creation guidance, and examples. The project extension exposes the
`context_packet_skill_info` smoke-test tool so the Copilot CLI extension loader
can be verified from this repository.

## Skill format

The skill follows the expected directory format:

```text
context-packet/
  SKILL.md
  references/
  evals/
```

`SKILL.md` starts with YAML frontmatter and includes the required `name` and
`description` fields. The name is `context-packet`, matching the skill directory,
and the body uses progressive disclosure by pointing to reference files instead
of loading every detail at once.

## Packaging and validation

Package the skill with:

```bash
python3 scripts/package-context-packet-skill.py
```

The packaging script validates the frontmatter, excludes local-only eval files
and `.DS_Store` files, and writes:

```text
dist/context-packet.skill
```

Inspect the package contents with:

```bash
unzip -l dist/context-packet.skill
```

## Publishing a release

Pushing any Git tag runs `.github/workflows/publish-skill.yml`. The workflow
packages the skill, verifies `dist/context-packet.skill`, and publishes that
file as an asset on a GitHub Release for the tag.

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Installing as a plugin

Install directly with GitHub CLI:

```bash
gh skill install colindembovsky/skills context-packet
```

Preview before installing:

```bash
gh skill preview colindembovsky/skills context-packet
```

Pin a specific version:

```bash
gh skill install colindembovsky/skills context-packet@v0.1.1
```

You can also distribute the skill by sharing the packaged `.skill` artifact from
the latest GitHub Release:

```text
https://github.com/colindembovsky/skills/releases/latest
```

Users should download `context-packet.skill` from the release assets and import
or install that file in their skill-compatible AI agent or plugin manager. The
`.skill` file is the portable plugin package; this repository is the source used
to build it.

The project extension in `.github/extensions/context-packet/extension.mjs` is
only for Copilot CLI smoke testing in this repository. It is not required for
users who install with `gh skill` or the packaged `context-packet.skill` plugin.

## Extension smoke test

Copilot CLI project extensions are discovered from:

```text
.github/extensions/<extension-name>/extension.mjs
```

This repository includes `.github/extensions/context-packet/extension.mjs`.
Reload extensions after editing it:

```text
extensions_reload({})
```

Then verify it is loaded:

```text
extensions_manage({ operation: "list" })
extensions_manage({ operation: "inspect", name: "context-packet" })
```

The extension registers `context_packet_skill_info`, which reports the local
skill path, package artifact path, reference URL, and frontmatter validation
details.

## Example prompts

```text
Create a context packet for adding rate-limit headers to the search API.
```

```text
Something is broken with login. Make an issue for Copilot.
```

```text
Write a task brief for refactoring the billing worker retry code. I want it
easier to test, but do not change billing semantics.
```

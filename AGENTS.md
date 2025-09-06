# CI: pass pre-commit gate before committing

## One-time setup
- Sync dependencies (uv):
  - `uv sync`
- Install the git hook:
  - `uv run pre-commit install` (or `pre-commit install` if pre-commit is on PATH)

## Before every commit (from repo root)
1) Auto-format fast path (optional, speeds things up)
- `uv run ruff format .`

2) Run all hooks and apply fixes
- `uv run pre-commit run --all-files`
- If it reports “files were modified by this hook”:
  - `git add -A`
  - `uv run pre-commit run --all-files`
- Repeat until pre-commit finishes with no modifications.

3) Commit
- `git commit -m "…"`

---

# Before implementing a function: fetch fresh context with MCP tool `context7`

Always gather up-to-date docs before writing new code or using a new API.

## What to fetch with `context7`
- Package/API docs for every third‑party dependency you plan to call.
- Latest Python 3.12 syntax and typing features relevant to the change.

## How to use `context7`
- Invoke the MCP tool with clear, targeted queries and ask for official sources and version info.
- Example invocations (adapt to your client’s syntax):
  - `context7: docs package=requests topics=install,quickstart,api,examples`
  - `context7: python version=3.12 topic=typing changes summary for "<task>"`
  - `context7: python version=3.12 topic="pattern matching" examples minimal`

## Apply the results
- Prefer APIs shown as current/stable in the fetched docs.
- Conform examples to Python 3.12 syntax.
- If results conflict, choose the latest stable and note the source in the PR description.

## If `context7` is unavailable
- Retry once. If still unavailable, proceed only with well‑established APIs and add a PR note to re‑verify with `context7`.

---

# Comment policy: never use “TODO”

- Do not introduce “TODO” (or variants like “TO DO”, “ToDo”, “@todo”) anywhere:
  - Not in code comments, docstrings, notebooks, or commit messages.
- If follow‑up work is needed:
  - Open a GitHub issue and reference it without using the word “TODO”.
  - Preferred format in code/comments: `NOTE: see issue #123 for follow‑up rationale` or `FOLLOW‑UP: see issue #123`.

Quick self-check before committing:
- Search and remove any occurrences: `git grep -n -E '\bT[O0]\s?DO\b|@todo' || true`
- Then run: `uv run ruff format . && uv run pre-commit run --all-files`

---
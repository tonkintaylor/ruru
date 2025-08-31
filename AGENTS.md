# AGENTS.md

# CI: pass pre-commit gate before committing

The last CI failure was caused by ruff-format modifying files (“files were modified by this hook”), which makes pre-commit exit with code 1. Run the hooks locally until they make no changes, then commit.

## One-time setup

- Sync dependencies (uv):
  - `uv sync`
- Install the git hook:
  - `uvx pre-commit install` (or `pre-commit install` if pre-commit is on PATH)

## Before every commit (from repo root)

1) Auto-format fast path (optional, speeds things up)
- `uvx ruff format .`

2) Run all hooks and apply fixes
- `uvx pre-commit run --all-files`
- If it reports “files were modified by this hook”:
  - `git add -A`
  - `uvx pre-commit run --all-files`
- Repeat until pre-commit finishes with no modifications.

3) Commit
- `git commit -m "…"`

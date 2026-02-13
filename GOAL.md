Goal
Build a `hyperlink_button` Streamlit element that has exactly the same API and behavior as `st.button`, but renders as a typical hoverable hyperlink.

Context
Streamlit has `st.link_button` (looks like a button, behaves like a link). There is no built-in interactive element that looks and behaves like a hyperlink but functions like a button. This project provides a clean, testable, publishable component to fill that gap. The repo contains `st_docs/` (Streamlit docs mirror) and it must be used for research.

Non-negotiable constraints
- ALL WORK MUST BE DONE AND TESTED IN A DOCKER CONTAINER.
  - Host commands are permitted only to orchestrate Docker (build/run/logs/cp).
  - Do not run `uv`, `python`, `pytest`, `npm`, etc. on the host.
- Use `uv` and Python 3.13 for development.
- Use the most recent versions of libraries; never manually type/pin versions; rely on CLI workflows (e.g. `uv add`).
- Only use Docker for runtime checks; run and inspect the app inside the container.

Deliverables
- Python library ready for PyPI.
- A simple example app in-repo.
- Automated tests (unit + integration) including Streamlit widget testing.
- Headless browser verification of rendered output.
- Documentation, including an exhaustive PyPI release manual.

Orchestrator delegates work, verifies and integrates.

Delegation primitives (tooling reality)
- `opencode-subagent` skill (preferred): async, resumable sessions; use for any task that may require iteration.
- `task` (avoid at orchestrator level): one-off, non-resumable; use only for quick exploration. Subagents may spawn short-lived `task` agents as needed.

Tool availability (critical)
- Tool parity: subagents have exactly the same tools as the orchestrator, including file editing via `apply_patch` and command execution via `bash`.
- Subagents MUST produce real patches (use `apply_patch`) rather than only describing changes.
- If any agent claims it cannot edit files or lacks tool access, treat it as a mistake: correct it and require it to use `apply_patch`.

Models available to `opencode-subagent`:
- `azure/gpt-5-nano`: cheap, low capability
- `azure/gpt-5-mini`: default workhorse
- `azure/gpt-5.2-codex`: expensive, best for hard integration/debugging

Model variants:
- `medium` (default)
- `high` (for difficult integration/debugging or for cheaper models)

Default usage:
- Start with `azure/gpt-5-mini` + `medium` for most implementation work.
- Use `azure/gpt-5-nano` for reconnaissance, doc reading, and mechanical tasks.
- Escalate to `azure/gpt-5.2-codex` and/or `high` only after a clear roadblock (repeat failures, subtle Streamlit/component protocol issues, flaky E2E).

Orchestrator edit policy (bounded authority)
- Default: orchestrator does not change implementation code.
- Allowed orchestrator edits:
  - Steering/governance docs (e.g. `AGENTS.md`, this file).
  - Mechanical integration glue (conflict resolution, wiring, renames) when necessary.
- Any non-mechanical implementation change must be delegated as a work order to a subagent.

Work-order discipline (prevents overlap + bloat)
- Every subagent task must be issued as a work order with:
  - Objective (one sentence)
  - Allowed paths (explicit allowlist)
  - Forbidden paths (explicit denylist)
  - Acceptance criteria (observable outcomes)
  - Docker-only verification commands
  - Model + variant
- Require a handoff packet from subagents:
  - changed paths
  - why (not a dump of code)
  - verification performed + where logs/artifacts are
  - known limitations + follow-ups

Coordination and overlap control (avoid integration traps)
- Do not run overlapping work orders that touch the same files.
- Treat these as shared/locked files by default (only one active work order may touch at a time):
  - `pyproject.toml`
  - lockfiles
  - Dockerfiles
  - `AGENTS.md`

Verification requirements
- Tests must run in Docker.
- Use unit + integration tests.
- Use Streamlit's widget testing where applicable.
- Use headless browsing to verify Streamlit render output.
- Prefer delegating verification to a dedicated verifier subagent, but require evidence (logs/artifacts) either way.

Ambiguity handling (don't interrupt mid-flight)
- Proceed with reasonable defaults when requirements are ambiguous.
- Track assumptions/decisions in separate docs (e.g. `ASSUMPTIONS.md` / `DECISIONS.md`).
- Only ask the user when blocked or the choice materially changes architecture/security/publishability.

-----------------------------------------------------------------------------

STEP 0 (check-in before autonomous execution)
- Verify Docker availability via CLI.
- Raise concerns if the request appears non-viable.
- Ask only blocking questions.
- Create/refresh `AGENTS.md` for subagents.
- Confirm tool parity in practice (especially that subagents can use `apply_patch`).

REITERATING: STEP 0 IS A CHECK-IN WITH THE USER BEFORE KICKING OFF AUTONOMOUS WORK.

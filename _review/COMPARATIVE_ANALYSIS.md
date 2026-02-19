# Final Comparative Report: `hyperlink_button` Autonomous Experiments (Attempts 1-6)

## 0) Problem statement and experiment design

### Problem statement

This experiment series evaluates how well long-horizon autonomous agents can deliver a production-ready Streamlit component under strict process constraints.

Target artifact:
- Build a `hyperlink_button` component with `st.button`-compatible API/behavior, but hyperlink-like visual presentation.

Delivery constraints repeatedly used across attempts:
- Work autonomously with minimal user interruption.
- Prefer delegation/subagent orchestration over single-thread execution.
- Run validation in Docker and use `uv` + Python 3.13.
- Provide tests (unit + browser/e2e), docs, packaging, and PyPI release readiness.

### What was varied across attempts

The six attempts intentionally varied execution strategy and control policies:
- Orchestrator model choice and model-tier routing.
- Delegation architecture (`opencode-subagent`, `task` subagents, or none).
- Strictness and practical enforcement of Docker-only and delegate-first mandates.
- Orchestration style (parallel decomposition vs serial debugging).

### Evaluation objective

The goal of this report is not only to compare output quality, but to identify repeatable success/failure patterns for future long-horizon agent and subagent orchestration experiments.

Confidence convention used in this report:
- `Confirmed`: directly supported by branch artifacts/review evidence.
- `Hypothesis`: inferred recommendation or heuristic requiring validation in future runs.

## 1) Executive summary

This six-attempt series shows a clear pattern: outcome quality is driven less by how many subagents are launched and more by whether orchestration is bounded by hard architectural and milestone gates. The strongest functional runs were attempt 1 and attempt 3, which both produced full component-style implementations with tests and docs. Attempt 3 delivered the highest overall quality but at higher cost. Attempt 1 delivered the best cost-to-quality value but retained a major click-state defect and weaker Docker mandate compliance.

Attempts 4 and 6 illustrate architecture drift under operational pressure. Both delivered working packages with verification artifacts, but they converged toward CSS/DOM wrappers around `st.button` instead of robust custom-component architecture expected by planning documents and review standards. Attempt 5 demonstrates the cost risk of single-thread debugging without delegation or stop-loss controls: token spend and wall-clock time escalated while convergence remained weak. Attempt 2 shows the opposite failure mode: orchestration scaffolding and delegation setup succeeded, but delivery halted early due to autonomy/confirmation conflicts.

The most actionable conclusion is that strict process prose alone is insufficient. “Delegate-first,” “Docker-only,” and “no self-edit” constraints must be machine-checkable and tied to acceptance gates, or they are bypassed or create deadlocks. The best next strategy is a gated, budget-aware orchestration protocol that combines attempt-3’s architecture quality with attempt-1’s value efficiency: fewer but better-scoped subagents, explicit model-tier routing, stop-losses for polling/debug loops, and a parity checklist mapped to `st.button` semantics before declaring success.

## 2) Experiment overview and variable matrix

### Scope and comparison method

This synthesis combines per-attempt deep dives (`_review/evidence/attempt-1-deep-dive.md` through `_review/evidence/attempt-6-deep-dive.md`) and three cross-cut analyses (`_review/evidence/crosscut-orchestration.md`, `_review/evidence/crosscut-cost-quality.md`, `_review/evidence/crosscut-failure-taxonomy.md`). Where metrics disagree slightly across files, values from the deep dives/cross-cut tables are prioritized as comparative baselines.

Confidence labeling used in this report:
- `Confirmed` means directly supported by evidence files.
- `Hypothesis` means inferred for synthesis or prioritization and should be validated in future runs.

### Variable matrix (design factors vs outcomes)

| Attempt | Orchestrator Model | Delegation Architecture | Docker Constraint Behavior | Delivered Architecture | Outcome Class | Cost | Duration | Leverage | Cache Pressure |
|---|---|---|---|---|---|---:|---|---:|---:|
| 1 | GPT-5.2-High | Early broad subagent fan-out (`opencode-subagent`) | Partial compliance; Docker mandate drift | Proper component frontend + Python wrapper | Success with major defect | $4.32 | ~2h | 2.45x | 8.5x |
| 2 | GPT-5.2-Codex | Delegation-heavy scaffolding, low delivery throughput | Setup-compliant but no full implementation/testing | No core component delivered | Failed early stop | $0.75 | short | N/A | 2.0x |
| 3 | GPT-5.2-High | Strong multi-subagent implementation pipeline | Mixed compliance; some drift | Proper component frontend + wrapper | Best functional success | $8.97 | ~2h | 2.79x | 4.5x |
| 4 | GPT-5.2 | Light `task` delegation, orchestrator-heavy coding | Strong practical Docker compliance | CSS/DOM wrapper around `st.button` | Partial (architecture miss) | $5.32 | ~1h40m | 0.41x | 1.7x |
| 5 | GPT-5.2-High | Single thread (no subagents) | Strong adherence, poor convergence | Frontend exists but parity shallow, routing/debug instability | Partial/incomplete | $11.22 | hours | ~0x | 28.0x |
| 6 | GPT-5.2-High | Many subagents with high coordination overhead | High formal/practical compliance | CSS/DOM wrapper path (architecture drift) | Partial (high overhead) | $15.43 | ~15h | 1.79x | 15.3x |

Interpretation:
- Good delegation architecture correlates with better quality only when integration cadence is strong (attempts 1, 3).
- Strict Docker/process constraints do not independently predict quality (attempts 4, 5, 6).
- High cache pressure strongly correlates with runaway cost/time (attempts 5, 6).
- Hypothesis: a practical “safe zone” is `cache_ratio <= 5x` plus leverage `>= 2x`, based on these six runs.

## 3) Condensed per-attempt summaries (1-6)

### Attempt 1

Attempt 1 is a high-value baseline with strong artifact completeness: Python wrapper, React frontend, tests (including Playwright/e2e), docs, packaging, and demo app were all produced in one autonomous run. It handled early orchestration prompt-mangling issues and path friction (`st_docs` permissions/symlink portability) through quick correction loops. The key positive was productive parallel decomposition early in the run and good integration throughput afterward.

Its primary weakness is correctness robustness: a major click-state bug is documented where click events can be missed due to remount/reset interactions with monotonic state handling. Docker was requested as mandatory sandbox execution but not consistently enforced in practice. There is also evidence that delegation discipline degraded mid-run, with orchestrator self-implementation rising despite delegate-first guidance.

Net assessment: very good cost/quality profile and a useful orchestration blueprint, but with one release-blocking behavior defect and policy fidelity gaps.

### Attempt 2

Attempt 2 demonstrates orchestration capability without delivery. It successfully created governance and infrastructure artifacts (`AGENTS.md`, Docker scaffolding) and used resumable subagent mechanisms, including parallel tasks for survey and setup. Tooling telemetry and status tracking were operationally clean.

However, execution stalled before core implementation. The run sought user confirmation early and ended with “can proceed” style messaging despite autonomy directives to complete end-to-end unless genuinely blocked. No functional component, no full test matrix, and no package-level product readiness were achieved.

Net assessment: low absolute cost but poor objective completion, making this a classic “delegation theater” case where coordination actions are mistaken for progress. It is a useful negative control proving that delegation infrastructure alone does not produce outcomes.

### Attempt 3

Attempt 3 is the highest-quality run in this dataset. It delivered a proper component architecture, robust wrapper semantics, meaningful tests (unit, widget/fallback, e2e), and practical documentation/release guidance. It also showed strong decomposition and productive parallel subagent usage. Leverage was highest (`2.79x`), and quality evidence is materially stronger than attempts 4-6.

Problems were mostly governance and efficiency rather than pure correctness. There were policy breaches where orchestrator self-edited despite explicit anti-self-patch instructions. E2E and packaging paths required remediation cycles (build include paths, e2e retries), indicating preflight risk controls were insufficient. Docker-only discipline was not perfectly strict.

Net assessment: best functional template for future experiments, but should be wrapped with stronger policy enforcement and budget/loop controls.

### Attempt 4

Attempt 4 is operationally disciplined in Docker execution and verification, with passing tests/build flows and coherent package/docs delivery. It performs well on reproducibility and process evidence. Cost and duration are moderate.

Its core limitation is architecture quality relative to requirement intent. The implementation converged to scoped CSS injection around native `st.button` instead of a robust custom frontend component path. This passes short-term behavior checks but increases long-term fragility due to Streamlit DOM/testid coupling and selector assumptions. Delegation leverage was very low (`0.41x`), indicating that orchestrator did most substantive work despite delegate-first framing.

Net assessment: a reproducible partial success that under-delivers architectural fidelity and delegation economics.

### Attempt 5

Attempt 5 highlights runaway overhead in single-thread execution. It retained Docker/tooling discipline and produced artifacts (frontend tree, tests, docs), but repeated debugging loops around component routing/404 and Playwright readiness dominated the run. Operational friction included command errors, port/process churn, container package remediation, and repeated health-vs-route mismatch investigations.

No subagent delegation was used, and cache pressure was extreme (`28.0x`), with high total spend and weak convergence. API/behavior parity with `st.button` remained shallow, with accepted parameters not fully reflected in behavior and limited test depth for parity-critical semantics.

Net assessment: expensive partial/incomplete outcome and strong evidence that single-thread high-tier orchestration is the least efficient strategy for this task class.

### Attempt 6

Attempt 6 is the most exhaustive endurance run: broad artifact coverage, many subagents, comprehensive docs/specs, and layered testing. It demonstrates persistence and process scaffolding maturity.

But efficiency and architectural fidelity are poor. Coordination loops (poll/wait/cancel/retry) consumed substantial time and tokens. Multiple subagent stalls and cancellations occurred. Despite planning docs favoring custom component architecture, delivered implementation again drifted to CSS/DOM wrapper strategy. Cost and duration were highest in the series, and cache pressure remained severe (`15.3x`; orchestrator cache-bloat metrics even higher in review-specific analysis).

Net assessment: good as a stress-test of autonomous orchestration, weak as a model for cost-effective “build the right thing” delivery.

## 4) Cross-cutting findings

### Orchestration architecture

The strongest orchestration pattern is “decompose early, integrate quickly, gate often.” Attempts 1 and 3 used early parallel tracks for research, implementation slices, tests, and packaging, then converged through integration. Their outcomes materially outperformed attempts dominated by either under-delegation (attempt 5) or over-coordination without integration cadence (attempt 2, attempt 6).

Two recurring architecture failures:
- Control-loop bloat: repeated status polling and coordination chatter without artifact movement.
- Governance drift: delegate-first policies not enforced when pressure rises.

Hypothesis: The orchestrator tends to optimize local certainty (more checks, more polling) rather than global throughput when no stop-loss exists. This likely explains why high-process runs can become high-cost/low-yield despite good intentions.

### Cost-quality tradeoffs

Attempt 3 maximized quality; attempt 1 maximized value density. Attempts 5 and 6 are dominated outcomes, where higher spending did not yield correspondingly better quality. Cache pressure is the most consistent early warning signal of economic failure.

Practical tradeoff rules from evidence:
- Higher model tier can improve coding throughput when tightly scoped (attempt 3).
- High-tier orchestrator without delegation or controls burns budget (attempt 5).
- Mixed-tier routing only helps when orchestration thread length is bounded (attempt 6 shows limits).

Hypothesis: For this repository/task, expected good runs should target total tokens under ~10M and cache ratio below ~5x while preserving full parity gates.

### Failure mode taxonomy

The crosscut taxonomy is stable across sources:
1. Mandate conflict paralysis (autonomy vs clarification).
2. Delegation theater (coordination without delivery).
3. Architecture downgrade under constraint pressure.
4. Verification asymmetry (tests pass but parity incomplete).
5. Cache-bloat/orchestration overhead spiral.

All five are directly evidenced in at least two attempts, with strongest signatures in attempts 2, 5, and 6. Notably, these are process-architecture failures first, not language-model raw capability failures.

### Constraint design effectiveness

Constraint prose was high quality but weakly enforceable. The same three constraints appeared repeatedly: Docker-only execution, delegate-first behavior, and no orchestrator self-edit except minor fixes. Yet compliance varied by attempt and did not reliably predict quality.

Why constraints underperformed:
- They were aspirational text, not checked gates.
- They sometimes conflicted (autonomy vs ask-questions behavior).
- They did not include convergence controls (maximum retries, polling caps, root-cause reset rules).

Hypothesis: Converting constraints to measurable checks would likely produce larger quality gains than further prompt wording refinements.

## 5) Success and failure patterns (ranked factors)

### Ranked success factors

1. Hard architecture and milestone gates tied to artifacts.
2. Early parallel decomposition with explicit merge checkpoints.
3. Delegation quality (task typing + integration cadence), not delegation volume.
4. Layered verification including parity semantics, not only smoke/e2e.
5. Model-tier specialization with bounded orchestrator thread growth.

### Ranked failure factors

1. Missing stop-loss controls for low-yield loops (poll/check/retry churn).
2. Architecture shortcuts accepted under schedule/constraint pressure (CSS wrapper drift).
3. Unenforced delegation policy leading to either paralysis (attempt 2) or drift (attempt 3).
4. High cache replay overhead in long monolithic threads.
5. Validation focused on “runs” rather than semantic parity completeness.

### Pattern synthesis

Success requires a dual discipline: technical architecture discipline and orchestration economics discipline. Teams/runs that had one without the other either shipped fragile implementations (attempts 4/6) or spent heavily without convergence (attempt 5). Runs that balanced both dimensions (attempt 3, partly attempt 1) achieved materially better outcomes.

Hypothesis: If a future run enforces component-architecture gate + parity checklist + cache stop-loss, it should outperform attempt 3 on cost while matching or exceeding quality.

## 6) Quantitative comparison dashboard (table)

| Attempt | Outcome | Architecture Fidelity | Tests Depth | Cost | Duration | Total Tokens | Input+Output | Cache Read | Cache Ratio | Leverage | Quality Score* |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Functional success, major click bug, Docker drift | High (proper component path) | High (unit + e2e + widget) | $4.32 | ~2h | 6.82M | 719.3K | 6.1M | 8.5x | 2.45x | 3.2 |
| 2 | Early stop, no core feature delivery | None | Minimal | $0.75 | short | 0.57M | 188.8K | 385.4K | 2.0x | N/A | 0.8 |
| 3 | Best overall functional delivery, governance drift | High | High | $8.97 | ~2h | 8.00M | 1.44M | 6.4M | 4.5x | 2.79x | 4.1 |
| 4 | Partial success, CSS workaround architecture | Medium-low | Medium (incl. e2e) | $5.32 | ~1h40m | 3.90M | 1.42M | 2.4M | 1.7x | 0.41x | 2.4 |
| 5 | Partial/incomplete, prolonged routing/debug loops | Medium-low | Low-medium | $11.22 | hours | 31.4M | 1.08M | 30.2M | 28.0x | ~0x | 1.4 |
| 6 | Broad deliverables, architecture drift, heavy overhead | Medium-low | High breadth, mixed stability | $15.43 | ~15h | 30.36M | 1.86M | 28.5M | 15.3x | 1.79x | 2.8 |

`*Quality Score` is a comparative synthesis metric from cross-cut evidence (0-5), not a directly logged repository field (hypothesis-level construct).

Key dashboard takeaways:
- Attempt 3 is quality leader.
- Attempt 1 is value leader.
- Attempts 5 and 6 are economically inefficient for delivered fidelity.
- Hypothesis: “Best next baseline” should hybridize attempt-3 architecture rigor with attempt-1 economic discipline.

## 7) Recommendations for next experiments

### Orchestration architecture

Use a milestone-gated architecture with evidence packets per gate:
1. Gate M1: component architecture proof (`frontend/src/*`, bridge wiring, minimal event roundtrip).
2. Gate M2: parity-critical unit/widget tests pass.
3. Gate M3: Dockerized e2e pass with deterministic environment checks.
4. Gate M4: packaging + release docs completeness.

Require each gate to include:
- Changed files list.
- Commands run with outcomes.
- Remaining risk statement.

No new parallel tracks are opened until current gate evidence is accepted automatically by script checks. Hypothesis: this will reduce attempt-6 style orchestration sprawl.

### Prompt and constraint engineering

Redesign constraints from prose to measurable rules:
- `delegate-first`: require a minimum subagent net token share target and cap orchestrator direct patch count.
- `docker-only`: require command transcript evidence from containerized runs.
- `no architecture shortcut`: fail if no component frontend artifacts exist unless explicit waiver is set.

Add anti-loop guardrails:
- Maximum repeated polling cycles per subagent.
- Maximum retries for same failing symptom before mandatory root-cause memo.
- Maximum message budget per gate before forced strategy switch.

This preserves autonomy while preventing attempt-2 paralysis and attempt-5/6 churn. [Confirmed + Assumption blend]

### Model selection strategy

Adopt explicit tier routing:
- Planning/research/log parsing: mini-tier.
- Implementation and hard bug fixes: codex-high tier.
- Orchestrator synthesis/merge decisions: high-tier but with strict token/message budget.

Track per-task model rationale in a short ledger:
- Task type.
- Model chosen.
- Expected cost band.
- Exit criteria.

Escalate to expensive models only after cheaper-tier failure with documented reason. Hypothesis: this should improve cost-quality ratio without reducing delivery confidence.

### Subagent coordination protocol

Use fewer, larger, artifact-owned subagents instead of many tiny specialists:
- `arch+api` owner.
- `frontend+integration` owner.
- `testing+qa` owner.
- `packaging+docs` owner.

Each subagent must return:
- Patch summary.
- Commands run.
- Explicit unresolved blockers.

Orchestrator does only merge/conflict/integration glue and decision-making. Any non-glue direct edits require logged exception reason.

### Monitoring and circuit breakers

Introduce live run metrics with hard stops:
- `cache_ratio` checkpoint every 20 messages.
- Message budget per gate.
- Time budget per gate.
- Progress heartbeat (“new artifact or passed test” required per interval).

Circuit breakers:
1. Stop when `cache_ratio > 10x` at two consecutive checkpoints.
2. Stop when no new artifact/test progress across 40 messages.
3. Stop when same failure signature occurs three times without hypothesis change.
4. Auto-cancel stalled subagents and reroute with narrowed prompts.

These controls directly target observed failure modes in attempts 5 and 6.

### 5 concrete experiment proposals

1. **Experiment A: Attempt-3 replica with hard gates**
- Objective: preserve quality baseline.
- Changes: add architecture gate + polling cap + cache stop-loss.
- Success criteria: quality score >= 4.1, cost <= $8.0, cache ratio <= 6x.

2. **Experiment B: Value-optimized hybrid (A1 economics + A3 architecture)**
- Objective: maximize quality per dollar.
- Changes: mini-tier for planning/tests, codex-high only for coding slices.
- Success criteria: quality score >= 3.9, cost <= $6.0, leverage >= 2.2x.

3. **Experiment C: Delegation-compliance stress test**
- Objective: validate measurable delegate-first controls.
- Changes: orchestrator direct patch cap and auto-fail on breach.
- Success criteria: subagent net share >= 60%, no delivery regression vs A/B.

4. **Experiment D: Docker reproducibility hardening**
- Objective: eliminate ambiguity in Docker-only compliance.
- Changes: scripted evidence collector for build/test/e2e in container.
- Success criteria: 100% required commands container-evidenced, no host-path drift.

5. **Experiment E: Parity-first test matrix expansion**
- Objective: close `st.button` semantic gaps.
- Changes: checklist-driven tests for callbacks, args/kwargs, disabled, width/type/icon behavior, rerun semantics.
- Success criteria: parity checklist 100% mapped to tests before release decision.

## 8) Appendix: data caveats and evidence index

### Data caveats

1. Some metrics are normalized across heterogeneous report formats (different attempts recorded telemetry with different granularity).
2. Duration fields are approximate for several attempts (“~2h”, “hours”, “~15h”).
3. Quality Score is a synthesized comparative measure and not a native repo metric (hypothesis-level construct).
4. Cross-attempt judgments about “architecture fidelity” rely on both code inventory and reviewer framing, which may include normative preference for custom component architecture over CSS wrapper approaches (mixed evidence and hypothesis).
5. Token/cost interpretations treat high cache-read as overhead risk; this is empirically correlated in this dataset but not a universal law across all tasks (hypothesis-level generalization).

### Confirmed evidence index

Per-attempt deep dives:
- `_review/evidence/attempt-1-deep-dive.md`
- `_review/evidence/attempt-2-deep-dive.md`
- `_review/evidence/attempt-3-deep-dive.md`
- `_review/evidence/attempt-4-deep-dive.md`
- `_review/evidence/attempt-5-deep-dive.md`
- `_review/evidence/attempt-6-deep-dive.md`

Cross-cut analyses:
- `_review/evidence/crosscut-orchestration.md`
- `_review/evidence/crosscut-cost-quality.md`
- `_review/evidence/crosscut-failure-taxonomy.md`

Supporting comparative context:
- `_review/REVIEW.md` (current-branch baseline review)
- Branch-specific reviews referenced via `git show origin/attempt-{N}:_review/REVIEW.md`

### Assumptions requiring explicit validation in next run

1. `cache_ratio <= 5x` and leverage `>= 2x` as reliable predictors of good outcomes.
2. Quality score thresholds (`>= 4.0`) as decision gates.
3. Fewer, larger subagents outperform many specialized subagents for this repository.
4. The proposed budget bands will not suppress required experimentation depth.
5. Architecture gate strictness (reject CSS-wrapper-only paths) is aligned with project owner intent for future versions.
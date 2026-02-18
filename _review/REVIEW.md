- It works! But the experiment is a failur
![alt text](image.png)
- It is a hack, agent went the easy route and implemented workaround JS/CSS not a valid element with React:

```
def _scoped_style_block(scope_id: str) -> str:
    scope_container = (
        f'div[data-testid="stElementContainer"]:has(span[data-hyperlink-button-scope="{scope_id}"])'
    )
...
```
 - ~1h 40m execution with no user intervention
- Total Cost $5.32
- Orchestrator Cost: $3.52
- Leverage (net tokens): 0.41x — `task` subagents used (same model), lightweight delegation
- Total tokens processed (including cached reads): 3,898.9K
- 4 tests, all pass, widget and playwright
- Issue, README, dev section proposes to install systemwide
- Orchestrator model: GPT-5.2
- just `task` + GPT 5.2  prompt forcing delegation and docker

## opencode-subagent stats

None, only plain `task` subagents

## opencode total stats

```
┌──────────────────────────────────────────────────────────┐
│                         OVERVIEW                         │
├──────────────────────────────────────────────────────────┤
│ Sessions                                               6 │
│ Messages                                              89 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                      COST & TOKENS                       │
├──────────────────────────────────────────────────────────┤
│ Total Cost                                         $5.32 │
│ Input                                               1.3M │
│ Output                                            116.0K │
│ Reasoning                                          82.9K │
│ Cache Read                                          2.4M │
│ Cache Write                                            0 │
│ Total Tokens                                        3.9M │
│ Avg Tokens/Session                                643.4K │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       MODEL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ azure/gpt-5.2                             83 msgs  $5.32 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                        TOOL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ bash                                          49 (40.5%) │
│ read                                          26 (21.5%) │
│ apply_patch                                   14 (11.6%) │
│ webfetch                                       11 (9.1%) │
│ glob                                            7 (5.8%) │
│ grep                                            6 (5.0%) │
│ task                                            5 (4.1%) │
│ todowrite                                       3 (2.5%) │
└──────────────────────────────────────────────────────────┘
```

## Orchestratort Session

```
New session - 2026-02-11T20:01:52.869Z
Context
98,472 tokens
25% used
$3.52 spent
```

```

┌──────────────────────────────────────────────────────────┐
│                         OVERVIEW                         │
├──────────────────────────────────────────────────────────┤
│ Sessions                                               1 │
│ Messages                                              46 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                      COST & TOKENS                       │
├──────────────────────────────────────────────────────────┤
│ Total Cost                                         $3.52 │
│ Input                                             945.2K │
│ Output                                             64.9K │
│ Reasoning                                          54.3K │
│ Cache Read                                          1.6M │
│ Cache Write                                            0 │
│ Total Tokens                                        2.7M │
│ Avg Tokens/Session                                  2.7M │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       MODEL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ azure/gpt-5.2                                            │
│   Messages                                            45 │
│   Input Tokens                                    945.2K │
│   Output Tokens                                   119.2K │
│   Cache Read                                        1.6M │
│   Cache Write                                          0 │
│   Cost                                           $3.5239 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                        TOOL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ bash                                          33 (50.8%) │
│ read                                          13 (20.0%) │
│ apply_patch                                    7 (10.8%) │
│ task                                            5 (7.7%) │
│ todowrite                                       3 (4.6%) │
│ grep                                            3 (4.6%) │
│ glob                                            1 (1.5%) │
└──────────────────────────────────────────────────────────┘

```

## Tokenomics

| Metric | Value | What it means |
|---|---|---|
| **Leverage (net tokens)** | 0.41x | `task` subagents (same GPT-5.2 model) contributed 0.41x the orchestrator's net effort |
| **`task` subagent share (net)** | 29.0% | `task` subagents did ~29% of unique token work |
| **`task` subagent share (gross)** | 31.7% | Similar gross share due to low cache bloat |
| **Cost per net M tokens (all)** | $3.55 | Single premium model for everything |
| **Cost per net M tokens (orch)** | $3.31 | Orchestrator session cost per net token |
| **Cost per net M tokens (subs)** | $4.14 | `task` subagents cost per net token (same model) |
| **Cache bloat (orchestrator)** | 1.50x | Very low conversation re-reading overhead |

**Bottom line**: Lightweight `task` subagent delegation — all using the same GPT-5.2 model across 6 sessions (5 `task` tool calls). The leverage ratio of 0.41x is very low — the orchestrator did ~71% of the work itself and barely delegated. Cache bloat is remarkably low at 1.50x (vs 26.4x in the dedicated-subagent example), meaning minimal wasted re-reading. Since all sessions use the same premium model, there's no cost advantage from delegation ($3.31 vs $4.14 per net M tokens). Total cost ($5.32) is 23% higher than the subagent example ($4.32) — without cheaper models to offload work, the single-model approach cost more overall while producing a worse result ("a hack" via CSS/JS workaround instead of a proper React component).

## How Tokens Actually Work

- **Input tokens**: The prompt sent to the model (your message + system prompt + context). The model *reads* these.
- **Output tokens**: What the model *generates* — actual reasoning, code, tool calls.
- **Reasoning tokens**: Internal chain-of-thought the model uses before generating output. Billed separately from output.
- **Cache Read tokens**: Previously seen input tokens that were cached and re-sent cheaply. The model still *reads* them, but you pay less. They represent **repeated context** (e.g., the full conversation history re-sent each turn).

So the **total tokens processed** (i.e., total "work" the model did) is:

$$\text{Total Work} = \text{Input} + \text{Cache Read} + \text{Output} + \text{Reasoning}$$

Cache reads are still *read by the model* — they're just cheaper to bill. From an **effort** standpoint, the model still processes them. But from a **novelty/unique work** standpoint, cache reads are redundant — they're the same context re-sent.

This gives us two useful metrics:

### 1. **Gross Effort** (total tokens processed)
Everything the model touched:

| Component | Input | Cache Read | Output | Reasoning | **Gross Total** |
|---|---|---|---|---|---|
| Orchestrator | 945.2K | 1,600K | 64.9K | 54.3K | **2,664.4K** |
| `task` subagents | 354.8K | 800K | 51.1K | 28.6K | **1,234.5K** |
| **All** | **1,300K** | **2,400K** | **116.0K** | **82.9K** | **3,898.9K** |

By gross effort, the orchestrator did **2,664.4K / 3,898.9K = 68.3%** of total work. `task` subagents did 31.7%. The orchestrator's 1.6M cache reads are just re-reading the same growing conversation each turn.

### 2. **Net Effort** (unique/new tokens only)
Strip out cache reads — what was *new* information flowing in and out:

$$\text{Net Effort} = \text{Input (non-cached)} + \text{Output} + \text{Reasoning}$$

| Component | Input (fresh) | Output | Reasoning | **Net Total** |
|---|---|---|---|---|
| Orchestrator | 945.2K | 64.9K | 54.3K | **1,064.4K** |
| `task` subagents | 354.8K | 51.1K | 28.6K | **434.5K** |
| **All** | **1,300K** | **116.0K** | **82.9K** | **1,498.9K** |

By net effort: the orchestrator did **1,064.4K / 1,498.9K = 71.0%** of unique token work. `task` subagents did 29.0%.

### 3. **Output-Only Effort** (what was actually *produced*)
If you only care about what each component *generated* (code, reasoning, decisions):

| Component | Output | Reasoning | Generated Total | Share |
|---|---|---|---|---|
| Orchestrator | 64.9K | 54.3K | 119.2K | **59.9%** |
| `task` subagents | 51.1K | 28.6K | 79.7K | **40.1%** |

---

## The Ratios That Actually Make Sense

### **Leverage Ratio** (Net Effort)
$$\text{Leverage} = \frac{\text{task subagent Net Effort}}{\text{Orchestrator Net Effort}} = \frac{434.5K}{1,064.4K} = 0.41$$

The orchestrator generated only **0.41x its own weight** in `task` subagent work. This confirms lightweight delegation — the orchestrator did most of the work itself, with `task` subagents handling smaller scoped operations.

### **Overhead Ratio** (Cost per Net Token)
$$\text{All sessions: } \frac{\$5.32}{1,498.9K} = \$3.55 \text{ per M tokens}$$
$$\text{Orchestrator: } \frac{\$3.52}{1,064.4K} = \$3.31 \text{ per M tokens}$$
$$\text{task subagents: } \frac{\$1.80}{434.5K} = \$4.14 \text{ per M tokens}$$

All sessions used the same model (GPT-5.2), so per-token costs are similar. The slight variation comes from different cache hit rates. No cost leverage from delegation since `task` subagents use the same premium model.

### **Cache Bloat Ratio**
$$\frac{\text{Orchestrator Cache Read}}{\text{Orchestrator Net Effort}} = \frac{1,600K}{1,064.4K} = 1.50x$$

The orchestrator re-read its context **1.50x** for every unit of new work. This is very low — the conversation didn't grow excessively. Compare to 26.4x in the subagent example where deep multi-turn coordination caused massive context re-reading.

---
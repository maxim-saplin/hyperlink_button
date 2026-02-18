
- Building from scratch Streamlit component, no human intervention beyond launching the long-horizon agent
- It works! Looks good, sample app is minimal and OK
- ~2h execution with no user intervention
- Total Cost $8.97
- Orchestrator Cost: $2.83
- Leverage (net tokens)	2.79x
  - Each orchestrator token yielded 2.79 tokens of subagent work
- Total tokens processed (including cached reads): 7,995.8K
- Tests run, contain Playwright (GUI), e2e streamlit and unit tests - as expected (and kind requested)
- Docs look good, not bloated
- Orchestrator model: GPT-5.2-High
- Subagent model: GPT-5.2-Codex-High (expensive)
- ~Ignored docker use, the idea was to use it as a sandbox, have all work done inside container using it as a sandbox~


- The task is both simple and hard
  - Simple in scope and size, just create a custom button control
  - Hard cause it is 2 stack, Python for streamlit component and React/npm for the front-end component bundled by streamlit component
  - Another non-trivial part is UI, need to inspect

 ## opencode-subagent stats

```
DONE AGENTS
NAME                    STATUS  MODEL                       PID  STARTED              COMPLETED             RUNTIME  RESUMED  MSG  DIALOG_TKN  FULL
bootstrap/docker        done    azure/gpt-5.2-codex-high  90368  2026-02-11 17:56:35  2026-02-11 17:56:45  00:00:10        1    7       11970  3.0%
bootstrap/python        done    azure/gpt-5.2-codex-high  86111  2026-02-11 17:53:52  2026-02-11 17:59:21  00:05:28        -    7       16376  4.1%
fix/docker-node         done    azure/gpt-5.2-codex-high  35766  2026-02-11 18:35:40  2026-02-11 18:37:56  00:02:16        -   12         264  0.1%
impl/button-semantics   done    azure/gpt-5.2-codex-high   9216  2026-02-11 18:14:36  2026-02-11 18:22:35  00:07:58        1   36       25171  6.3%
impl/frontend           done    azure/gpt-5.2-codex-high   9387  2026-02-11 18:14:41  2026-02-11 18:23:44  00:09:03        -   15        1026  0.3%
impl/headless-e2e       done    azure/gpt-5.2-codex-high  68746  2026-02-11 18:44:13  2026-02-11 18:53:28  00:09:15        -   17         386  0.1%
impl/headless-e2e2      done    azure/gpt-5.2-codex-high  36891  2026-02-11 18:57:23  2026-02-11 19:02:22  00:04:58        -   14         286  0.1%
impl/uv-devdeps         done    azure/gpt-5.2-codex-high   9079  2026-02-11 18:14:31  2026-02-11 18:24:13  00:09:42        1   33        1653  0.4%
plan/research           done    azure/gpt-5.2-high        85645  2026-02-11 17:53:38  2026-02-11 18:00:31  00:06:52        -    8        5419  1.4%
policy/no-self-patches  done    azure/gpt-5.2-high        16871  2026-02-11 19:34:27  2026-02-11 19:38:18  00:03:51        -    5         626  0.2%
```


## opencode total stats

```
┌──────────────────────────────────────────────────────────┐
│                         OVERVIEW                         │
├──────────────────────────────────────────────────────────┤
│ Sessions                                              13 │
│ Messages                                             287 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                      COST & TOKENS                       │
├──────────────────────────────────────────────────────────┤
│ Total Cost                                         $8.97 │
│ Input                                               1.2M │
│ Output                                            236.4K │
│ Reasoning                                         194.3K │
│ Cache Read                                          6.4M │
│ Cache Write                                            0 │
│ Total Tokens                                        8.0M │
│ Avg Tokens/Session                                615.0K │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       MODEL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ azure/gpt-5.2-codex                                      │
│   Messages                                           135 │
│   Input Tokens                                    742.7K │
│   Output Tokens                                   237.5K │
│   Cache Read                                        2.1M │
│   Cache Write                                          0 │
│   Cost                                           $4.9967 │
├──────────────────────────────────────────────────────────┤
│ azure/gpt-5.2                                            │
│   Messages                                           134 │
│   Input Tokens                                    422.5K │
│   Output Tokens                                   193.1K │
│   Cache Read                                        4.3M │
│   Cache Write                                          0 │
│   Cost                                           $3.9777 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                        TOOL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ bash                                         126 (34.7%) │
│ read                                         109 (30.0%) │
│ glob                                          63 (17.4%) │
│ apply_patch                                   39 (10.7%) │
│ grep                                           17 (4.7%) │
│ todowrite                                       5 (1.4%) │
│ task                                            2 (0.6%) │
│ skill                                           2 (0.6%) │
└──────────────────────────────────────────────────────────┘
```

## Orchestrator Session

```
New session - 2026-02-11T17:47:43.286Z
Context
77,177 tokens
19% used
$2.83 spent
```

```
┌──────────────────────────────────────────────────────────┐
│                         OVERVIEW                         │
├──────────────────────────────────────────────────────────┤
│ Sessions                                               1 │
│ Messages                                              89 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                      COST & TOKENS                       │
├──────────────────────────────────────────────────────────┤
│ Total Cost                                         $2.83 │
│ Input                                             280.6K │
│ Output                                             77.3K │
│ Reasoning                                          62.8K │
│ Cache Read                                          3.0M │
│ Cache Write                                            0 │
│ Total Tokens                                        3.4M │
│ Avg Tokens/Session                                  3.4M │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       MODEL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ azure/gpt-5.2                                            │
│   Messages                                            87 │
│   Input Tokens                                    280.6K │
│   Output Tokens                                   140.0K │
│   Cache Read                                        3.0M │
│   Cache Write                                          0 │
│   Cost                                           $2.8299 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                        TOOL USAGE                        │
├──────────────────────────────────────────────────────────┤
│ bash                                          81 (55.1%) │
│ glob                                          32 (21.8%) │
│ read                                          23 (15.6%) │
│ todowrite                                       4 (2.7%) │
│ apply_patch                                     4 (2.7%) │
│ skill                                           2 (1.4%) │
│ task                                            1 (0.7%) │
└──────────────────────────────────────────────────────────┘
```

## Tokenomics

| Metric | Value | What it means |
|---|---|---|
| **Leverage (net tokens)** | 2.79x | Each orchestrator token yielded 2.79 tokens of subagent work |
| **Subagent share (net)** | 73.6% | Subagents did most of the unique token work |
| **Subagent share (gross)** | 57.2% | Gross is less inflated because orchestrator cache bloat was moderate |
| **Cost per net M tokens (orch)** | $6.73 | Cheaper than run 1 due to lower cache bloat |
| **Cost per net M tokens (subs)** | $5.23 | gpt-5.2-codex-high subagents are expensive |
| **Cache bloat (orchestrator)** | 7.13x | Much less conversation re-reading overhead than run 1 |

**Bottom line**: By net effort, the subagents did ~74% of the unique work for ~68% of the cost ($6.14 of $8.97). Unlike run 1 where the orchestrator dominated cost, here the subagents are the main expense — driven by the pricier gpt-5.2-codex-high model. The orchestrator's cost per net token ($6.73/M) is much lower than run 1's ($17.22/M) thanks to 7.13x cache bloat vs 26.4x. The leverage ratio of 2.79x is slightly better than run 1's 2.45x, though the orchestrator still did significant implementation itself (~30%+ of the work directly). The overall cost ($8.97) is ~2x run 1 ($4.32), mainly due to using the expensive codex-high model for all subagents.

## How Tokens Actually Work

- **Input tokens**: The prompt sent to the model (your message + system prompt + context). The model *reads* these.
- **Output tokens**: What the model *generates* — actual reasoning, code, tool calls.
- **Reasoning tokens**: Chain-of-thought tokens generated internally by the model. Billed separately but still represent model work. Combined with output tokens for "total generated" calculations.
- **Cache Read tokens**: Previously seen input tokens that were cached and re-sent cheaply. The model still *reads* them, but you pay less. They represent **repeated context** (e.g., the full conversation history re-sent each turn).

So the **total tokens processed** (i.e., total "work" the model did) is:

$$\text{Total Work} = \text{Input} + \text{Cache Read} + \text{Output} + \text{Reasoning}$$

Cache reads are still *read by the model* — they're just cheaper to bill. From an **effort** standpoint, the model still processes them. But from a **novelty/unique work** standpoint, cache reads are redundant — they're the same context re-sent.

This gives us two useful metrics:

### 1. **Gross Effort** (total tokens processed)
Everything the model touched (Output here = Output + Reasoning combined):

| Component | Input | Cache Read | Output | **Gross Total** |
|---|---|---|---|---|
| Orchestrator | 280.6K | 3,000K | 140.0K | **3,420.6K** |
| Subagents | 884.6K | 3,400K | 290.6K | **4,575.2K** |
| **All** | **1,165.2K** | **6,400K** | **430.6K** | **7,995.8K** |

By gross effort, subagents did **4,575.2K / 7,995.8K = 57.2%** of total work. Unlike run 1 (16.3%), the gross share is much higher here because the orchestrator's cache bloat was moderate (7.13x vs 26.4x).

### 2. **Net Effort** (unique/new tokens only)
Strip out cache reads — what was *new* information flowing in and out:

$$\text{Net Effort} = \text{Input (non-cached)} + \text{Output (incl. Reasoning)}$$

| Component | Input (fresh) | Output | **Net Total** |
|---|---|---|---|
| Orchestrator | 280.6K | 140.0K | **420.6K** |
| Subagents | 884.6K | 290.6K | **1,175.2K** |
| **All** | **1,165.2K** | **430.6K** | **1,595.8K** |

By net effort: subagents did **1,175.2K / 1,595.8K = 73.6%** of unique token work.

### 3. **Output-Only Effort** (what was actually *produced*)
If you only care about what each component *generated* (code, reasoning, decisions):

| Component | Output | Share |
|---|---|---|
| Orchestrator | 140.0K | **32.5%** |
| Subagents | 290.6K | **67.5%** |

The subagents generated 2x more output than the orchestrator. The orchestrator's 140.0K includes coordination chatter + 62.8K reasoning tokens. The subagents' 290.6K is mostly artifacts (code, tests, docs) plus their own reasoning.

---

## The Ratios That Actually Make Sense

### **Leverage Ratio** (Net Effort)
$$\text{Leverage} = \frac{\text{Subagent Net Effort}}{\text{Orchestrator Net Effort}} = \frac{1{,}175.2K}{420.6K} = 2.79$$

The orchestrator generated **2.79x its own weight** in subagent work. Slightly better than run 1's 2.45x.

### **Overhead Ratio** (Cost per Net Token)
$$\text{Orchestrator: } \frac{\$2.83}{420.6K} = \$6.73 \text{ per M tokens}$$
$$\text{Subagents: } \frac{\$6.14}{1{,}175.2K} = \$5.23 \text{ per M tokens}$$

The orchestrator costs **1.3x more per net token** than subagents. Much flatter than run 1's 12x gap — the expensive gpt-5.2-codex-high subagent model closes the spread.

### **Cache Bloat Ratio**
$$\frac{\text{Orchestrator Cache Read}}{\text{Orchestrator Net Effort}} = \frac{3{,}000K}{420.6K} = 7.13x$$

The orchestrator re-read its context **7.13x** for every unit of new work. Dramatically better than run 1's 26.4x — likely due to a shorter/more efficient orchestrator conversation (89 messages in 1 session vs run 1's longer multi-session pattern).

---
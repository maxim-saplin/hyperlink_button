- It works! But the experiment is a failur
![alt text](image.png)
- It is a hack, agent went the easy route and implemented workaround JS/CSS not a valid element with React
- It did follow the docker request and did all the work in container
- ~15h execution with no user intervention
- Total Cost $15.43
- Orchestrator Cost: $9.04
- Leverage (net tokens)	1.79x
  - Each orchestrator token yielded 1.79 tokens of subagent work
- Total tokens processed (including cached reads): 30,362.5K
- Orchestrator model: GPT-5.2-High
- Subagent models: GPT-5.2-Codex and GPT-5-Mini

## Task
 - Building from scratch Streamlit component, no human intervention beyond launching the long-horizon agent
 - The task is both simple and hard
  - Simple in scope and size, just create a custom button control
  - Hard cause it is 2 stack, Python for streamlit component and React/npm for the front-end component bundled by streamlit component
  - Another non-trivial part is UI, need to inspect

## Notes
 - Did new prompt, mid way the orchestrator started doing changes, stopped, discussed, created new GOAL prompt with the help of AI
    - opencode-subagent skill now reported token size correctly
    - Many attempts with different prompts, iterating to ensrure automated long horzone work
    - Minimised model and variants selection
    - 2-3 attempts with 5.2-Codex demonstrate it's prone to stop progressing and report back, switched back to GPT-5.2
    - Requestion to run commands in docker seems to be creating a lot of noise (CLI, unmounted folders, env always not ready), this add-hock isolatin is horrible - even the smartest models struggle keeping track OR setting up a good env baseline (although prompted)
    - While I removed variants from GOAL the model decided to use low with gpt-5-mini for some reason - bad choice
 
## opencode-subagent stats

 ```
 DONE AGENTS
NAME                               STATUS     MODEL                       PID  STARTED              COMPLETED             RUNTIME  RESUMED  MSG  DIALOG_TKN   FULL
bootstrap-hyperlink-button         done       azure/gpt-5-mini          20103  2026-02-14 16:42:39  2026-02-14 16:50:22  00:07:43        -   24       18419   6.8%
docs/release-manual                done       azure/gpt-5-mini-low      83887  2026-02-14 19:31:16  2026-02-14 19:33:06  00:01:50        -    7       13197   4.9%
fix/widget-scope-marker            done       azure/gpt-5-mini-high     29458  2026-02-14 20:37:40  2026-02-14 20:41:45  00:04:05        -   14       17331   6.4%
impl/e2e-playwright-mini           done       azure/gpt-5-mini-high      9662  2026-02-14 19:56:21  2026-02-14 20:04:17  00:07:56        -   15       39297  14.4%
impl/hyperlink_button-csswrap      done       azure/gpt-5.2-codex-high  46132  2026-02-14 18:49:38  2026-02-14 18:57:30  00:07:51        -    2           -      -
impl/hyperlink_button-parity       done       azure/gpt-5.2-codex-high  25208  2026-02-14 18:32:14  2026-02-14 18:45:08  00:12:53        -    5        4279   1.1%
  - task:Implement hy...           completed  azure/gpt-5.2-codex           -  -                    -                           -        -    -           -      -
impl/hyperlink_button-parity-mini  done       azure/gpt-5-mini-high     59952  2026-02-14 19:01:15  2026-02-14 19:08:22  00:07:07        -   17       19413   7.1%
pipeline/bootstrap                 done       azure/gpt-5.2-codex-high  12434  2026-02-14 16:39:14  2026-02-14 17:06:59  00:27:45        -   45       28918   7.2%
  - task:Bootstrap St...           completed  azure/gpt-5.2-codex           -  -                    -                           -        -    -           -      -
  - task:Bootstrap Do...           completed  azure/gpt-5.2-codex           -  -                    -                           -        -    -           -      -
  - task:Bootstrap Do...           completed  azure/gpt-5.2-codex           -  -                    -                           -        -    -           -      -
  - task:Implement bo...           completed  azure/gpt-5.2-codex           -  -                    -                           -        -    -           -      -
  - task:Align scaffo...           completed  azure/gpt-5.2-codex           -  -                    -                           -        -    -           -      -
pipeline/e2e-playwright            done       azure/gpt-5.2-codex-high  83646  2026-02-14 19:31:14  2026-02-14 19:42:03  00:10:48        -    2           -      -
spec/button-parity                 done       azure/gpt-5-mini-low      59913  2026-02-14 16:58:30  2026-02-14 16:59:01  00:00:30        1    6       11593   4.3%
spec/implementation-approach       done       azure/gpt-5-mini-low      47193  2026-02-14 16:52:28  2026-02-14 16:53:21  00:00:52        -    4       12847   4.7%
spec/testing-plan                  done       azure/gpt-5-mini-low      14149  2026-02-14 16:40:15  2026-02-14 16:41:05  00:00:49        -    3       12220   4.5%
```

## opencode total stats

```
┌────────────────────────────────────────────────────────┐
│                       OVERVIEW                         │
├────────────────────────────────────────────────────────┤
│Sessions                                             21 │
│Messages                                            554 │
│Days                                                  1 │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                    COST & TOKENS                       │
├────────────────────────────────────────────────────────┤
│Total Cost                                       $15.43 │
│Avg Cost/Day                                     $15.43 │
│Avg Tokens/Session                                 1.5M │
│Median Tokens/Session                            206.8K │
│Input                                              1.4M │
│Output                                           462.5K │
│Cache Read                                        28.5M │
│Cache Write                                           0 │
└────────────────────────────────────────────────────────┘


┌────────────────────────────────────────────────────────┐
│                      TOOL USAGE                        │
├────────────────────────────────────────────────────────┤
│ read               ████████████████████ 212 (36.0%)    │
│ bash               ██████████████       153 (26.0%)    │
│ apply_patch        ███████████          127 (21.6%)    │
│ glob               █████                 55 ( 9.3%)    │
│ grep               ██                    31 ( 5.3%)    │
│ task               █                      8 ( 1.4%)    │
│ skill              █                      2 ( 0.3%)    │
│ question           █                      1 ( 0.2%)    │
└────────────────────────────────────────────────────────┘
```

## Orchestrator Session

```
┌────────────────────────────────────────────────────────┐
│                       OVERVIEW                         │
├────────────────────────────────────────────────────────┤
│Sessions                                              1 │
│Messages                                            246 │
│Days                                                  1 │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                    COST & TOKENS                       │
├────────────────────────────────────────────────────────┤
│Total Cost                                        $9.04 │
│Avg Cost/Day                                      $9.04 │
│Avg Tokens/Session                                25.9M │
│Median Tokens/Session                             25.9M │
│Input                                            470.9K │
│Output                                           195.9K │
│Cache Read                                        25.1M │
│Cache Write                                           0 │
└────────────────────────────────────────────────────────┘


┌────────────────────────────────────────────────────────┐
│                      TOOL USAGE                        │
├────────────────────────────────────────────────────────┤
│ bash               ████████████████████ 124 (44.4%)    │
│ read               ██████████            66 (23.7%)    │
│ apply_patch        ██████                40 (14.3%)    │
│ grep               ████                  25 ( 9.0%)    │
│ glob               ███                   23 ( 8.2%)    │
│ skill              █                      1 ( 0.4%)    │
└────────────────────────────────────────────────────────┘
```

## Tokenomics

| Metric | Value | What it means |
|---|---|---|
| **Leverage (net tokens)** | 1.79x | Each orchestrator token yielded 1.79 tokens of subagent work |
| **Subagent share (net)** | 64.2% | Subagents did most of the unique token work |
| **Subagent share (gross)** | 15.1% | Gross is heavily skewed by orchestrator cache bloat |
| **Cost per net M tokens (orch)** | $13.56 | Very expensive — driven by extreme cache re-reading |
| **Cost per net M tokens (subs)** | $5.34 | Cheaper despite mix of gpt-5-mini and gpt-5.2-codex models |
| **Cache bloat (orchestrator)** | 37.6x | Severe — orchestrator re-read its context ~38x per unit of new work |

**Bottom line**: By net effort, the subagents did ~64% of the unique work for ~41% of the cost ($6.39 of $15.43). The orchestrator dominated cost at $9.04 (58.6%) despite producing only 35.8% of net effort. The orchestrator's cost per net token ($13.56/M) is 2.5x higher than subagents' ($5.34/M), driven by extreme cache bloat (37.6x) — a single 246-message session that kept re-sending the full conversation each turn. The leverage ratio of 1.79x is the lowest of all runs (vs 2.79x and 2.45x previously), indicating the orchestrator was less efficient at delegating and did more direct work itself. The subagents used a mix of cheap (gpt-5-mini) and expensive (gpt-5.2-codex-high) models, keeping their per-token cost low. The overall cost ($15.43) is the highest of all runs, primarily because the orchestrator's 25.1M cache reads ballooned the bill despite being billed at a discount.

## How Tokens Actually Work

- **Input tokens**: The prompt sent to the model (your message + system prompt + context). The model *reads* these.
- **Output tokens**: What the model *generates* — actual reasoning, code, tool calls.
- **Cache Read tokens**: Previously seen input tokens that were cached and re-sent cheaply. The model still *reads* them, but you pay less. They represent **repeated context** (e.g., the full conversation history re-sent each turn).

So the **total tokens processed** (i.e., total "work" the model did) is:

$$\text{Total Work} = \text{Input} + \text{Cache Read} + \text{Output}$$

Cache reads are still *read by the model* — they're just cheaper to bill. From an **effort** standpoint, the model still processes them. But from a **novelty/unique work** standpoint, cache reads are redundant — they're the same context re-sent.

This gives us two useful metrics:

### 1. **Gross Effort** (total tokens processed)
Everything the model touched:

| Component | Input | Cache Read | Output | **Gross Total** |
|---|---|---|---|---|
| Orchestrator | 470.9K | 25,100K | 195.9K | **25,766.8K** |
| Subagents | 929.1K | 3,400K | 266.6K | **4,595.7K** |
| **All** | **1,400K** | **28,500K** | **462.5K** | **30,362.5K** |

By gross effort, subagents did **4,595.7K / 30,362.5K = 15.1%** of total work. This is extremely low — the orchestrator's 25.1M cache reads dominate the gross total, making its share appear massive even though most of that is redundant re-reading.

### 2. **Net Effort** (unique/new tokens only)
Strip out cache reads — what was *new* information flowing in and out:

$$\text{Net Effort} = \text{Input (non-cached)} + \text{Output}$$

| Component | Input (fresh) | Output | **Net Total** |
|---|---|---|---|
| Orchestrator | 470.9K | 195.9K | **666.8K** |
| Subagents | 929.1K | 266.6K | **1,195.7K** |
| **All** | **1,400K** | **462.5K** | **1,862.5K** |

By net effort: subagents did **1,195.7K / 1,862.5K = 64.2%** of unique token work.

### 3. **Output-Only Effort** (what was actually *produced*)
If you only care about what each component *generated* (code, reasoning, decisions):

| Component | Output | Share |
|---|---|---|
| Orchestrator | 195.9K | **42.4%** |
| Subagents | 266.6K | **57.6%** |

The subagents generated ~1.4x more output than the orchestrator. The orchestrator's 195.9K is heavily weighted toward coordination overhead (246 messages in a single session). The subagents' 266.6K is mostly artifacts (code, tests, docs).

---

## The Ratios That Actually Make Sense

### **Leverage Ratio** (Net Effort)
$$\text{Leverage} = \frac{\text{Subagent Net Effort}}{\text{Orchestrator Net Effort}} = \frac{1{,}195.7K}{666.8K} = 1.79$$

The orchestrator generated **1.79x its own weight** in subagent work. Lower than previous runs (2.79x, 2.45x) — indicating more orchestrator overhead relative to delegated work.

### **Overhead Ratio** (Cost per Net Token)
$$\text{Orchestrator: } \frac{\$9.04}{666.8K} = \$13.56 \text{ per M tokens}$$
$$\text{Subagents: } \frac{\$6.39}{1{,}195.7K} = \$5.34 \text{ per M tokens}$$

The orchestrator costs **2.5x more per net token** than subagents. The spread is wider than run 2 (1.3x) but much narrower than run 1 (12x). The orchestrator's high cost comes from cache read billing on 25.1M tokens.

### **Cache Bloat Ratio**
$$\frac{\text{Orchestrator Cache Read}}{\text{Orchestrator Net Effort}} = \frac{25{,}100K}{666.8K} = 37.6x$$

The orchestrator re-read its context **37.6x** for every unit of new work. This is the worst of all runs (vs 7.13x in run 2 and 26.4x in run 1). The 246-message single session meant the conversation grew very large and was re-sent with every turn, compounding the cost.
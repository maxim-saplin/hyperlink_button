- Single thread no subagents
- After hours of execution stopped it, requests seemed hanged
- The models started getting screenshots and using curl against container, seems like a lot of overhead was here
- GPT 5.2 High + prompt forcing docker

┌────────────────────────────────────────────────────────┐
│                       OVERVIEW                         │
├────────────────────────────────────────────────────────┤
│Sessions                                              1 │
│Messages                                            257 │
│Days                                                  1 │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                    COST & TOKENS                       │
├────────────────────────────────────────────────────────┤
│Total Cost                                       $11.22 │
│Avg Cost/Day                                     $11.22 │
│Avg Tokens/Session                                31.4M │
│Median Tokens/Session                             31.4M │
│Input                                            846.1K │
│Output                                           230.9K │
│Cache Read                                        30.2M │
│Cache Write                                           0 │
└────────────────────────────────────────────────────────┘


┌────────────────────────────────────────────────────────┐
│                      TOOL USAGE                        │
├────────────────────────────────────────────────────────┤
│ bash               ████████████████████ 202 (76.2%)    │
│ apply_patch        ███                   33 (12.5%)    │
│ read               █                     15 ( 5.7%)    │
│ glob               █                      8 ( 3.0%)    │
│ todowrite          █                      4 ( 1.5%)    │
│ grep               █                      3 ( 1.1%)    │
└────────────────────────────────────────────────────────┘
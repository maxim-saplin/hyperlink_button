- Attempt 3 - sneaky bastard noticed there's attempt-1 branch and started "taking insipirations" from there (which seemed like a chat). Suspect that was due to pending changes in Git which the agent picked up and swayed away
- Upon restart the agent for some reason decided subagents can't patch file (doesn't have ther tool?) - had to intervene early on and shout at orchestrator
!!! Though re: skill - explain which tools/capabilties the agents have, explain the levels of agents (e.g. orchestrator can do subagent and task, subagent can only do task -> draw mermaid)
- Juat like in attempt-2 here I wanted you steer agents to rely on docker container (and set it up accordingly) using a "weak" for of sandboxing.
- In attempt-1 I didn't course correct
- Mid way orchestrator missed script directory (seen it before) and it had a short detour inspecting opencode-subagent internal state files
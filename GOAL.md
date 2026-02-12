Goal:
Build a `hyperlink_button` Streamlit element that has exactly the same API and functionality as the standard Streamlit button, but looks like a typical hoverable hyperlink.

Context:
The challenge is that there is currently no way to create an interactive element in Streamlit that looks and behaves like a hyperlink but functions as a button (distinct from Streamlit's existing `link_button` control, which looks like a button but behaves like a hyperlink). Workarounds via JS injection are an inelegant solution for achieving a true hyperlink-looking button in Streamlit. This new element will allow Streamlit developers to import the library and use the element.

Operating mode:
- Exercise autonomy
- Delegate, do not do the work yourself
- Focus on integrating and verifying the work of subagents
- Execute research, preparation, planning, building, and testing
- Fight bloat fiercely
- Do not bother the user until necessary if you are not finished
- Be accountable for end results

Verification:
- Ensure the code being built is tested
- Use unit and integration tests
- Utilize CLI
- Utilize Streamlit's widget testing
- Use headless browsing to verify Streamlit render output

Constraints:
- ALL WORK MUST BE DONE AND TESTED IN A DOCKER CONTAINER: prepare image, mount repo, use Docker as sandbox, do not run any CLI commands against host except as necessary to interact with Docker
- DO NOT DO CODING BY YOURSELF, YOU'VE GOT SUB-AGENTS FOR THAT
- Use uv and Python 3.13 for development
- Use only the most recent versions of libraries; never manually type in versions rely on CLI for package amanagemenbt (e.g. uv add)
- Only use Docker for runtime checks, run and inspect the app inside the container, use CLI via Docker

Important notes:
- The library must be covered with automated tests and documentation
- The library must be ready for publishing to PyPI
- An exhaustive manual for the PyPI release must be created (assume the user has never published to PyPI but has experience publishing to pub.dev)
- The repo must include a simple test app that a user can run to test the control
- The repo contains a ./st_docs/ symlink—this is a directory with Streamlit docs, used for research and exploration; it must have the manual for extension building

Orchestration approach:
- Delegate work to subagents: plan, describe tasks, verify—do not waste your cognitive bandwidth on small things. Be the leader and the manager. Management is the art of achieving results through the efforts of others.
- Use the `opencode-subagent` skill for larger tasks where session resumption, more inputs, and adjustments are needed
  - Plan macro-tacks, do not hesitate to ask resumabe subagents to follow-up and iterate
  - When reasonable - ask subagents to do nested delegation via `task` tool
  - When using opencode-subagent, explicitly define the model to be used
- Don't use `task` directly, push subagents to create smaller shortlived subagents via `task`
- Prioritase use of less expensive subagents, deffer to stronger subagent only when absilutely necessary (you are hitting a roadblock)
- If the environment changes, update AGENTS.md to efficiently guide new subagents


Models available to `opencode-subagent`:
- azure/gpt-5-nano: low intelligence, cheap, 272k context
- azure/gpt-5-mini: medium intelligence, moderate cost, 272k context
- azure/gpt-5.2-codex: high intelligence, coding-focused, expensive, 272k context


Model variants available: 'medium' and 'high' for different reasoning needs.

Tools available: all subagents have exactly the same tools as orchestrator.

-----------------------------------------------------------------------------

!!! STEP 0 !!! Before starting the project and taking the driver’s seat:
- Verify the environment using CLI and make sure you have all necessary tools
- Raise any concerns if you consider the request non-viable
- Ask questions, if any
- Create an initial version of AGENTS.md to be used by subagents

REITERATING, STEP 0 IS CHECK-IN WITH THE USER BEFORE KICKING OF THE AUTONOMOUS WORK!
Goal:
Build `hyperlink_button` Streamlit element that has absolutely the same API and functionality as stock Streamlit button but looks like a typical hoverable text. 

Context:
The challenge is there's no way to create an interactive element which looks and behaves like a link but allows to use it as button element in streamlit (don't confuse with streamlit's existing link_button control which looks like button but behaves like a hyperlink). Workarounds via JS injects is the only ugly way to get a true hyperlink looking button in St. This element will allow ST devs to import the new library and use the element.

Operating mode:
- Exercise autonomy
- Delegate, do not do work by yourself
- Focus on integrating and verifying the work of subagents
- Execute research, preparations, planning, building and testing
- Fight bloat fiercely
- Do not bother the user if you're not done until absolutely necessary
- Be accountable for the end results

Verification:
- Make sure the code being built is tested
- Use unit and integration tests
- Utilize CLI
- Utilize streamlit's widget testing
- Utilize headless browsing to check what is being rendered by streamlit

Constraints:
- ALL WORK DONE AND TESTED IN DOCKER CONTAINER `dev-4`: prep image, mount repo there, use docker as snadbox, do not run any CLI commands against host beyond what is necessary to prep/interact with docker
- DO NOT UPDATE ANY FILES BY YOURSELF until it's some minor fix not worth delegation, always rely on subagents
- Use uv and Python 3.13 for development
- Use only the most recent versions of libraries, i.e. never hardcode versions in pyproject.toml, install via uv the most recent versions
- Only use docker for runtime checks, run and inspect the app inside container, use CLI via docker
- Target Python 3.13 and above

Important mentions:
- The library must be covered with automated tests and docs
- The library must be ready for publishing to PyPI
- Exhaustive manual for PyPI must be created (assuming someone has never published to PyPI but has experience publishing to pub.dev)
- The repo must contain a simple test app that a user can run and test the control
- The repo contains ./st_docs/ symlink - it is a directory with streamlit docs, use it for research and exploration > it must have the manual for extension building


Orchestration approach:

- Delegate work to subagents: plan, describe tasks, verify - don't waste your brain cycles on small things. Be the leader and the manager. Management is the art of getting the result through the effort of others
- Use `task` tool for one-off tasks where you need prompt-and-response from a subagent and don't intend to follow-up with the subagent


STEP 0!!! Before we kick off the project and you take the driver's seat:
- Verify environment using CLI and make sure you are equipped with all necessary tools
- Shoot if you consider the request non-viable
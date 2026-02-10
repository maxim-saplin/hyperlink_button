Goal:
Build `hyperlink_button` Streamlit element that has absolutely the same API and functionality as stock Stramlit button but looks like a stypical hoverable text. 

Context:
The challenge is there's no way to create an interactive element which looks and behaves like a link but allows to use it as button element in streamlit (don't confuse with streamlit's exisating link_button control which looks like button but bhaves like a hyperlink). Workarounds via JS injects is the only ugly way to get a tru hypelink looking button in St. This element will allow ST devs to import the new libary and use the element.

Operating mode:
- Excecrise autonomy
- Do not bother the user if you're not done until absolutely necessary
- Execute research, preparations, planning, building and testing
- Delegate
- Fight bloat fiercely
- Be accountable for the end results

Verification:
- Make sure the code being built is tests
- Use unit and integration tests
- Utilize CLI
- Utilize streamlit's widget testing
- Utilize headless browsing to check what is being rendered by streamlit

Constrains:
- Use uv and Python 3.13 for development
- Use only the most recent versions of libraries, i.e. never hardcode versions in pyproject.toml, install via uv the most recent versions
- Only use docker for runtime checks, run and inspect the app inside container, use CLI via docker
- Target Python 3.13 and above

Important mentions:
- The library must be covered with atuomated tests and docs
- The library must be ready for publishing to pypy
- Exhastive manual for pypi manual must be created (asssumg this someone has never published to pypy but has experience publushing to pub.dev)
- The repo must contain a simple test app the a user can run and test the control
- The repo contains ./st_docs/ synmlink - it is a directory with streamlit docs, use it for research and exploration > it must have the manual for extentioin building


Orchestration approach:
- Delegate work to subagents: plan, describe tasks, verify - don't waiste your brain cycles on small things. Be the leader and the manager. Management is the art of getting the result through the effort of others
- When choosing subagents pick wisely
  - Use `task` tool for one-of tasks where you need prompt-and-response from a subagent and don't intende to follo-up with thew subagent
  - Use `opencode-subagent` skill for larger tasks where you have the ability to resume subagent sessions, providfe more inputs and ask for addustemnts
  - When using opencode-subagent don't be shy to also require using task subagents
  - When using opencode-subagent subagents explicitly define model to be used

Models available:
- dial/gpt-5-nano, low intelligence, cheap, 272k context window
- dial/gpt-5-mini, medium intelligence, medium cost, 272k context window
- yourself - high inteligence, expnesive, 272k context window

STEP 0!!! Before we kick of the project and you take the drivers seat:
- Verify environment using CLI and make sure you are equiped with all necessary tools
- Shoot if you consider the request unvaiable
- Ask questions, if any


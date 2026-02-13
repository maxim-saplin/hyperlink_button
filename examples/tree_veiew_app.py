"""
Tree view sample using hyperlink_button and Streamlit standard controls.

Displays a made-up file structure with folders and files as hyperlinks only.
Click folder hyperlinks to expand/collapse; click file hyperlinks to view.
"""

import streamlit as st

from hyperlink_button import hyperlink_button

# Made-up file structure: dict = folder, None = file
FILE_TREE = {
    "src": {
        "app": {
            "main.py": None,
            "utils": {
                "helpers.py": None,
                "config.py": None,
            },
            "models": {"user.py": None, "post.py": None},
        },
        "tests": {"test_main.py": None, "test_utils.py": None, "conftest.py": None},
        "README.md": None,
    },
    "docs": {"index.md": None, "api": {"reference.md": None}, "guides": {"getting-started.md": None}},
    "config": {"config.yaml": None, "secrets.env": None},
    "config.yaml": None,
    "requirements.txt": None,
    "pyproject.toml": None,
    ".gitignore": None,
    ".env.example": None,
}


def _matches_filter(path: str, filter_type: str) -> bool:
    """Check if a file path matches the selected type filter."""
    if filter_type == "All":
        return True
    if filter_type == "Python":
        return path.endswith(".py")
    if filter_type == "Config":
        return path.endswith((".yaml", ".yml", ".env"))
    if filter_type == "Docs":
        return path.endswith((".md", ".mdx"))
    return True


def _tree_row(depth: int, label: str, key: str, help_text: str, clicked_callback=None) -> bool:
    """Render one tree row with simulated indent via columns. Returns True if clicked."""
    indent_ratio = min(0.25, depth * 0.06) if depth > 0 else 0.01
    content_ratio = 1 - indent_ratio
    cols = st.columns([indent_ratio, content_ratio])
    with cols[0]:
        st.write("")  # Spacer for indent
    with cols[1]:
        clicked = hyperlink_button(label, key=key, help=help_text)
    if clicked and clicked_callback:
        clicked_callback()
    return clicked


def render_tree(
    node: dict | None,
    path: str = "",
    depth: int = 0,
    filter_type: str = "All",
    show_hidden: bool = True,
):
    """Recursively render folder structure using hyperlink buttons only."""
    if node is None:
        return

    expanded = st.session_state.expanded_paths

    for name, child in node.items():
        full_path = f"{path}/{name}" if path else name
        if not show_hidden and name.startswith("."):
            continue

        if child is None:
            # Leaf file - apply filter
            if not _matches_filter(full_path, filter_type):
                continue
            key = f"file_{full_path.replace('/', '_')}"
            _tree_row(
                depth,
                f"📄 {name}",
                key=key,
                help_text=f"Open {full_path}",
                clicked_callback=lambda p=full_path: (
                    setattr(st.session_state, "selected_file", p),
                    setattr(st.session_state, "selected_content", _fake_content(p)),
                ),
            )
        else:
            # Folder - 📂 expanded, 📁 collapsed (one icon per node)
            is_expanded = full_path in expanded
            icon = "📂" if is_expanded else "📁"
            key = f"folder_{full_path.replace('/', '_')}"
            _tree_row(
                depth,
                f"{icon} {name}",
                key=key,
                help_text="Collapse" if is_expanded else "Expand",
                clicked_callback=lambda p=full_path, exp=is_expanded: (
                    expanded.discard(p) if exp else expanded.add(p),
                    st.rerun(),
                ),
            )
            if is_expanded:
                render_tree(child, full_path, depth + 1, filter_type, show_hidden)


def _fake_content(path: str) -> str:
    """Return fake file content for display."""
    if path.endswith(".py"):
        return f'''# {path}
def main():
    """Entry point."""
    print("Hello from {path}")

if __name__ == "__main__":
    main()
'''
    if path.endswith((".md", ".mdx")):
        return f"""# {path}

This is placeholder content for the documentation file.

## Overview
- Section one
- Section two
"""
    if path.endswith((".yaml", ".yml", ".env")):
        return f"# {path}\nkey: value\nanother: setting"
    return f"# {path}\n[Binary or unknown file type]"


def main():
    st.set_page_config(page_title="File Tree", page_icon="📂", layout="wide")

    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None
    if "selected_content" not in st.session_state:
        st.session_state.selected_content = None
    if "expanded_paths" not in st.session_state:
        st.session_state.expanded_paths = {"src"}

    tree_col, content_col = st.columns([1, 2])

    with tree_col:
        render_tree(FILE_TREE)

    with content_col:
        if st.session_state.selected_file:
            st.code(st.session_state.selected_content, language="python")
            st.caption(f"File: `{st.session_state.selected_file}`")
        else:
            st.info("Select a file from the tree to view its contents.")


if __name__ == "__main__":
    main()

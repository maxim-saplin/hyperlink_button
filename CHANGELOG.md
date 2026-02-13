# Changelog

## [0.1.1] - 2026-02-13

### Fixed
- Made click activation reliable by moving `Streamlit.setComponentValue(...)` out of the React state updater.
- Removed duplicate keyboard activation handling so Enter/Space no longer trigger double increments.
- Seeded frontend click counter from backend session state to prevent missed clicks after iframe remounts.

### Added
- Added/updated tree view sample app using hyperlink controls in `examples/tree_veiew_app.py`.


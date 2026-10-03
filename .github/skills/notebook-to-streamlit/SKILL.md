---
name: notebook-to-streamlit
description: Use when converting an existing Jupyter Notebook into a Streamlit app while reusing the notebook's existing analysis and business logic. Not for building a Streamlit app from scratch, and not for notebook-only changes.
---

## Step 1 — Extract reusable core logic
1. Identify the reusable computation functions from the Jupyter Notebook.
2. Test the functions using the same inputs used in the notebook and confirm that they produce consistent and reasonable results before building the Streamlit interface.
3. Extract or reuse these functions in a separate Python module and this module only for computating and logic with no Streamlit imports and no user-interface code.
4. Ensure all core functions return reusable values that can be used by the Streamlit app.

## Step 2 — State discipline

Streamlit reruns the whole script on every widget interaction.

1. Any `if st.button(...)` block should **mutate state only**.
2. Rendering happens outside those blocks, reading from `st.session_state` unconditionally.
3. Anything the user would be annoyed to lose on a rerun goes in session state - including the currently displayed result, not just accumulated history.

## Done when

- [ ] The reusable functions from the notebook still work.
- [ ] The Streamlit app has been tested by clicking the main action button.
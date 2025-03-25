# Pixel Patrol

## How to use

1. Clone repository
2. Install `uv`
3. `uv pip install -e .`
4. `uv run streamlit_main.py`

If you get an error when adding a folder path - install tkinter/python-tk:   
Ubuntu: `sudo apt-get install python3-tk`  
Mac: `brew install python-tk`  

## How to add widget

Widgets can be added in this repository or in separate packages.

### Write Widget

```
# my/widgets/test_widget.py

import streamlit as st
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class TestWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return "Other"

    def run(self, selected_files_df):
        with st.expander("Test widget", expanded=False):
            st.text("Hi!")
```

### Add Widget to `entry-points` of the package

```
# pyproject.toml

[project]
...
[project.entry-points."pixel_patrol.widgets"]
test_widget = "my.widgets.test_widget:TestWidget"

```
import importlib.util
from collections import defaultdict, OrderedDict

import pandas as pd
import streamlit as st

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.utils.session import get_all_widgets, set_all_widgets


def output_ratio_of_files_with_column_info(df, column_name, display_name=None, treat_one_as_null=False, numeric=False):

    display_name = display_name or column_name
    total_files = len(df)

    if numeric:
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')  # TODO: Move this to process metadata!
    # TODO: Maybe all column type conversions should be done in process metadata?

    if pd.api.types.is_numeric_dtype(df[column_name]):
        column_present = df[column_name].notnull() & (df[column_name] != 0)
        if treat_one_as_null:
            column_present &= (df[column_name] != 1)
    else:
        column_present = df[column_name].notnull()

    column_count = column_present.sum()
    percentage = (column_count / total_files) * 100

    if pd.api.types.is_numeric_dtype(df[column_name]):
        if treat_one_as_null:
            st.markdown(
                f"**{percentage:.2f}% ({column_count}/{total_files})** of files have valid `{display_name}` information (excluding 0 and 1)."
            )
        else:
            st.markdown(
                f"**{percentage:.2f}% ({column_count}/{total_files})** of files have valid `{display_name}` information (excluding 0)."
            )
    else:
        st.markdown(
            f"**{percentage:.2f}% ({column_count}/{total_files})** of files have `{display_name}` information."
        )

    return column_present


def get_required_columns(widgets):
    columns = []
    for widget in widgets:
        if hasattr(widget.__class__, "required_columns"):
            for column in widget.required_columns():
                if column not in columns:
                    columns.append(column)
    return columns


def load_widgets():
    """Discover and load all widget widgets using importlib.metadata."""
    widgets = []
    for entry_point in importlib.metadata.entry_points().select(group='pixel_patrol.widgets'):
        widget_class = entry_point.load()
        widget_instance = widget_class()
        # if issubclass(type(widget_instance), ImagePrevalidationWidgetDeprecated) or issubclass(type(widget_instance), ImagePrevalidationWidget):
        widgets.append(widget_instance)
    return widgets


def load_or_get_project_widgets(project):
    widgets = get_all_widgets()
    if not widgets:
        widgets = load_widgets()
        set_all_widgets(widgets)
    # Load widget selection from project config if available
    project_widgets = project.selected_widgets
    if project_widgets:
        widgets = [w for w in widgets if w.name in project_widgets]
    return widgets


def organize_widgets_by_tab(widgets):
    """Organize widgets based on their designated tabs."""
    tabbed_widgets = defaultdict(list)
    for widget in widgets:
        tabbed_widgets[widget.tab].append(widget)
    default_tab_values = {tab.value for tab in DefaultTabs}
    ordered_keys = [tab.value for tab in DefaultTabs if tab.value in tabbed_widgets]
    extra_keys = [tab for tab in tabbed_widgets if tab not in default_tab_values]
    all_keys = ordered_keys + extra_keys
    return OrderedDict((tab, tabbed_widgets[tab]) for tab in all_keys)

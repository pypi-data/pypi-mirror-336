import os
from datetime import datetime
from importlib.resources import files
from pathlib import Path

import polars as pl
import streamlit as st
from matplotlib import pyplot as plt
from plotly import graph_objects as go
from streamlit_extras.stylable_container import stylable_container

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.project import Project
from pixel_patrol.utils.session import get_all_widgets, set_all_widgets, set_current_step, PrevalidationStep
from pixel_patrol.utils.utils import is_subpath, is_superpath, apply_fast_mode, \
    add_new_path, get_dataframe_path_structure_path, get_dataframe_images_file, update_path_summary
from pixel_patrol.utils.widget import load_widgets, \
    organize_widgets_by_tab

try:
    import tkinter as tk
    from tkinter import filedialog
except ModuleNotFoundError:
    st.error("Required module 'tkinter' is not installed. Please install it to continue - Instructions are in README.")


def configure_layout(project):
    """
    Configure the Streamlit layout: set page configuration and inject global CSS.
    """
    if project.is_report_mode:
        st.set_page_config(layout="centered")
    else:
        st.set_page_config(layout="wide")
        css = """
        <style>
            .scrollable-tree {
                overflow-x: auto; /* Enable horizontal scrolling */
                white-space: nowrap; /* Prevent text wrapping */
                max-width: 100%; /* Constrain the width to the column */
            }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

def get_sidebar_container_style(i, value):
    container_active = """
                    button {
                        width: 100%;
                        font-weight: bold;
                        background: #414142;
                        color: white;
                    }
                    """
    container_past = """
                    button {
                        width: 100%;
                    }
                    """
    container_future = """
                    button {
                        width: 100%;
                    }
                    """
    if i < value:
        return container_past
    if i > value:
        return container_future
    return container_active


def get_directories_column_configuration():
    return {
        "parent": None,
        "depth": None,
        "type": None,
        "size": None,
        "size_readable": st.column_config.Column(label="Size"),
        "name": st.column_config.Column(label="Path"),
        "modification_date": st.column_config.Column(label="Modified"),
    }


def display_imported_dirs_info(project):
    if not project.path_summaries:
        st.info("No directories imported yet.")
        return

    for path, summary_df in project.path_summaries.items():
        st.write(path)
        col1, col2, col3 = st.columns([4, 4, 1])

        with col1:
            # Transpose summary_df for clear vertical presentation
            df_transposed = summary_df.transpose(include_header=True)
            st.dataframe(df_transposed, use_container_width=True) # TODO: column header as name like it was

        with col2:
            detailed_df = project.paths.get(path)
            if detailed_df is not None and not detailed_df.is_empty():
                sunburst_dirs(detailed_df) # TODO: crashes when too big - Fix (e.g. ella/Desktop/test
            else:
                st.info("No folder data available for sunburst visualization.")

        with col3:
            if st.button("Remove from project", key=path):
                remove_path(project, path)
            path_images = get_dataframe_images_file(path)
            path_structure = get_dataframe_path_structure_path(path)
            cache_exists = not os.path.exists(path_images) or not os.path.exists(path_structure)
            if st.button("Clear data cache", key=f"{path}_cache", disabled=cache_exists):
                os.remove(path_images)
                os.remove(path_structure)
                update_path_summary(path, project)
                st.rerun()


def add_dir_cache_date(display_df, imported):
    cache_file = get_dataframe_path_structure_path(imported["path"])
    if os.path.exists(cache_file):
        cache_date = datetime.fromtimestamp(os.path.getmtime(cache_file)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        cache_date = "No Cache"
    display_df = display_df.with_columns(pl.lit(cache_date).alias("cache_date"))
    return display_df


def remove_path(project: Project, dir_path: str):
    project.paths.pop(dir_path, None)
    project.path_summaries.pop(dir_path, None)
    st.success(f"Removed directory: {dir_path}")
    st.rerun()


def sunburst_dirs(dataframe: pl.DataFrame):
    dataframe = dataframe.filter(pl.col("type").eq("folder"))

    if dataframe.is_empty() or dataframe.height == 1:
        return

    # Extract columns from the Polars DataFrame
    ids = dataframe['name'].to_list()
    labels = [os.path.basename(name) for name in dataframe['name'].to_list()]
    parents = dataframe['parent'].to_list()
    values = dataframe['size'].to_list()

    # Define colors
    root_color = "#2b252a"
    colors = [root_color if not parent else None for parent in parents]

    # Create the Sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=colors),
    ))

    fig.update_layout(margin=dict(t=0, l=20, r=0, b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)


def create_sunburst(df_pandas):

    labels = df_pandas['name'].tolist()
    parents = df_pandas['parent'].tolist()
    values = df_pandas['size'].tolist()

    # Create the Sunburst plot
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
    ))

    return fig


def get_step_name(step: PrevalidationStep) -> str:
    if step == PrevalidationStep.DEFINE_PROJECT:
        return "Define Project"
    if step == PrevalidationStep.SELECT_WIDGETS:
        return "Select Widgets"
    if step == PrevalidationStep.SETTINGS:
        return "Settings"
    if step == PrevalidationStep.REPORT:
        return "Report"
    return ""


def step_is_disabled(project, step: PrevalidationStep):
    project_exists = project.name is not None
    if step in (PrevalidationStep.SELECT_WIDGETS, PrevalidationStep.SETTINGS):
        # Disable if no project or no imported paths.
        return not project_exists or not project.paths
    if step == PrevalidationStep.REPORT:
        files = project.df_images
        return (not project_exists or files is None or files.is_empty() or
            project.has_project_config_changed())
    return False


def display_step_buttons(project, current_step):
    for step in PrevalidationStep:
        with stylable_container(
                key=step.name + "_container",
                css_styles=get_sidebar_container_style(step.value, current_step.value),
        ):
            if st.button(get_step_name(step), disabled=step_is_disabled(project, step)):
                set_current_step(step)
                st.rerun()


def choose_matplotlib_colormap(default):
    available_cmaps = sorted([c for c in plt.colormaps() if not c.endswith("_r")])
    selected_cmap = st.selectbox(
        "Colormap of selected directories:",
        available_cmaps,
        index=available_cmaps.index(default),
        key="select_colormap"  # Unique key added here
    )
    return selected_cmap


def display_widget_selection_confirmation_buttons(project):
    buttons_col1, buttons_col2 = st.columns(2)
    with buttons_col1:
        if st.button("Confirm Widget Selection"):
            if project.selected_widgets:
                st.success("Selection confirmed!")
                set_current_step(PrevalidationStep.SETTINGS)
                st.rerun()
            else:
                st.warning("No widgets selected to confirm.")
    with buttons_col2:
        if st.button("Select All Widgets"): # TODO: bug fix - last widget not selected
            all_widgets = get_all_widgets()
            if all_widgets:
                project.selected_widgets = all_widgets
                st.rerun()
            else:
                st.warning("No widgets available to select.")


def create_csv_download_button(df, filename='pixel_patrol_selected_files.csv', label="📥 Download Data as CSV"):
    """Creates a download button for a DataFrame."""
    csv = df.to_pandas().to_csv(index=False).encode('utf-8')
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime='text/csv',
    )


def choose_widgets(project):
    widgets = get_all_widgets()
    if not widgets:
        widgets = load_widgets()
        set_all_widgets(widgets)
    tabbed_widgets = organize_widgets_by_tab(widgets)
    if tabbed_widgets:
        st.markdown("Choose which widgets you are interested in. You can expand them to check out what they do. These widgets display example data results, they do net represent your own data at this point.")
        selected_widgets = project.selected_widgets
        new_selected_widgets = []
        for tab_name, widgets in zip(tabbed_widgets.keys(), tabbed_widgets.values()):
            st.markdown("### " + tab_name)
            for widget in widgets:
                if st.toggle(widget.name, key=widget.name, value=(not selected_widgets or len(selected_widgets) == 0) or widget.name in selected_widgets):
                    new_selected_widgets.append(widget.name)
        project.selected_widgets = new_selected_widgets
        display_widget_selection_confirmation_buttons(project)


def create_add_folder_button(project):
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([5,1], vertical_alignment="bottom")
    with col1:
        folder_path = st.text_input("Directory location")
    with col2:
        with stylable_container(
            key="container_with_border",
            css_styles=r"""
            button div:before {
                font-family: 'Font Awesome 5 Free';
                content: '\f07c';
                display: inline-block;
                padding-right: 3px;
                vertical-align: middle;
                font-weight: 900;
            }
            """,
        ):
            if st.button(" "):
                # Create and configure tkinter root window
                root = tk.Tk()
                root.withdraw()  # Hide the main window

                try:
                    # Open folder selection dialog
                    folder_path = filedialog.askdirectory(
                        title="Select Dataset Folder",
                        initialdir=os.path.expanduser("~"),  # Start from user's home directory
                        parent=root
                    )

                    # Show the root window again
                    root.deiconify()

                finally:
                    # Ensure the window is properly destroyed
                    root.destroy()
    if folder_path:
        add_new_path_with_subpath_check(str(Path(folder_path)), project)


def add_new_path_with_subpath_check(new_path, project, show_success=True, suppress_warning=False):
    relevant_existing_paths = list(project.paths.keys())

    # Check if the new path is already covered by existing paths (new_path is subpath)
    duplicate_or_subpath = any(is_subpath(new_path, existing) for existing in relevant_existing_paths)
    if duplicate_or_subpath:
        if not suppress_warning:
            st.warning(
                "The path you are trying to add is already imported or is a subpath of an existing imported path. "
                "It won't be added again."
            )
        return

    # Check if the new path is a superpath (new_path contains existing paths)
    paths_to_remove = [existing for existing in relevant_existing_paths if is_superpath(new_path, existing)]
    if paths_to_remove:
        for path in paths_to_remove:
            project.paths.pop(path, None)
            project.path_summaries.pop(path, None)
        if not suppress_warning:
            st.warning(
                f"The new path you added contains existing paths, which have been removed: "
                f"{', '.join(paths_to_remove)}"
            )

    with st.spinner(f"Processing dataset: {new_path}..."):
        add_new_path(new_path, project)
        if show_success:
            st.success(f"Dataset added: {new_path}")


def create_sidebar(project, current_step):
    # Dataset Management and Selectors
    with st.sidebar:
        image_path = files("pixel_patrol.data.img").joinpath("prevalidation.png")
        st.image(image_path)
        st.title("Pixel Patrol")

        display_step_buttons(project, current_step)
        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        display_disclaimer()


def display_disclaimer():
    st.info(
        """
        **Disclaimer**: This application is a prototype. The data presented may be inaccurate and is intended solely for conceptual exploration.
        """,
    )


def display_fast_mode(df):
    fast_mode = st.toggle("Fast Mode")
    st.text(
        "In fast mode, a fixed random number of files will be picked in each selected folder. The processing will only run on these files, in contrast to processing all files if Fast Mode is disabled.")
    if fast_mode:
        number = st.number_input(
            "Number of random files to be picked", value=5, placeholder="Type a number..."
        )
        df = apply_fast_mode(df, number)
    return df

def display_widgets_as_tab(tabbed_widgets, data_frame):
    if data_frame is None or data_frame.is_empty():
        st.warning("No test data found.")
        return
    if tabbed_widgets:
        dataframe_pandas = data_frame.to_pandas()
        tab_objects = st.tabs(tabbed_widgets.keys())
        for tab, tab_key in zip(tab_objects, tabbed_widgets):
            widgets = tabbed_widgets[tab_key]
            with tab:
                for widget in widgets:
                    if hasattr(widget.__class__, "run"):
                        widget.run(dataframe_pandas)
                    else:
                        with st.expander(widget.name, expanded=True):
                            options = widget.options(data_frame)
                            widget.render(data_frame, **options)
                if str(tab) == str(DefaultTabs.SUMMARY.value):
                    display_summaries(data_frame, tabbed_widgets)



def display_widgets_as_report(tabbed_widgets, data_frame):
    if data_frame is None or data_frame.is_empty():
        st.warning("No test data found.")
        return
    if tabbed_widgets:
        dataframe_pandas = data_frame.to_pandas()

        for tab, widgets in zip(tabbed_widgets.keys(), tabbed_widgets.values()):

            st.header(tab)
            for widget in widgets:
                if hasattr(widget.__class__, "run"):
                    widget.run(dataframe_pandas)
                else:
                    # options = widget.options(data_frame)
                    # widget.render(data_frame, **options)
                    st.markdown(f"### {widget.name}")
                    widget.render(data_frame)

            if str(tab) == str(DefaultTabs.SUMMARY.value):
                display_summaries(data_frame, tabbed_widgets)


def display_summaries(data_frame, tabbed_widgets):
    st.markdown("#### Widget summaries")
    for widgets in tabbed_widgets.values():
        for widget in widgets:
            if hasattr(widget.__class__, "summary"):
                widget.summary(data_frame)


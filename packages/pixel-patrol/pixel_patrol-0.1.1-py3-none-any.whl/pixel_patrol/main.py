from pathlib import Path

import polars as pl
import streamlit as st
import yaml

from pixel_patrol.project import Project
from pixel_patrol.utils.session import (
    get_project, initialize_session_state, PrevalidationStep, get_current_step, set_current_step,
    is_debug_mode, KEY_TEST_DATA_DIR, get_all_widgets
)
from pixel_patrol.utils.ui import (
    choose_matplotlib_colormap, configure_layout, create_sidebar,
    create_add_folder_button, choose_widgets,
    add_new_path_with_subpath_check, display_imported_dirs_info,
    display_widgets_as_report, display_widgets_as_tab, step_is_disabled, display_disclaimer
)
from pixel_patrol.utils.utils import (
    preprocess_files, process_files,
    get_cache_dir, aggregate_folder_dataframes, count_file_extensions, load_dataframe_images,
    store_all_dataframe_images_to_cache, set_colors, cache_all_project_path_structures, add_new_path,
    file_structure_cache_missing
)
from pixel_patrol.utils.widget import (
    get_required_columns, load_or_get_project_widgets, organize_widgets_by_tab
)


def load_config(config_path: str = "../config.yaml"):
    config = {}
    config_file = Path(__file__).parent / config_path
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            st.error(f"Error parsing YAML file: {e}")
    else:
        st.error(f"Configuration file `{config_path}` not found.")
    return config


def select_project(project):
    # Check if a project name is provided in the URL query parameters
    placeholder = st.empty()
    with placeholder.container():
        projects_dir = get_cache_dir() / "projects"
        projects_dir.mkdir(exist_ok=True)
        existing_projects = [p.stem for p in projects_dir.glob("*.yml")]
        options = ["New Project"] + existing_projects
        selected = st.selectbox("Select Project", options, key="project_select")

        if selected == "New Project":
            new_project_name = st.text_input("Enter New Project Name", key="new_project_name")
            if new_project_name and st.button("Confirm", key="confirm_new"):
                if new_project_name in existing_projects:
                    st.error("Project already exists. Choose a different name.")
                else:
                    project.name = new_project_name
                    project.selected_widgets = [w.name for w in load_or_get_project_widgets(project)]
                    st.query_params["project"] = project.name
                    placeholder.empty()
        else:
            if st.button("Confirm", key="confirm_existing"):
                set_active_project(project, selected)
                st.rerun()

    return project


def set_active_project(project, project_name):
    if project is not None and project.name == project_name:
        # project is in session, do not load from disk
        return
    project.name = project_name
    if project.exists():
        project.load_project_from_yml(project_name)
    for path in project.paths:
        add_new_path(path, project)
    project.selected_widgets = [w.name for w in load_or_get_project_widgets(project)]
    load_dataframe_images(project)
    st.query_params["project"] = project_name


def reset_project_selection():
    st.session_state.project.reset()
    st.query_params.clear()
    set_current_step(PrevalidationStep.DEFINE_PROJECT)
    st.rerun()


def get_test_data_dir(config):
    test_data_dir = config.get(KEY_TEST_DATA_DIR, "test_data")
    return Path(__file__).parent / test_data_dir


def load_test_data(test_data_dir, project):
    """Load all datasets from the test_data directory."""
    if not test_data_dir.exists():
        st.error(f"Test data directory `{test_data_dir}` does not exist.")
        return

    # Iterate over each dataset directory in test_data
    for dataset_dir in test_data_dir.iterdir():
        if dataset_dir.is_dir():
            # Check if the dataset is already loaded to prevent duplication
            if not any(d['path'] == str(dataset_dir) for d in st.session_state.project.paths):
                add_new_path_with_subpath_check(str(dataset_dir), project)
    st.success(f"Test data loaded from `{test_data_dir}`.")


def create_dataframe_images_from_file_structure(project):
    # project.paths is now a dict[path: df_structure]
    dataframe_images = aggregate_folder_dataframes(project.paths)
    dataframe_images = dataframe_images.filter(pl.col("type").eq("file"))

    selected_file_types = project.settings.get("selected_file_extensions", [])
    if selected_file_types:
        # Convert selected_file_types to lowercase for case-insensitive comparison
        selected_file_types = [ft.lower() for ft in selected_file_types]
        dataframe_images = dataframe_images.filter(
            pl.col("file_extension").is_in(selected_file_types)
        )

    dataframe_images = preprocess_files(dataframe_images)
    return dataframe_images


def display_project_settings(config, project):
    st.header("Project Settings")

    preselected_file_extensions = [
        ft.lower() for ft in
        (project.settings.get("selected_file_extensions") or config.get('preselected_file_extensions', []))
    ]

    extension_info = count_file_extensions(project.paths)
    if not extension_info:
        if "all_files" in extension_info and extension_info["all_files"] == 0:
            st.warning("No files found in any imported directories.")
        else:
            st.warning("No files with valid extensions found in these directories.")
        return

    total_file_count = extension_info.pop("all_files", 0)
    if not extension_info:
        st.warning("No valid file extensions found in these directories.")
        return

    st.subheader("Choose Which File Extensions to Include:")
    options = [f".{ext} ({extension_info[ext]})" for ext in sorted(extension_info.keys())]
    default = [f".{ext} ({extension_info[ext]})" for ext in preselected_file_extensions if ext in extension_info]
    selected_options = st.multiselect("Select file extensions:", options, default=default)

    # Extract the selected extensions (remove the count from the label)
    selected_file_extensions = [opt.split(" ")[0][1:] for opt in selected_options]

    project.settings["selected_file_extensions"] = selected_file_extensions

    chosen_count = sum(extension_info[ext] for ext in selected_file_extensions)
    st.info(f"Chosen {chosen_count} out of {total_file_count} total files.")

    # display_fast_mode(project)

    cmap = project.settings.get("cmap", 'rainbow')
    cmap = choose_matplotlib_colormap(cmap)
    project.settings["cmap"] = cmap

    example_images = st.slider("Number of example images", min_value=1, max_value=15, value=9)
    project.settings["example_images"] = example_images
    st.write(f"Number of example images: {example_images}")

    if st.button("Confirm Settings and Process Files"):
        with st.spinner("Processing ongoing..."):

            if project.has_project_config_changed() or file_structure_cache_missing(project):
                project.save_project_to_yml()
                st.info("Project configuration has changed. All caches will be updated.")
                cache_all_project_path_structures(project)

            to_be_processed_files = load_dataframe_images(project)
            if to_be_processed_files is None:
                # If no cache was available, create from scratch
                to_be_processed_files = create_dataframe_images_from_file_structure(project)

            to_be_processed_files = set_colors(to_be_processed_files, project)
            widgets = load_or_get_project_widgets(project)
            columns = get_required_columns(widgets)
            processed_files = process_files(to_be_processed_files, columns)

            project.df_images = processed_files
            store_all_dataframe_images_to_cache(processed_files)

        st.balloons()
        set_current_step(PrevalidationStep.REPORT)
        st.rerun()


def create_main_section(config, project: Project, current_step: PrevalidationStep):

    if step_is_disabled(project, current_step):
        set_current_step(PrevalidationStep.DEFINE_PROJECT)
        st.rerun()

    match current_step:
        case PrevalidationStep.DEFINE_PROJECT:
            if project.name is None:
                st.header("Define Project")
                project = select_project(project)
            if project.name is None:
                return

            st.header(f"Project: {project.name}")

            if st.button("Select a different project", key="reset_project_main"):
                reset_project_selection()

            st.subheader("Directory Selection")
            if project.paths:
                for directory in project.paths:
                    add_new_path_with_subpath_check(directory, project, show_success=False, suppress_warning=True)
                st.success("Project directories loaded from configuration.")

            select_directories(config, project)
            if st.button("Confirm Directory Selection", key="confirm_dirs"):
                if not project.paths:
                    st.warning("Please add at least one valid directory with files or folders.")
                else:
                    set_current_step(PrevalidationStep.SELECT_WIDGETS)
                    st.rerun()

        case PrevalidationStep.SELECT_WIDGETS:
            choose_widgets(project)

        case PrevalidationStep.SETTINGS:
            display_project_settings(config, project)

        case PrevalidationStep.REPORT:
            project = st.session_state.project
            st.toggle(
                "Print Mode",
                value=project.is_report_mode,
                on_change=lambda: setattr(project, "is_report_mode", not project.is_report_mode)
            )
            enabled_widgets = [w for w in get_all_widgets() if w.name in project.selected_widgets]
            tabbed_widgets = organize_widgets_by_tab(enabled_widgets)

            if project.is_report_mode:
                display_widgets_as_report(tabbed_widgets, project.df_images.filter(pl.col("type") == "file"))
            else:
                display_widgets_as_tab(tabbed_widgets, project.df_images.filter(pl.col("type") == "file"))


def select_directories(config, project):
    if is_debug_mode():
        test_data_dir = get_test_data_dir(config)
        load_test_data(test_data_dir, project)
        st.header("Debug Mode Enabled")
        st.write(f"Using test data from `{test_data_dir}`")
    else:
        create_add_folder_button(project)
        display_imported_dirs_info(project)


def process_query(project):
    query_params = st.query_params
    if "project" in query_params and query_params["project"]:
        set_active_project(project, query_params["project"])
    if "view" in query_params and query_params["view"]:
        view = query_params["view"]
        view_step = PrevalidationStep[view]
        if view_step:
            set_current_step(view_step)


def main():
    config = load_config()
    initialize_session_state(config)
    project = get_project()
    configure_layout(project)
    process_query(project)
    current_step = get_current_step()
    if not project.is_report_mode:
        create_sidebar(project, current_step)
    else:
        display_disclaimer()
    create_main_section(config, project, current_step)


if __name__ == "__main__":
    main()

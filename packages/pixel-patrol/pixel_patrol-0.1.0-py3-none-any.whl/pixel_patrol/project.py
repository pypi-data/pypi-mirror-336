from typing import Dict, List, Optional, Any

import polars as pl
import streamlit as st
import yaml

from pixel_patrol.utils.utils import hash_file_path, get_projects_dir


class Project:
    def __init__(self):
        # Session state keys
        self._session_keys = {
            "name": "project_name",
            "yml": "project_yml",
            "paths": "imported_paths",
            "path_summaries": "path_summaries",
            "df_images": "df_images",
            "selected_widgets": "selected_widgets",
            "settings": "project_settings",
            "is_report_mode": "is_report_mode",
        }

    # --- Properties for saved state (yml) ---
    @property
    def yml(self) -> Dict[str, Any]:
        """The saved state of the project (from the YAML file)."""
        return st.session_state.get(self._session_keys["yml"], {})

    @yml.setter
    def yml(self, value: Dict[str, Any]):
        """Update the saved state of the project."""
        st.session_state[self._session_keys["yml"]] = value

    # --- Properties for runtime state ---
    @property
    def name(self) -> Optional[str]:
        """The runtime state of the project name."""
        return st.session_state.get(self._session_keys["name"])

    @name.setter
    def name(self, value: Optional[str]):
        """Update the runtime state of the project name."""
        st.session_state[self._session_keys["name"]] = value

    @property
    def paths(self) -> Dict[str, pl.DataFrame]:
        """The runtime state of imported paths (full structure dfs)."""
        return st.session_state.get(self._session_keys["paths"], {})

    @paths.setter
    def paths(self, value: Dict[str, pl.DataFrame]):
        """Update the runtime state of imported paths."""
        st.session_state[self._session_keys["paths"]] = value

    @property
    def path_summaries(self) -> Dict[str, pl.DataFrame]:
        return st.session_state.get("path_summaries", {})

    @path_summaries.setter
    def path_summaries(self, value: Dict[str, pl.DataFrame]):
        st.session_state["path_summaries"] = value

    @property
    def df_images(self) -> pl.DataFrame:
        """The runtime state of the dataframe for images."""
        return st.session_state.get(self._session_keys["df_images"], pl.DataFrame())

    @df_images.setter
    def df_images(self, value: pl.DataFrame):
        """Update the runtime state of the dataframe for images."""
        st.session_state[self._session_keys["df_images"]] = value

    @property
    def selected_widgets(self) -> Optional[List[Any]]:
        """The runtime state of selected widgets."""
        return st.session_state.get(self._session_keys["selected_widgets"])

    @selected_widgets.setter
    def selected_widgets(self, value: Optional[List[Any]]):
        """Update the runtime state of selected widgets."""
        st.session_state[self._session_keys["selected_widgets"]] = value

    @property
    def settings(self) -> Dict[str, Any]:
        """The runtime state of project settings."""
        return st.session_state.get(self._session_keys["settings"], {})

    @settings.setter
    def settings(self, value: Dict[str, Any]):
        """Update the runtime state of project settings."""
        st.session_state[self._session_keys["settings"]] = value

    @property
    def is_report_mode(self) -> bool:
        """The runtime state of report mode."""
        return st.session_state.get(self._session_keys["is_report_mode"], False)

    @is_report_mode.setter
    def is_report_mode(self, value: bool):
        """Update the runtime state of report mode."""
        st.session_state[self._session_keys["is_report_mode"]] = value

    # --- Helper Methods ---
    def reset(self):
        """Reset the project to its initial state."""
        self.name = None
        self.yml = {}
        self.paths = {}
        self.path_summaries = {}
        self.df_images = pl.DataFrame()
        self.selected_widgets = None
        self.settings = {}
        self.is_report_mode = False

    def load_project_from_yml(self, project_name: str):
        """Load a project from its YAML file and initialize the runtime state."""
        self.yml = self._read_yml(project_name)
        self.name = self.yml.get("name")
        self.paths = self.yml.get("paths", [])
        self.selected_widgets = self.yml.get("selected_widgets")
        self.settings = self.yml.get("settings", {})

    def exists(self):
        return Project.get_project_filepath(self.name).exists()

    def save_project_to_yml(self):
        if self.name:
            paths_hashed = {path: hash_file_path(path) for path in self.paths.keys()}
            widget_names = [w for w in (self.selected_widgets or [])]
            self.yml = {
                "name": self.name,
                "paths": paths_hashed,
                "selected_widgets": widget_names,
                "settings": self.settings,
            }
            self._write_yml()

    def _write_yml(self):
        """Save the yml to a YAML file."""
        projects_dir = get_projects_dir()
        projects_dir.mkdir(exist_ok=True)
        filepath = projects_dir / f"{self.name}.yml"
        with open(filepath, "w") as f:
            yaml.safe_dump(self.yml, f)

    @staticmethod
    def _read_yml(project_name: str) -> Dict[str, Any]:
        """Load the yml from a YAML file."""
        filepath = Project.get_project_filepath(project_name)
        if filepath.exists():
            with open(filepath, "r") as f:
                return yaml.safe_load(f)
        return {}

    @staticmethod
    def get_project_filepath(project_name):
        projects_dir = get_projects_dir()
        filepath = projects_dir / f"{project_name}.yml"
        return filepath

    def has_project_config_changed(self) -> bool:
        """
        Check if the project configuration has changed compared to the saved YAML.
        Compares:
        - Paths: Only the keys (directory paths).
        - Selected Widgets: The list of selected widgets.
        - Settings: Only the `selected_file_extensions` list.
        """
        saved_yml = self.yml

        # Compare paths (only keys)
        saved_paths = set(saved_yml.get("paths", {}).keys())
        current_paths = set(self.paths.keys())
        if saved_paths != current_paths:
            return True

        # Compare selected widgets
        saved_widgets = set(saved_yml.get("selected_widgets", []))
        current_widgets = set(self.selected_widgets or [])
        if saved_widgets != current_widgets:
            return True

        # Compare selected file extensions in settings
        saved_settings = saved_yml.get("settings", {})
        current_settings = self.settings
        if saved_settings != current_settings:
            return True

        return False

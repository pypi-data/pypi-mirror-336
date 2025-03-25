import os
import polars as pl
import streamlit as st
from enum import Enum
from typing import Dict

from pixel_patrol.project import Project


# Constants for session state keys
KEY_PROJECT = "project"
KEY_CURRENT_STEP = "current_step"
KEY_DEBUG_MODE = "debug_mode"
KEY_ALL_WIDGETS = "all_widgets"
KEY_TEST_TABLE = "test_table"
KEY_TEST_DATA_DIR = "test_data_dir"
KEY_TEST_TABLE_NAME = "test_table_name"
KEY_PATH_SUMMARIES = "path_summaries"


class PrevalidationStep(Enum):
    DEFINE_PROJECT = 0
    SELECT_WIDGETS = 1
    SETTINGS = 2
    REPORT = 3


def initialize_session_state(config):
    """Initialize all session state variables, including the Project object."""
    if KEY_PROJECT not in st.session_state:
        st.session_state[KEY_PROJECT] = Project()
    if KEY_PATH_SUMMARIES not in st.session_state:
        st.session_state[KEY_PATH_SUMMARIES] = {}
    if KEY_DEBUG_MODE not in st.session_state:
        st.session_state[KEY_DEBUG_MODE] = config.get(KEY_DEBUG_MODE, False)
    if KEY_ALL_WIDGETS not in st.session_state:
        st.session_state[KEY_ALL_WIDGETS] = None
    if KEY_TEST_TABLE not in st.session_state:
        st.session_state[KEY_TEST_TABLE] = None


def get_project():
    """Get the Project object from session state."""
    return st.session_state.get(KEY_PROJECT)


def get_path_summaries() -> Dict[str, pl.DataFrame]:
    return st.session_state.get(KEY_PATH_SUMMARIES, {})


def set_path_summaries(value: Dict[str, pl.DataFrame]):
    st.session_state[KEY_PATH_SUMMARIES] = value


def set_current_step(step: PrevalidationStep):
    st.session_state[KEY_CURRENT_STEP] = step.value
    st.query_params["view"] = step.name


def get_current_step():
    if KEY_CURRENT_STEP not in st.session_state:
        st.session_state[KEY_CURRENT_STEP] = PrevalidationStep.DEFINE_PROJECT.value
    current_step = PrevalidationStep(st.session_state[KEY_CURRENT_STEP])
    return current_step


def get_all_widgets():
    """Get all widgets from session state."""
    return st.session_state.get(KEY_ALL_WIDGETS)


def set_all_widgets(all_widgets):
    """Set all widgets in session state."""
    st.session_state[KEY_ALL_WIDGETS] = all_widgets


def get_test_dataframe():
    """Get the test dataframe from session state."""
    return st.session_state.get(KEY_TEST_TABLE)


def ensure_test_table_existence(config):
    """Ensure the test table exists and load it into session state."""
    test_data_dir = config.get(KEY_TEST_DATA_DIR, "test_data")
    test_table_name = config.get(KEY_TEST_TABLE_NAME, "test.parquet")

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_table_path = os.path.join(current_dir, test_data_dir, test_table_name)

    if not os.path.exists(test_table_path):
        st.error(f"Test table not found at {test_table_path}")
    else:
        test_dataframe = pl.read_parquet(test_table_path)
        st.session_state[KEY_TEST_TABLE] = test_dataframe


def is_debug_mode():
    """Check if debug mode is enabled."""
    return st.session_state.get(KEY_DEBUG_MODE, False)
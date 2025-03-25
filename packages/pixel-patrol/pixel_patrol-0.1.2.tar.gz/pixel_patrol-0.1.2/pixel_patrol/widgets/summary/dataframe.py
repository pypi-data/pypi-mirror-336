from typing import List

import polars as pl
import streamlit as st

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class DataFrameWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.SUMMARY.value

    @property
    def name(self) -> str:
        return "Dataframe Viewer"

    def required_columns(self) -> List[str]:
        return []

    def render(self, data_frame: pl.DataFrame):
        limit_df_per_condition = 50
        st.write(f"Limited to {limit_df_per_condition} files per folder.")
        data_frame_limited = data_frame.group_by("selected_folder", maintain_order=True).head(
            limit_df_per_condition)
        st.write(data_frame_limited)
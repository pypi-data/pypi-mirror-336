from typing import List

import streamlit as st
import os
import pandas as pd

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
from pixel_patrol.utils.plot import create_bar_chart, create_bar_chart_go_w_pattern
from pixel_patrol.utils.widget import output_ratio_of_files_with_column_info

class DimOrderWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.METADATA.value

    def required_columns(self) -> List[str]:
        return ["metadata"]

    def run(self, selected_files_df: pd.DataFrame):
        with st.expander("Dim Order Distribution", expanded=False):
            # Calculate and display the ratio of files with 'dim_order' information
            dim_order_present = output_ratio_of_files_with_column_info(
                selected_files_df,
                column_name='dim_order',
                display_name='Dim Order'
            )

            # Optionally include additional information (e.g., file type)
            include_file_extension = st.checkbox("Include File Type Information", value=False, key="dim_order_include_file_extension")

            # Prepare the data for plotting
            plot_data = selected_files_df[dim_order_present].copy()
            plot_data['value'] = 1  # Each file counts as 1

            if include_file_extension:
                plot_data['selected_folder_base'] = plot_data['selected_folder'].apply(lambda x: os.path.basename(x))
                fig = create_bar_chart_go_w_pattern(
                    df=plot_data,
                    x_col="dim_order",
                    sub_x_col="selected_folder_base",
                    pattern_col="file_extension",
                    value_col="value",
                    title="Dim Order Distribution",
                    hover_cols=['name', 'dim_order', 'file_extension', 'selected_folder'],
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = create_bar_chart(
                    df=plot_data,
                    x='dim_order',
                    title="Dim Order Distribution",
                    x_title="Dim Order",
                    y_title="Number of Files",
                    key_suffix="dim_order",
                    hover_columns=['name', 'dim_order', 'file_extension'],
                )
                st.plotly_chart(fig, use_container_width=True)
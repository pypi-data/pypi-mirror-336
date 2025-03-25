from typing import List

import streamlit as st

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
from pixel_patrol.utils.plot import create_bar_chart, create_bar_chart_go_w_pattern
from pixel_patrol.utils.widget import output_ratio_of_files_with_column_info
import os


class DataTypeWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.METADATA.value

    def required_columns(self) -> List[str]:
        return ["metadata"]

    def run(self, selected_files_df):
        with st.expander("Data Type Distribution", expanded=False):

            dtype_present = output_ratio_of_files_with_column_info(selected_files_df, 'dtype', 'Data Type')

            include_file_extension = st.checkbox("Include File Type Information", value=False, key="dtype_include_file_extension")

            plot_data = selected_files_df[dtype_present].copy()
            plot_data['value'] = 1

            if include_file_extension:
                plot_data[f'selected_folder_base'] = plot_data['selected_folder'].apply(lambda x: os.path.basename(x))
                fig = create_bar_chart_go_w_pattern(
                    df=plot_data,
                    x_col="dtype",
                    sub_x_col="selected_folder_base",
                    pattern_col="file_extension",
                    value_col="value",
                    title="Data Type Distribution",
                    hover_cols=['name', 'dtype', 'file_extension', 'selected_folder'],
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = create_bar_chart(
                    plot_data,
                    x='dtype',
                    title="Data Type Distribution",
                    x_title="Data Type",
                    key_suffix="dtype",
                    hover_columns=['name', 'dtype', 'file_extension'],
                )

                st.plotly_chart(fig, use_container_width=True)

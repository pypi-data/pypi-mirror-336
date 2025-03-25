from typing import List

import streamlit as st
import pandas as pd

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
from pixel_patrol.utils.widget import output_ratio_of_files_with_column_info
from pixel_patrol.utils.plot import create_histogram_chart, create_bubble_chart, create_heatmap_chart, get_chart_type


class DimSizeWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.METADATA.value

    def required_columns(self) -> List[str]:
        return ["metadata"]

    def run(self, selected_files_df: pd.DataFrame):

        with st.expander("Size Distribution", expanded=False):
            st.markdown("### Size Distribution Across Dimensions")

            with st.container():

                x_col, y_col = "x_size", "y_size"

                col_x_present = output_ratio_of_files_with_column_info(
                    selected_files_df,
                    column_name=x_col,
                    display_name=x_col.replace('_', ' ').title(),
                    treat_one_as_null=True
                )
                col_y_present = output_ratio_of_files_with_column_info(
                    selected_files_df,
                    column_name=y_col,
                    display_name=y_col.replace('_', ' ').title(),
                    treat_one_as_null=True
                )

                plot_data = selected_files_df[col_x_present & col_y_present] # TODO: Is it ok to assume those come together?
                # TODO: What if only one of them is present?

                if plot_data.empty:
                    st.info(f"No valid data to plot for X and Y dimension sizes.")
                else:
                    st.markdown(f"#### X and Y Size Distribution")

                    chart_type = get_chart_type(f"xy_size_chart_type", ["Bubble", "Heatmap"])

                    plot_title = "Distribution of X and Y Dimension Sizes"

                    if chart_type == "Bubble":
                        fig = create_bubble_chart(
                            df=plot_data,
                            x=x_col,
                            y=y_col,
                            title=plot_title,
                            x_title=x_col.replace('_', ' ').title(),
                            y_title=y_col.replace('_', ' ').title(),
                            key_suffix=f"size_distribution_XY_size",
                        )
                    else:
                        fig = create_heatmap_chart(
                            df=plot_data,
                            x=x_col,
                            y=y_col,
                            title=plot_title,
                            x_title=x_col.replace('_', ' ').title(),
                            y_title=y_col.replace('_', ' ').title(),
                            key_suffix=f"size_distribution_XY_size",
                        )

                    st.plotly_chart(fig, use_container_width=True)



            selected_columns = select_dims_to_display(selected_files_df)

            if not selected_columns:
                st.info("Please select dims to visualize their size.")
            else:
                for column in selected_columns:
                    with st.container():

                        col_present = output_ratio_of_files_with_column_info(
                            selected_files_df,
                            column_name=column,
                            display_name=column.replace('_', ' ').title(),
                            treat_one_as_null=True
                        )

                        plot_data = selected_files_df[col_present]

                        if plot_data.empty:
                            st.info(f"No valid data to plot for {column.replace('_', ' ').title()}.")
                            continue

                        st.markdown(f"#### {column.replace('_', ' ').title()}")

                        if column == 's_size':
                            st.info(f"Exists in color images - Usually RGB/RGBA.")

                        fig = create_histogram_chart(
                            df=plot_data,
                            x=column,
                            title=f"Distribution of {column.replace('_', ' ').title()}",
                            x_title=column.replace('_', ' ').title(),
                            y_title="Number of Files",
                            key_suffix=f"size_distribution_{column}",
                        )

                        # TODO: Fix legend over x axis if X tick names go low. Maybe we don't show all ticks in this case?
                        # TODO: Check why we have z = 1000 for an image

                        st.plotly_chart(fig, use_container_width=True)


def select_dims_to_display(selected_files_df):
    numerical_columns = ['y_size', 'x_size', 'z_size', 't_size', 'c_size', 's_size', 'n_images']
    available_columns = [col for col in numerical_columns if col in selected_files_df.columns]
    missing_columns = [col for col in numerical_columns if col not in selected_files_df.columns]
    if missing_columns:
        st.warning(f"The following columns are missing: {', '.join(missing_columns)}")
    selected_columns = st.multiselect(
        "Select Size Columns to Visualize",
        options=available_columns,
        default=[col for col in available_columns if col not in ['y_size', 'x_size']],
        key="dims_size_distribution"
    )
    return selected_columns

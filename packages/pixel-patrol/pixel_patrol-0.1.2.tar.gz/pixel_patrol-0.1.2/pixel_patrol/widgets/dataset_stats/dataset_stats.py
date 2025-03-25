from pathlib import Path
from typing import List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import streamlit as st
from scipy.stats import mannwhitneyu

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
import itertools
import statsmodels.stats.multitest as smm
from scipy.stats import mannwhitneyu


class DatasetStatsWidget(ImagePrevalidationWidget):
    @property
    def tab(self) -> str:
        return DefaultTabs.DATASET_STATS.value

    def required_columns(self) -> List[str]:
        return ["mean", "median", "std", "min", "max"]

    def run(self, selected_files_df: pd.DataFrame) -> None:
        with st.expander("Pixel Value Statistics", expanded=True):
            self.plot_basic_2d_image_stats(selected_files_df)

    def plot_basic_2d_image_stats(self, selected_files_df: pd.DataFrame) -> None:
        """Plot the basic stats, directly extracted from the images of each selected folder."""
        if selected_files_df.empty:
            st.warning("No images found in the selected folders.")
            return

        selected_files_df["selected_folder_short"] = selected_files_df[
            "selected_folder_short"
        ].apply(lambda x: str(Path(x).name))

        # Dropdown to select the value to plot
        value_to_plot = st.selectbox(
            label="Select value to plot",
            # options=all columns containing any strings of the requested_columns() list
            options=[
                col
                for col in selected_files_df.columns
                if any(x in col for x in self.required_columns())
            ],
            index=0,
        )

        # Create the strip plot with overlaid box plots
        chart = px.strip(
            selected_files_df,
            x="selected_folder_short",
            y=value_to_plot,
            labels={"selected_folder_short": ""},
            color="color",
            stripmode="overlay",
            hover_data={
                value_to_plot: True,
                "color": False,
                "selected_folder_short": False,
            },
            hover_name="name",
        )
        # Remove the legend from the strip markers
        chart.update_traces(showlegend=False)

        # Add boxplots to the stripplot, disabling hover on the boxplots
        for selected_folder_short in selected_files_df[
            "selected_folder_short"
        ].unique():
            data = selected_files_df[
                selected_files_df["selected_folder_short"] == selected_folder_short
            ][value_to_plot]
            chart.add_trace(
                go.Box(
                    y=data,
                    name=selected_folder_short,
                    marker_color=selected_files_df[
                        selected_files_df["selected_folder_short"]
                        == selected_folder_short
                    ]["color"].iloc[0],
                    showlegend=True,
                )
            )

        # Reorder traces so that box plot elements are drawn below the strip markers.
        box_traces = [trace for trace in chart.data if trace.type == "box"]
        non_box_traces = [trace for trace in chart.data if trace.type != "box"]
        chart.data = box_traces + non_box_traces

        # ---------------------------------------------------------------------
        # Add statistical annotations using pairwise Mann-Whitney U tests with Bonferroni correction

        # Determine groups and compute all pairwise comparisons
        groups = list(selected_files_df["selected_folder_short"].unique())

        # if only one group is selected, do not show the statistics
        if len(groups) > 1:
            comparisons = list(itertools.combinations(groups, 2))
            p_values = []
            for group1, group2 in comparisons:
                data1 = selected_files_df[
                    selected_files_df["selected_folder_short"] == group1
                ][value_to_plot]
                data2 = selected_files_df[
                    selected_files_df["selected_folder_short"] == group2
                ][value_to_plot]
                # Perform two-sided test (default alternative is "two-sided")
                stat_val, p_val = mannwhitneyu(data1, data2)
                p_values.append(p_val)

            # Apply Bonferroni correction
            reject, pvals_corrected, _, _ = smm.multipletests(
                p_values, alpha=0.05, method="bonferroni"
            )

            # Ensure consistent ordering on the x-axis
            group_order = groups
            chart.update_layout(
                xaxis=dict(categoryorder="array", categoryarray=group_order)
            )
            positions = {group: i for i, group in enumerate(group_order)}
            n_groups = len(group_order)

            # Calculate a y-offset based on the range of the values
            overall_y_min = selected_files_df[value_to_plot].min()
            overall_y_max = selected_files_df[value_to_plot].max()
            y_offset = (overall_y_max - overall_y_min) * 0.05
            # If there are more than 3 groups, just compare adjacent groups and use a higher offset.
            if len(group_order) > 3:
                comparisons = [
                    (group_order[i], group_order[i + 1])
                    for i in range(len(group_order) - 1)
                ]
                y_offset = (overall_y_max - overall_y_min) * 0.2
            else:
                # Also use adjacent comparisons for consistency
                comparisons = [
                    (group_order[i], group_order[i + 1])
                    for i in range(len(group_order) - 1)
                ]

            # Compute p-values for adjacent comparisons
            p_values = []
            for group1, group2 in comparisons:
                data1 = selected_files_df[
                    selected_files_df["selected_folder_short"] == group1
                ][value_to_plot]
                data2 = selected_files_df[
                    selected_files_df["selected_folder_short"] == group2
                ][value_to_plot]
                stat_val, p_val = mannwhitneyu(data1, data2)
                p_values.append(p_val)

            # Apply Bonferroni correction for the number of comparisons
            reject, pvals_corrected, _, _ = smm.multipletests(
                p_values, alpha=0.05, method="bonferroni"
            )

            # Define a horizontal offset for spacing between comparisons
            x_offset = 0.1

            # For categorical x-axis, use numeric positions (0, 1, 2, …) based on group_order
            # positions was defined earlier: positions = {group: i for i, group in enumerate(group_order)}
            # n_groups = len(group_order)

            # Add bracket annotations for each adjacent comparison
            for (group1, group2), p_corr in zip(comparisons, pvals_corrected):
                if p_corr < 0.001:
                    sig = "***"
                elif p_corr < 0.01:
                    sig = "**"
                elif p_corr < 0.05:
                    sig = "*"
                else:
                    sig = "ns"

                # Compute the maximum y value for each group (without extra offset)
                y_max1 = selected_files_df[
                    selected_files_df["selected_folder_short"] == group1
                ][value_to_plot].max()
                y_max2 = selected_files_df[
                    selected_files_df["selected_folder_short"] == group2
                ][value_to_plot].max()
                y_bracket = max(y_max1, y_max2) + 1.0

                # Get numeric positions for the groups and adjust with horizontal offset.
                pos1 = positions[group1]
                pos2 = positions[group2]

                # Add a horizontal line connecting the two groups with some space at the ends.
                chart.add_shape(
                    type="line",
                    x0=pos1 + x_offset,
                    x1=pos2 - x_offset,
                    y0=y_bracket,
                    y1=y_bracket,
                    line=dict(color="black"),
                    xref="x",
                    yref="y",
                )
                # Add vertical lines (brackets) at the ends.
                chart.add_shape(
                    type="line",
                    x0=pos1 + x_offset,
                    x1=pos1 + x_offset,
                    y0=y_bracket,
                    y1=y_bracket,
                    line=dict(color="black"),
                    xref="x",
                    yref="y",
                )
                chart.add_shape(
                    type="line",
                    x0=pos2 - x_offset,
                    x1=pos2 - x_offset,
                    y0=y_bracket,
                    y1=y_bracket,
                    line=dict(color="black"),
                    xref="x",
                    yref="y",
                )
                # Compute the midpoint (using the adjusted positions) for the annotation.
                x_mid = (pos1 + x_offset + pos2 - x_offset) / 2
                chart.add_annotation(
                    x=x_mid,
                    y=y_bracket + y_offset / 2,
                    text=sig,
                    showarrow=False,
                    font=dict(color="black"),
                    xref="x",
                    yref="y",
                )

            # Update the x-axis to display the original group labels at the correct positions.
            chart.update_xaxes(
                tickmode="array", tickvals=list(range(n_groups)), ticktext=group_order
            )
        # ---------------------------------------------------------------------

        st.plotly_chart(chart, use_container_width=True)

        # add a markdown text with the description of the test
        st.markdown(
            """
            ### Selectable values to plot: 
            The selected representation of intensities within an image is plotted on the y-axis, while the x-axis shows the different groups (folders) selected.  
            This is calculated on each individual image in the selected folders.    
            Each image is represented by a dot, and the boxplot shows the distribution of the selected value for each group.  

            #### Images with more than 2 dimensions:
            As images can contain multiple time points (t), channels (c), and z-slices (z), the statistics are calculated across all dimensions.   
            To e.g. visualize the distribution of mean intensities across all z-slices and channels at time point t0, please select e.g. `mean_t0`.  
            
            If you want to display the mean intensity across the whole image, select `mean` (without any suffix).

            #### Higher dimensional images that include RGB data: 
            When an image with Z-slices or even time points contains RGB data, the S-dimension is added.   
            Therefore, the RGB color is indicated by the suffix `s0`, `s1`, and `s2` for red, green, and blue channels, respectively.  
            This allows for images with multiple channels, where each channels consists of an RGB image itself, while still being able to select the color channel.
            
            Some images, like TIFF files, are loaded as 5D arrays (T, C, Z, Y, X), even if they are 2D or 3D images. This results in t0, c0, z0 to always be present, even if the image is just 2D.    
            
            The suffixes are as follows:
            - `t`: time point
            - `c`: channel
            - `z`: z-slice
            - `s`: color in RGB images (red, green, blue)
        
            ### Statistical hints:
            The symbols (`*` or `ns`) shown above indicate the significance of the differences between two groups, with more astersisk indicating a more significant difference.   
            The Mann-Whitney U test is applied to compare the distributions of the selected value between pairs of groups.   
            This non-parametric test is used as a first step to assess whether the distributions of two independent samples.   
            The results are adjusted with a Bonferroni correction to account for multiple comparisons, reducing the risk of false positives.  

            Significance levels:
            - `ns`: not significant
            - `*`: p < 0.05
            - `**`: p < 0.01
            - `***`: p < 0.001

            ##### Disclaimer:
            Please do not interpret the results as a final conclusion, but rather as a first step to assess the differences between groups.    
            This may not be the appropriate test for your data, and you should always consult a statistician for a more detailed analysis.
            """
        )

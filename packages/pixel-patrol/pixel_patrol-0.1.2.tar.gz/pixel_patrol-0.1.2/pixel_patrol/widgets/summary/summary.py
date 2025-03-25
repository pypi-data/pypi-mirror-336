from typing import List

import polars as pl
import streamlit as st
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class SummaryWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.SUMMARY.value

    @property
    def name(self) -> str:
        return "Summary"

    def required_columns(self) -> List[str]:
        return ["metadata"]

    def render(self, df: pl.DataFrame):
        unique_folders = df.unique(subset=["selected_folder_short"])
        color_map = {row["selected_folder_short"]: row["color"] for row in unique_folders.to_dicts()}

        # Compute summary metrics aggregated by folder (using selected_folder_short)
        folder_content = df.group_by("selected_folder_short").agg([
            pl.sum("n_images").alias("image_count"),
            (pl.sum("size") / (1024 * 1024)).alias("total_size_mb")  # Convert bytes to MB
        ]).sort("selected_folder_short")

        intensity_stats = df.group_by("selected_folder_short").agg([
            pl.mean("mean").alias("mean_intensity"),
            pl.std("mean").alias("std_intensity"),
            pl.median("mean").alias("median_intensity"),  # Add median intensity
            (pl.quantile("mean", 0.75) - pl.quantile("mean", 0.25)).alias("intensity_iqr")  # Add IQR
        ]).sort("selected_folder_short")

        dimension_stats = df.group_by("selected_folder_short").agg([
            pl.mean("x_size").alias("mean_x_size"),
            pl.std("x_size").alias("std_x_size")
        ]).sort("selected_folder_short")

        # Merge all summaries into one table
        summary = folder_content.join(intensity_stats, on="selected_folder_short") \
            .join(dimension_stats, on="selected_folder_short")

        summary_df = summary.to_pandas()

        # Prepare folder labels and corresponding colors
        folder_labels = summary_df["selected_folder_short"].tolist()
        colors = [color_map.get(folder, "#333333") for folder in folder_labels]

        # Create a combined Plotly figure with 2 rows x 2 columns
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=("Image Count", "Total Size (MB)", "Intensity Distribution")
        )

        # Subplot 1: Image Count per folder
        fig.add_trace(
            go.Bar(
                x=folder_labels,
                y=summary_df["image_count"],
                marker_color=colors
            ),
            row=1, col=1
        )

        # Subplot 2: Total Size (MB) per folder
        fig.add_trace(
            go.Bar(
                x=folder_labels,
                y=summary_df["total_size_mb"],
                marker_color=colors
            ),
            row=1, col=2
        )

        # Subplot 4: Box Plot of Intensity Distribution
        for folder, color in zip(folder_labels, colors):
            folder_data = df.filter(pl.col("selected_folder_short") == folder)
            fig.add_trace(
                go.Box(
                    y=folder_data["mean"].to_list(),
                    name=folder,
                    marker_color=color,
                    boxpoints="outliers",  # Show outliers
                    line=dict(width=1.5),
                ),
                row=1, col=3
            )

        fig.update_layout(
            height=300,
            title_text="Dataset Overview: Folder Comparison",
            showlegend=False,
            margin=dict(l=40, r=40, t=80, b=40)
        )

        # --- Streamlit layout ---

        # --- Generate an Introductory Summary Text ---
        # Aggregate basic folder details: total images, total size (MB) and data types used
        folder_details = df.group_by("selected_folder_short").agg([
            pl.sum("n_images").alias("image_count"),
            (pl.sum("size") / (1024 * 1024)).alias("total_size_mb"),
            pl.col("file_extension").unique().alias("file_types"),
            pl.col("dtype").unique().alias("data_types")
        ]).sort("selected_folder_short")
        folder_details_df = folder_details.to_pandas()

        # Build the introduction text using the aggregated folder details
        intro_text = f"### Dataset Overview\n\nThis dataset compares **{len(folder_details_df)}** folders with each other. " \
                     "Each folder represents a group of images with distinct properties.\n\n"
        for _, row in folder_details_df.iterrows():
            # Convert the data types list to a comma-separated string.
            dt_str = ", ".join(map(str, row['data_types']))
            ft_str = ", ".join(map(str, row['file_types']))
            intro_text += f"- **{row['selected_folder_short']}**: Contains **{row['image_count']}** images, " \
                          f"totaling **{row['total_size_mb']:.1f} MB**. File types: **{ft_str}**. Data types: **{dt_str}**.\n"

        st.markdown(intro_text)

        st.markdown(
            """
            The colors correspond to each folder as defined in the dataset. For more details about the metadata and the dimension standards used (e.g., X: width, Y: height, etc.), please check the [BioIO documentation](https://bioio-devs.github.io/bioio/OVERVIEW.html).
            """
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Aggregated Folder Summary")
        st.dataframe(summary_df)

        st.markdown(
            """
            **Summary Interpretation:**

            - **Folders with higher image counts and total sizes** indicate larger dataset segments.
            - **Mean Intensity** provides insight into the overall brightness; differences might suggest varying imaging conditions.
            - **Median Intensity** represents the middle value of intensity distribution.
            - **Intensity IQR** shows the spread of the middle 50% of intensity values.
            - **Intensity Distribution (Box Plot)** visualizes the spread and outliers in image intensities, helping to identify variability within folders.

            Use this overview to quickly identify which folders might require further investigation or offer the best data quality.
            """
        )

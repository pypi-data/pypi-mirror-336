from typing import List
import polars as pl
import streamlit as st
from plotly import express as px

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class ImageQualityWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.DATASET_STATS.value

    @property
    def name(self) -> str:
        return "Image Quality Comparison"

    def required_columns(self) -> List[str]:
        return [
            "laplacian_variance",
            "tenengrad",
            "brenner",
            "noise_estimation",
            "wavelet_energy",
            "blocking_artifacts",
            "ringing_artifacts",
        ]

    def render(self, selected_files_df: pl.DataFrame):
        """
        Renders a point (strip) plot comparing image quality metrics across folders.

        - When "All" is selected, the widget melts the data to show all required metrics in separate facets.
        - When a specific metric is selected, a single plot shows that metric's values for each file,
          with files grouped by folder (selected_folder).
        """
        req_cols = ["name_short", "selected_folder_short", "color"] + self.required_columns()
        df = selected_files_df.select(req_cols)

        titles = {
            "laplacian_variance": "Laplacian variance",
            "tenengrad": "Tenengrad",
            "brenner": "Brenner",
            "noise_estimation": "Noise estimation",
            "wavelet_energy": "Wavelet energy",
            "blocking_artifacts": "Blocking artifacts",
            "ringing_artifacts": "Ringing Artifacts"
        }

        descriptions = {
            "laplacian_variance": (
                "Measures the sharpness of an image by calculating the variance of the Laplacian. "
                "The Laplacian operator highlights regions of rapid intensity change, such as edges. "
                "A higher value indicates a sharper image with more pronounced edges, while a lower value suggests a blurrier image."
            ),
            "tenengrad": (
                "Reflects the strength of edges in an image by computing the gradient magnitude using the Sobel operator. "
                "Stronger edges typically indicate a clearer and more detailed image. "
                "This metric is often used to assess image focus and sharpness."
            ),
            "brenner": (
                "Captures the level of detail in an image by measuring intensity differences between neighboring pixels. "
                "A higher Brenner score indicates more fine details and textures, while a lower score suggests a smoother or blurrier image. "
                "This metric is particularly useful for evaluating image focus."
            ),
            "noise_estimation": (
                "Estimates the level of random noise present in an image. "
                "Noise can appear as graininess or speckles and is often caused by low light conditions or sensor limitations. "
                "A higher noise level can reduce image clarity and make it harder to distinguish fine details."
            ),
            "wavelet_energy": (
                "Summarizes the amount of high-frequency detail in an image using wavelet transforms. "
                "Wavelets decompose an image into different frequency components, and the energy in the high-frequency bands reflects fine details and textures. "
                "A higher wavelet energy indicates more intricate details, while a lower value suggests a smoother image."
            ),
            "blocking_artifacts": (
                "Detects compression artifacts known as 'blocking,' which occur when an image is heavily compressed (e.g., in JPEG format). "
                "Blocking artifacts appear as visible 8x8 pixel blocks, especially in smooth or gradient regions. "
                "A higher score indicates more severe blocking artifacts, which can degrade image quality."
            ),
            "ringing_artifacts": (
                "Identifies compression artifacts known as 'ringing,' which appear as ghosting or oscillations near sharp edges. "
                "Ringing artifacts are common in compressed images and can make edges look blurry or distorted. "
                "A higher score indicates more pronounced ringing artifacts, which can reduce image clarity."
            ),
        }

        explanation = """
        These plots show individual measurements of image quality metrics for each file.
        Each point represents one file, and the points are grouped by folder, which may
        represent different conditions or sources.
        """
        st.markdown(explanation)
        for metric in self.required_columns():
            st.markdown(f"- **{titles[metric]}** {descriptions[metric]}")

        for metric in self.required_columns():
            # For a single metric, extract and rename the metric column.
            metric_df = df.select(["name_short", "selected_folder_short", metric, "color"])
            unique_folders = metric_df.unique(subset=["selected_folder_short"])
            color_map = {row["selected_folder_short"]: row["color"] for row in unique_folders.to_dicts()}
            fig = px.strip(
                metric_df,
                x="selected_folder_short",
                y=metric,
                labels={
                    "selected_folder_short": "",  # label for the x-axis
                    metric: titles[metric]  # label for the y-axis
                },
                color="selected_folder_short",
                hover_data=["name_short"],
                title=titles[metric],
                color_discrete_map=color_map
            )
            fig.update_layout(
                height=500,
                margin=dict(l=50, r=50, t=80, b=100),
                hovermode='closest',
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

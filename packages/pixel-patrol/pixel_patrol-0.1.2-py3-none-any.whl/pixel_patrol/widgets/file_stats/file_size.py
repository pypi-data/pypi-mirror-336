import polars as pl
import streamlit as st
from plotly import express as px

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class FileSizeWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.FILE_STATS.value

    @property
    def name(self) -> str:
        return "File Size Distribution"
    
    def options(self, data_frame: pl.DataFrame) -> dict:
        bar_mode = st.radio(
            "Select Bar Mode",
            ["Stacked", "Grouped"],
            horizontal=True,
            key=f"bar_mode_{self.name}"
        )
        return {"bar_mode": bar_mode}


    def render(self, selected_files_df: pl.DataFrame, bar_mode: str = "Stacked"):

        plot_data = prepare_size_bins(selected_files_df)

        columns = ['name', 'size']

        fig = px.bar(
            plot_data,
            x='size_bin',
            y='value',
            color='selected_folder_short',
            barmode='stack' if bar_mode == "Stacked" else 'group',
            color_discrete_map=dict(zip(
                plot_data['selected_folder_short'].unique(),
                plot_data.group_by('selected_folder_short', maintain_order=True).first().get_column("color")
            )),
            title="File Size Distribution",
            labels={
                'size_bin': "File Size Range",
                'value': "Number of Files",
                'selected_folder_short': 'Selected Folder'
            },
            hover_data=columns,
        )
        fig.update_traces(
            marker_line_color="white",
            marker_line_width=0.5,  # TODO: Makes plot opaque when too many bars - FIX!
            opacity=1,
        )
        fig.update_layout(
            height=500,
            margin=dict(l=50, r=50, t=80, b=100),
            hovermode='closest',
            bargap=0.1,
            bargroupgap=0.05,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig, use_container_width=True)


def prepare_size_bins(df: pl.DataFrame) -> pl.DataFrame:
    """Prepares size bin categories for the file size distribution."""
    bins = [
        1 * 1024 * 1024,  # 1 MB
        10 * 1024 * 1024,  # 10 MB
        100 * 1024 * 1024,  # 100 MB
        1 * 1024 * 1024 * 1024,  # 1 GB
        10 * 1024 * 1024 * 1024,  # 10 GB
        100 * 1024 * 1024 * 1024,  # 100 GB
    ]
    labels = [
        "<1 MB",
        "1 MB - 10 MB",
        "10 MB - 100 MB",
        "100 MB - 1 GB",
        "1 GB - 10 GB",
        "10 GB - 100 GB",
        ">100 GB"
    ]

    df = df.clone()

    # Create the bin column and add the value column
    df = df.with_columns([
        pl.col("size").cut(bins, labels=labels).alias("size_bin"),
        pl.lit(1).alias("value")
    ])

    # Polars categoricals are not ordered by default.
    # To mimic pandas’ ordered Categorical, create a mapping from label to sort order.
    order_map = {label: i for i, label in enumerate(labels)}

    # Add a temporary column with the sort order, sort the DataFrame, then drop the helper column.
    df = (
        df.with_columns(
            pl.col("size_bin").map_elements(lambda x: order_map.get(x, -1)).alias("size_bin_order")
        )
        .sort("size_bin_order")
        .drop("size_bin_order")
    )

    return df

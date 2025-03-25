import streamlit as st

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
from pixel_patrol.utils.plot import create_bar_chart


class FileExtensionWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.FILE_STATS.value

    def run(self, selected_files_df):
        with st.expander("File Extension Distribution", expanded=False):
            y_axis_param = st.radio(
                "Y axis:",
                ["Number of Files", "Total Size of Files"],
                horizontal=True
            )

            plot_data = selected_files_df.copy()
            plot_data['value'] = 1 if y_axis_param == "Number of Files" else plot_data['size']

            fig = create_bar_chart(
                plot_data,
                x='file_extension',
                title="File Extension Distribution",
                x_title="File Extension",
                y_title="Number of Files" if y_axis_param == "Number of Files" else "Total Size (Bytes)",
                key_suffix="file_extension",
                hover_columns=['name', 'size'], # TODO - human readable size with humanize
            )

            st.plotly_chart(fig, use_container_width=True)
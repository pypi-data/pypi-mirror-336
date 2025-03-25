import streamlit as st

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
from pixel_patrol.utils.plot import create_bar_chart


class FileTimestampWidget(ImagePrevalidationWidget):

    @property
    def tab(self) -> str:
        return DefaultTabs.FILE_STATS.value

    def run(self, selected_files_df):
        with st.expander("File Modification Date Distribution", expanded=False):
            plot_data = selected_files_df.copy()
            plot_data['value'] = 1
            plot_data['modification_period'] = plot_data['modification_period'].astype(str)

            fig = create_bar_chart(
                plot_data,
                x='modification_period',
                title="File Modification Date Distribution",
                x_title="Modification Month",
                key_suffix="date",
                hover_columns=['name'],
            )

            st.plotly_chart(fig, use_container_width=True)
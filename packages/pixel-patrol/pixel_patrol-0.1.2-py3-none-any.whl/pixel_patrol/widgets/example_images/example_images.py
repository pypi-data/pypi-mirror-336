from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from skimage.metrics import structural_similarity as ssim

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.widget_interface import ImagePrevalidationWidget
#from pixel_patrol.utils.utils import load_image


class ExampleImages(ImagePrevalidationWidget):
    @property
    def tab(self) -> str:
        return DefaultTabs.EXAMPLE_IMAGES.value

    def run(self, selected_files_df: pd.DataFrame) -> None:
        a = 1
    #     with st.expander("Example Image Statistic", expanded=True):
    #         on = st.toggle("Activate widget", key="toggle_example_image_stats")
    #
    #         if on:
    #             selected_files_df_adapt = selected_files_df[
    #                 selected_files_df.columns[~selected_files_df.columns.isin(["color"])]]
    #
    #             max_folder_size = selected_files_df_adapt.groupby('parent').size().max()
    #             default_slider_value = 1
    #
    #             subsample_size = st.slider("Select subsample size", min_value=1, max_value=max_folder_size,
    #                                        value=default_slider_value)
    #             subsampled_df = self.subsample(
    #                 selected_files_df_adapt,
    #                 subsample_size
    #             )
    #
    #             images = [(row['name'], load_image(row['name'])) for _, row in subsampled_df.iterrows()]
    #
    #             fft_results_per_image = self.calculate_fft(images)
    #             hist_per_image = self.calculate_histogram(images)
    #             ssim_matrix = self.calculate_ssim_per_channel(images)
    #
    #             self.plot_fft_results(fft_results_per_image)
    #             self.plot_histogram(hist_per_image)
    #             self.plot_ssim_matrices(ssim_matrix)
    #
    # @staticmethod
    # @st.cache_data
    # def _plot_fft_channel(fig, fft_data, row, col):
    #     fig.add_trace(
    #         go.Heatmap(z=fft_data, colorscale='Viridis'),
    #         row=row, col=col
    #     )
    #
    # @st.cache_data
    # def plot_fft_results(_self, fft_results_per_image):
    #     for image_path, fft_results in fft_results_per_image:
    #         num_channels = len(fft_results)
    #
    #         # Create a subplot grid with the number of columns equal to the number of channels
    #         fig = make_subplots(rows=1, cols=num_channels, subplot_titles=[f'Channel {i}' for i in range(num_channels)])
    #
    #         # Plot each channel for the current image
    #         for i in range(num_channels):
    #             _self._plot_fft_channel(fig, fft_results[i], row=1, col=i + 1)
    #
    #         # Update layout
    #         fig.update_layout(
    #             height=400, width=300 * num_channels,
    #             title_text=f'Frequency Domain for {Path(image_path).stem}',
    #             showlegend=False
    #         )
    #
    #         st.plotly_chart(fig, use_container_width=True)
    #
    # @st.cache_data
    # def subsample(_self, selected_files_df, subsample_size):
    #     # Calculate the maximum folder size
    #     subsampled_df = selected_files_df.groupby('parent').apply(
    #         lambda x: x.sample(n=min(len(x), subsample_size)))
    #     subsampled_df.reset_index(drop=True, inplace=True)
    #
    #     return subsampled_df
    #
    # @st.cache_data
    # def calculate_fft(_self, images):
    #     fft_results_per_image = []
    #     for image_path, image in images:
    #         fft_results = [np.fft.fft2(np.squeeze(image[0, channel])) for channel in range(image.shape[1])]
    #         fft_shifted = [np.fft.fftshift(fft) for fft in fft_results]
    #         fft_magnitude = [np.abs(shifted) for shifted in fft_shifted]
    #         fft_results_per_image.append((image_path, fft_magnitude))
    #
    #     return fft_results_per_image
    #
    # @st.cache_data
    # def calculate_histogram(_self, images):
    #     hist_list = []
    #     for image_path, image_data in images:
    #         num_channels = image_data.shape[1]
    #
    #         hist_channel = []
    #         for i in range(num_channels):
    #             channel_data = image_data[0, i].flatten()
    #             hist = px.histogram(channel_data, nbins=256, title=f'Histogram for Channel {i}')
    #             hist_channel.append(hist)
    #
    #         hist_list.append((image_path, hist_channel))
    #
    #     return hist_list
    #
    # @st.cache_data
    # def plot_histogram(_self, hist_per_image):
    #     for image_path, hist_channel in hist_per_image:
    #         num_channels = len(hist_channel)
    #
    #         # Create a subplot grid with the number of columns equal to the number of channels
    #         fig = make_subplots(rows=1, cols=num_channels, subplot_titles=[f'Channel {i}' for i in range(num_channels)])
    #
    #         for i in range(num_channels):
    #             fig.add_trace(hist_channel[i].data[0], row=1, col=i + 1)
    #
    #         # Update layout
    #         fig.update_layout(
    #             height=400, width=300 * num_channels,
    #             title_text=f'Intensity Histogram for {Path(image_path).stem}',
    #             showlegend=False
    #         )
    #
    #         st.plotly_chart(fig, use_container_width=True)
    #
    # @st.cache_data
    # def calculate_ssim_per_channel(_self, images):
    #     ssim_list = []
    #     for image_path, image_data in images:
    #         num_channels = image_data.shape[1]
    #         ssim_values = np.zeros((num_channels, num_channels))
    #
    #         for i in range(num_channels):
    #             for j in range(num_channels):
    #                 if i != j:
    #                     ssim_values[i, j] = ssim(np.squeeze(image_data[0, i]), np.squeeze(image_data[0, j]))
    #                 else:
    #                     ssim_values[i, j] = 1  # SSIM of the same channel with itself is 1
    #
    #         ssim_list.append((image_path, ssim_values))
    #
    #     return ssim_list
    #
    # @st.cache_data
    # def plot_ssim_matrices(_self, ssim_list):
    #     for image_path, ssim_matrix in ssim_list:
    #         num_channels = ssim_matrix.shape[0]
    #         channel_labels = [f'Channel {i}' for i in range(num_channels)]
    #
    #         # Calculate dimensions based on the number of channels
    #         plot_size = 100 * num_channels
    #
    #         # Create a subplot grid with a single plot
    #         fig = make_subplots(rows=1, cols=1, subplot_titles=[f'SSIM Matrix for {Path(image_path).stem}'])
    #
    #         # Add heatmap for SSIM matrix
    #         fig.add_trace(
    #             go.Heatmap(
    #                 z=ssim_matrix,
    #                 colorscale='Viridis',
    #                 showscale=True,
    #                 x=channel_labels,
    #                 y=channel_labels
    #             ),
    #             row=1, col=1
    #         )
    #
    #         # Update layout
    #         fig.update_layout(
    #             height=plot_size,
    #             width=plot_size,
    #             title_text=f'SSIM Matrix for {Path(image_path).stem}',
    #             showlegend=False,
    #             xaxis=dict(scaleanchor="y", scaleratio=1),  # Ensure equal aspect ratio
    #             yaxis=dict(scaleanchor="x", scaleratio=1, autorange='reversed')
    #             # Ensure equal aspect ratio and reverse y-axis
    #         )
    #
    #         st.plotly_chart(fig, use_container_width=False)
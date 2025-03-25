import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import polars as pl
import polars.selectors as cs
import requests
import streamlit as st

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.utils.preprocessing import SPRITE_SIZE
from pixel_patrol.utils.utils import create_sprite_image
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class EmbeddingProjectorWidget(ImagePrevalidationWidget):
    """
    This widget automatically selects numeric columns from your dataset
    and visualizes them as embeddings using TensorBoard’s Embedding Projector.
    """

    @property
    def tab(self) -> str:
        return DefaultTabs.VISUALIZATION.value

    @property
    def name(self) -> str:
        return "TensorBoard Embedding Projector"

    def required_columns(self) -> List[str]:
        """Returns required data column names"""
        return ["*"]


    def summary(self, data_frame: pl.DataFrame):
        df_numeric = data_frame.select(cs.by_dtype(pl.NUMERIC_DTYPES).replace(None, 0.0))
        st.write(f"✅ {df_numeric.shape[1]} numeric columns, "
                 f"with {df_numeric.shape[0]} rows can be utilized to display the data in the Embedding Projector.")


    def render(self, data_frame: pl.DataFrame):

        # Beginner-Friendly Introduction
        st.markdown("""
        The **Embedding Projector** allows you to explore high-dimensional data by reducing it to 
        2D or 3D using **Principal Component Analysis (PCA)** or **t-SNE**.

        **What is an embedding?**  
        - An embedding is a way to represent complex data (e.g., images, text) as points in a high-dimensional space.
        - The closer two points are, the more similar they are.

        **How does this tool help?**  
        - It helps visualize relationships between data points.
        - It enables exploration of clusters and patterns in large datasets.
        """)

        # Convert all columns to numeric, keeping only valid numeric ones
        df_numeric = data_frame.select(cs.by_dtype(pl.NUMERIC_DTYPES).replace(None, 0.0))
        df_metadata = data_frame.select(~cs.by_dtype(pl.NUMERIC_DTYPES) & ~cs.contains("thumbnail"))

        if df_numeric.is_empty():
            st.warning("No numeric data found! Embedding visualization requires numerical features.")
            return

        # Create embedding array
        embeddings_array = df_numeric.to_numpy()
        st.write(f"✅ Using {df_numeric.shape[1]} numeric columns, "
                 f"with {df_numeric.shape[0]} rows.")

        # Automatically Create a Temporary Directory
        temp_log_dir = Path(tempfile.mkdtemp())  # Uses a unique temp folder
        st.write(f"📂 Using temporary folder for TensorBoard logs: `{temp_log_dir}`")

        col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="bottom")

        with col1:
            # Launch TensorBoard
            port = st.number_input("📡 TensorBoard Port", value=6006, step=1)

        started = False
        stopped = False

        with col2:
            if st.button("🚀 Start TensorBoard"):
                st.session_state['tb_process'] = create_checkpoint_and_launch_tensorboard(temp_log_dir, data_frame, embeddings_array, port=port)
                started = True

        with col3:
            if started:
                st.markdown(f"[🔗 Open in new tab](http://127.0.0.1:{port}/#projector)")

        with col4:
            if st.button("🛑 Stop TensorBoard"):
                if "tb_process" in st.session_state:
                    st.session_state['tb_process'].terminate()
                    del st.session_state['tb_process']
                    stopped = True

        with col5:
            if started:
                st.success(f"TensorBoard is running on port {port}!")
            if stopped:
                st.success("TensorBoard stopped.")

        # Show the projector in an iframe
        if "tb_process" in st.session_state:
            st.markdown("### Embedding Projector UI")
            show_tensorboard_projector(port=port)


def generate_sprite_image_from_dataframe(df: pl.DataFrame, sprite_path="sprite.png"):
    """Creates a sprite image from thumbnails stored in a Polars DataFrame."""

    Path(sprite_path).parent.mkdir(parents=True, exist_ok=True)

    sprite_image = create_sprite_image(df)

    # Save sprite image
    sprite_image.save(sprite_path)
    print(f"✅ Sprite image saved: {sprite_path}")


def generate_tf1_projector_checkpoint(embeddings: np.ndarray, meta_df: pd.DataFrame, log_dir: Path, sprite_path: Path):
    """Creates a TF 1.x checkpoint with embedding metadata for TensorBoard."""

    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

    tf.reset_default_graph()

    with tf.Graph().as_default():
        with tf.Session() as sess:
            embedding_var = tf.get_variable(
                name="my_embedding",
                shape=embeddings.shape,
                initializer=tf.constant_initializer(embeddings)
            )
            sess.run(tf.global_variables_initializer())

            # Save checkpoint
            saver = tf.train.Saver()
            saver.save(sess, str(log_dir / "model.ckpt"), global_step=0)

    # Write metadata file
    metadata_file = log_dir / "metadata.tsv"
    meta_df.to_csv(metadata_file, sep="\t", index=False)

    # Create projector config
    from tensorboard.plugins import projector
    summary_writer = tf.summary.FileWriter(str(log_dir))
    config = projector.ProjectorConfig()
    embedding = config.embeddings.add()
    embedding.tensor_name = "my_embedding"
    embedding.metadata_path = "metadata.tsv"
    embedding.sprite.image_path = "sprite.png"
    embedding.sprite.single_image_dim.extend((SPRITE_SIZE, SPRITE_SIZE))
    projector.visualize_embeddings(summary_writer, config)


def create_checkpoint_and_launch_tensorboard(temp_log_dir, data_frame: pl.DataFrame, embeddings_array, port: int = 6006):
    """Launch TensorBoard as a subprocess."""

    # Check if a "thumbnail" column exists and generate a sprite image
    sprite_path = None
    if "thumbnail" in data_frame.columns:
        sprite_path = temp_log_dir.joinpath("sprite.png")
        generate_sprite_image_from_dataframe(data_frame, sprite_path)

    # Extract metadata columns
    df_labels = data_frame.clone().drop("thumbnail")

    generate_tf1_projector_checkpoint(embeddings_array, df_labels.to_pandas(), temp_log_dir, sprite_path)

    return launch_tensorboard(temp_log_dir, port)


def launch_tensorboard(logdir, port):
    cmd = ["tensorboard", f"--logdir={logdir}", f"--port={port}", "--bind_all"]
    env = os.environ.copy()
    env["GCS_READ_CACHE_MAX_SIZE_MB"] = "0"
    tb_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    import time
    for _ in range(50):
        try:
            r = requests.get(f"http://127.0.0.1:{port}")
            if r.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.2)
    return tb_process


def show_tensorboard_projector(port: int):
    """Embed TensorBoard's projector in Streamlit."""
    tb_url = f"http://127.0.0.1:{port}/#projector"
    st.components.v1.iframe(tb_url, height=800, scrolling=True)

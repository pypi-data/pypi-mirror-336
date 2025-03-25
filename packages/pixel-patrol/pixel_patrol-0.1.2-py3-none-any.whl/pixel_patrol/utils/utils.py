import hashlib
import math
import os
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import streamlit as st
from PIL import Image, ImageOps
from matplotlib.colors import rgb2hex

from pixel_patrol.default_values import BASE_CACHE_PATH
from pixel_patrol.default_values import BASE_CACHE_PATH_ENV_VAR
from pixel_patrol.utils.preprocessing import extract_metadata, SPRITE_SIZE

PNG_MODE_TO_INFO = {
    "1": {"s_size": 1, "dtype": "uint1"},       # 1-bit pixels, black and white
    "L": {"s_size": 1, "dtype": "uint8"},       # 8-bit pixels, grayscale
    "P": {"s_size": 1, "dtype": "uint8"},       # 8-bit pixels, palette
    "RGB": {"s_size": 3, "dtype": "uint8"},     # 3x8-bit pixels, true color
    "RGBA": {"s_size": 4, "dtype": "uint8"},    # 4x8-bit pixels, true color with alpha
    "CMYK": {"s_size": 4, "dtype": "uint8"},    # 4x8-bit pixels, color separation
    "YCbCr": {"s_size": 3, "dtype": "uint8"},   # 3x8-bit pixels, color video format
    "LAB": {"s_size": 3, "dtype": "uint8"},     # 3x8-bit pixels, L*a*b color space
    "HSV": {"s_size": 3, "dtype": "uint8"},     # 3x8-bit pixels, Hue, Saturation, Value
    "I": {"s_size": 1, "dtype": "int32"},       # 32-bit signed integer pixels
    "F": {"s_size": 1, "dtype": "float32"},     # 32-bit floating point pixels
    "I;16": {"s_size": 1, "dtype": "uint16"},   # 16-bit signed integer pixels
    "I;16B": {"s_size": 1, "dtype": "uint16"},  # 16-bit big-endian signed integer pixels
    "I;16L": {"s_size": 1, "dtype": "uint16"},  # 16-bit little-endian signed integer pixels
    "LA": {"s_size": 2, "dtype": "uint8"},      # 2x8-bit pixels, L with alpha
    "PA": {"s_size": 2, "dtype": "uint8"},      # 2x8-bit pixels, palette with alpha
}


SMART_FOLDER_FILTERS = [".git", ".zarr", ".ome-zarr"]
def parse_modification_date(date_str):
    """
    Parse modification date from HTTP header.
    Args:
        date_str (str): The date string from the HTTP header.

    Returns:
        datetime or None: The parsed modification date.
    """
    from datetime import datetime
    try:
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return None


def get_cache_dir() -> Path:
    # Use the base cache path from default_values
    cache_dir = Path(os.getenv(BASE_CACHE_PATH_ENV_VAR, BASE_CACHE_PATH))
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_projects_dir() -> Path:
    return get_cache_dir().joinpath("projects")


def get_dataframe_path_structure_path(directory: str) -> str:
    # Create a safe, short filename from the directory path for caching.
    folder_hash = hash_file_path(directory)  # Generate hash
    return str(get_cache_dir() / "dir_structure" / f"{folder_hash}.parquet")


def get_dataframe_images_file(directory: str) -> str:
    # Create a safe, short filename from the directory path for caching.
    folder_hash = hash_file_path(directory)  # Generate hash
    return str(get_cache_dir() / "dir_images" / f"{folder_hash}.parquet")


def get_sprite_file(directory: str) -> str:
    # Create a safe filename from the directory path for caching.
    safe_name = directory.replace(os.sep, "_").replace(":", "")
    return str(get_cache_dir() / f"{safe_name}.png")


def create_sprite_image(df, border=False, border_size=5) -> Image:
    """
    Creates a sprite sheet from the DataFrame, where each thumbnail is arranged in a grid.
    If border=True, it adds a border to each image using the 'color' column.

    :param df: Polars DataFrame containing 'thumbnail' (2D numpy arrays) and 'color' (border color).
    :param border: Whether to add borders to thumbnails.
    :param border_size: Border thickness in pixels.
    :return: PIL Image (sprite sheet).
    """

    # Extract and normalize thumbnails
    thumbnails = df["thumbnail"].drop_nulls().to_list()
    thumbnails = [(np.array(img) - np.min(img)) / (np.max(img) - np.min(img)) * 255 for img in thumbnails]
    thumbnails = [Image.fromarray(img.astype(np.uint8)).resize((SPRITE_SIZE, SPRITE_SIZE)) for img in thumbnails]

    # Extract colors if borders are enabled
    colors = df["color"].drop_nulls().to_list() if border else None

    # Compute grid size
    num_images = len(thumbnails)
    grid_size = math.ceil(math.sqrt(num_images))
    sprite_size = (SPRITE_SIZE + 2 * border_size) * grid_size if border else SPRITE_SIZE * grid_size
    sprite_image = Image.new("RGB", (sprite_size, sprite_size), color=(255, 255, 255))  # White background

    # Arrange images in a grid
    for idx, img in enumerate(thumbnails):
        row, col = divmod(idx, grid_size)

        if border:
            # Get border color
            border_color = colors[idx] if idx < len(colors) else "black"  # Default to black if missing

            # Apply border
            img = ImageOps.expand(img.convert("RGB"), border=border_size, fill=border_color)

        # Compute position
        x_pos = col * (SPRITE_SIZE + 2 * border_size) if border else col * SPRITE_SIZE
        y_pos = row * (SPRITE_SIZE + 2 * border_size) if border else row * SPRITE_SIZE

        # Paste image into the sprite sheet
        sprite_image.paste(img, (x_pos, y_pos))

    return sprite_image


def generate_sprite_image(thumbnails, sprite_path="sprite.png"):
    """Creates a sprite image from a list of thumbnails."""
    num_images = len(thumbnails)
    grid_size = math.ceil(math.sqrt(num_images))  # Make it square

    sprite_size = SPRITE_SIZE * grid_size
    sprite_image = Image.new("L", (sprite_size, sprite_size), color=255)  # Grayscale background

    for idx, thumbnail in enumerate(thumbnails):
        row, col = divmod(idx, grid_size)
        x, y = col * SPRITE_SIZE, row * SPRITE_SIZE
        img = Image.fromarray(thumbnail)
        sprite_image.paste(img, (x, y))

    sprite_image.save(sprite_path)
    print(f"Saved sprite image: {sprite_path}")


def store_all_dataframe_images_to_cache(joint_dataframe_images):
    selected_folders = joint_dataframe_images["selected_folder"].unique().to_list()
    for folder_name in selected_folders:
        # Get subset where column equals this unique value
        subset_df = joint_dataframe_images.filter(pl.col("selected_folder").eq(folder_name)).drop("color")
        existing_dataframe_images = load_dataframe_images_from_cache(folder_name)
        if existing_dataframe_images is None:
            joint_df = subset_df
        else:
            joint_df = aggregate_processing_result(existing_dataframe_images, subset_df)
        store_dataframe_images_to_cache(joint_df, folder_name)


def store_dataframe_images_to_cache(df: pl.DataFrame, directory: str):
    """Store a directory’s DataFrame to its cache file."""
    filepath = get_dataframe_images_file(directory)
    Path(filepath).parent.mkdir(exist_ok=True, parents=True)
    df.write_parquet(filepath)


def store_dataframe_path_structure_to_cache(df: pl.DataFrame, directory: str):
    """Store a directory’s DataFrame to its cache file."""
    filepath = get_dataframe_path_structure_path(directory)
    Path(filepath).parent.mkdir(exist_ok=True, parents=True)
    df.write_parquet(filepath)


def load_dataframe_path_structure_from_cache(folder_name):
    filepath = get_dataframe_path_structure_path(folder_name)
    if os.path.exists(filepath):
        return pl.read_parquet(filepath)
    return None

def load_dataframe_images_from_cache(folder_name):
    filepath = get_dataframe_images_file(folder_name)
    if os.path.exists(filepath):
        return pl.read_parquet(filepath)
    return None


def pick_colors(num_colors, colormap="viridis"):
    """
    Generate a list of colors from a Matplotlib colormap.
    Args:
        num_colors (int): Number of colors to generate.
        colormap (str): Name of the Matplotlib colormap to use.

    Returns:
        list: A list of HEX color strings.
    """
    cmap = plt.get_cmap(colormap)  # Load the colormap

    if num_colors == 1:
        # Return a single color in the middle of the colormap
        return [rgb2hex(cmap(0.3))]

    normalized_values = [i / (num_colors - 1) for i in range(num_colors)]  # Normalize indices
    colors = [rgb2hex(cmap(value)) for value in normalized_values]  # Convert to HEX
    return colors


def get_streamlit_colors(num_elements):
    """
    Retrieve Streamlit's default color palette.
    Args:
        num_elements (int): Number of colors to generate.

    Returns:
        list: List of HEX color strings.
    """
    cmap = plt.get_cmap("tab20")  # Use Streamlit's tab10 palette
    return [rgb2hex(cmap(i)) for i in range(num_elements)]


def format_size(bytes):
    """
    Convert a size in bytes to a human-readable string (e.g., KB, MB, GB).
    Args:
        bytes (float): The size in bytes.

    Returns:
        str: Human-readable size string.
    """
    if bytes is None or bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    idx = 0
    while bytes >= 1024 and idx < len(units) - 1:
        bytes /= 1024.0
        idx += 1
    return f"{bytes:.2f} {units[idx]}"


def parse_human_readable_size(size_str):
    """
    Convert human-readable file sizes (e.g., '1.2K', '3M') to bytes.
    Args:
        size_str (str): The size string.

    Returns:
        int: The size in bytes, or None if parsing fails.
    """
    if not size_str or not size_str.strip():  # Check if size_str is empty or None
        return None

    size_map = {'K': 1024, 'M': 1024**2, 'G': 1024**3}
    size_str = size_str.strip().upper()

    if size_str[-1] in size_map:
        try:
            return int(float(size_str[:-1]) * size_map[size_str[-1]])
        except ValueError:
            return None
    try:
        return int(size_str)
    except ValueError:
        return None


def fetch_local_directory_stats(root_path):
    """
    Traverse a local directory to collect stats.
    Args:
        root_path (str): The path to the root directory.

    Returns:
        dict: Directory stats including a DataFrame representing the tree structure.
    """
    if not os.path.isdir(root_path):
        raise ValueError(f"The path '{root_path}' is not a valid directory.")

    # Collect directory structure
    tree_data = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        current_depth = len(Path(dirpath).parts) - len(Path(root_path).parts)
        parent = str(Path(dirpath).parent) if dirpath != root_path else None

        # Add folder stats
        tree_data.append({
            "name": dirpath,
            "type": "folder",
            "parent": parent,
            "depth": current_depth,
            "size": 0,  # Size will be aggregated later
            "modification_date": datetime.fromtimestamp(os.path.getmtime(dirpath)),
            "file_extension": "",
        })

        # Add file stats
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            tree_data.append({
                "name": file_path,
                "type": "file",
                "parent": dirpath,
                "depth": current_depth + 1,
                "size": file_size,
                "modification_date": datetime.fromtimestamp(os.path.getmtime(file_path)),
                "file_extension": Path(filename).suffix[1:].lower() if Path(filename).suffix else "",
            })

    # Convert to DataFrame
    df = pl.DataFrame(tree_data)

    stats = aggregate_stats(df)

    return stats


def aggregate_stats(df):
    """Aggregate stats for folders."""
    if not isinstance(df, pl.DataFrame):
        raise ValueError("The provided object is not a DataFrame.")
    if df.is_empty():
        return {"files": 0, "folders": 0, "total_size": 0, "tree": df}

    unique_depths = sorted(df["depth"].unique().to_list(), reverse=True)
    for depth in unique_depths:
        level_df = df.filter(pl.col("depth") == depth)
        for row in level_df.iter_rows(named=True):
            if row["type"] == "folder":
                children = df.filter(pl.col("parent") == row["name"])
                total_size = children["size"].sum()
                modification_date = children["modification_date"].max()
                df = df.with_columns([
                    pl.when(pl.col("name") == row["name"])
                        .then(total_size)
                        .otherwise(pl.col("size"))
                        .alias("size"),
                    pl.when(pl.col("name") == row["name"])
                        .then(modification_date)
                        .otherwise(pl.col("modification_date"))
                        .alias("modification_date"),
                ])
    df = df.with_columns(
        pl.col("size").map_elements(lambda x: format_size(x), return_dtype=pl.Utf8).alias('size_readable')
    )

    total_files = df.filter(pl.col("type") == "file").height
    total_folders = df.filter(pl.col("type") == "folder").height
    total_size_val = df.filter(pl.col("type") == "file").select(pl.col("size").sum()).item()

    # Add aggregated stats to the root row (where parent is null)
    df = df.with_columns([
        pl.when(pl.col("parent").is_null()).then(pl.lit(total_files)).alias("files"),
        pl.when(pl.col("parent").is_null()).then(pl.lit(total_folders)).alias("folders"),
        pl.when(pl.col("parent").is_null()).then(pl.lit(format_size(total_size_val))).alias("total_size")
    ])

    return {"files": total_files, "folders": total_folders, "total_size": total_size_val, "tree": df}

# Find the common base folder
def find_common_base(folders):
    if not folders:
        return ""
    if len(folders) == 1:
        return str(Path(folders[0]).parent) + os.sep
    # Convert all paths to absolute paths to ensure consistency
    common_base = os.path.commonpath(folders)
    return common_base + os.sep

def preprocess_files(data_frame: pl.DataFrame) -> pl.DataFrame:
    """
    Preprocesses files by aggregating statistics from multiple imported paths
    and filtering based on selected folders.

    Parameters:
    - imported_paths: List of dictionaries containing file statistics under the key "stats" -> "tree".

    Returns:
    - A Polars DataFrame containing the aggregated and processed file information.
    """

    # Get all unique values in the "selected_folder" column
    unique_folders = data_frame["selected_folder"].unique().to_list()

    # Find the common base folder
    common_base = find_common_base(unique_folders)

    data_frame = data_frame.with_columns([
        pl.col("modification_date").dt.month().alias("modification_period"),
        # Extract file extension or set as 'unknown' if not present
        pl.col("name").str.split(".").list.last().fill_null("unknown").alias("file_extension"),
        pl.col("selected_folder").str.replace(common_base, "", literal=True).alias("selected_folder_short"),
        pl.col("name").str.replace(common_base, "", literal=True).alias("name_short"),
    ])

    return data_frame


def add_colors(data_frame: pl.DataFrame, colors: List[str] = None) -> pl.DataFrame:
    """
    Add colors to the dataframe based on the selected_folder column.

    Parameters:
    - data_frame
    - colors: List of color per each unique imported_folder entry.

    Returns:
    - A Polars DataFrame containing the aggregated and processed file information.
    """
    selected_folders = data_frame["selected_folder"].unique().to_list()
    color_mapping = {folder: color for folder, color in zip(selected_folders, colors)}

    if colors:
        data_frame = data_frame.with_columns(
            pl.col("selected_folder").replace_strict(color_mapping).alias("color")
        )
    return data_frame


def aggregate_folder_dataframes(imported_paths: OrderedDict[str, pl.DataFrame]) -> Optional[pl.DataFrame]:
    """
    Aggregate dataframes from multiple imported paths.

    Parameters:
    - imported_paths: List of dictionaries containing file statistics under the key "stats" -> "tree".

    Returns:
    - A Polars DataFrame containing the aggregated dataframes.
    """

    if len(imported_paths) == 0:
        return None

    # collect all dataframes and add selected_folder column
    dfs = []
    for imported_path in imported_paths:
        df = imported_paths[imported_path]
        if len(df) == 0:
            continue
        df = df.with_columns(pl.lit(str(imported_path)).alias("selected_folder"))
        dfs.append(df)

    # dfs = standardize_schema(dfs)

    if len(dfs) > 0:
        all_selected_files = pl.concat(dfs, how="diagonal_relaxed")
        return all_selected_files
    return None


def process_files(files: pl.DataFrame, required_columns: List[str]):
    if required_columns is None or len(required_columns) == 0:
        return files
    # Step 1: Extract metadata in Python
    metadata_list = [extract_metadata(name, required_columns) for name in files["name"]]
    # Step 2: Add metadata as a new column
    result = files.select(["name"]).with_columns(pl.Series("metadata", metadata_list))
    result = result.unnest('metadata')
    return aggregate_processing_result(files, result)


def apply_fast_mode(dataframe, num_files_per_selected_directory):
    df_with_rand = dataframe.with_columns(pl.lit(np.random.rand(dataframe.height)).alias("rand"))
    df_sorted = df_with_rand.sort(["selected_folder", "rand"])
    sampled_df = df_sorted.group_by("selected_folder").head(num_files_per_selected_directory)
    dataframe = sampled_df.drop("rand")
    return dataframe


def is_subpath(new_path, existing_path):
    """Check if new_path is a subpath of existing_path."""
    try:
        Path(new_path).resolve().relative_to(Path(existing_path).resolve())
        return True
    except ValueError:
        return False


def is_superpath(new_path, existing_path):
    """Check if new_path contains existing_path."""
    try:
        Path(existing_path).resolve().relative_to(Path(new_path).resolve())
        return True
    except ValueError:
        return False


def add_new_path(new_path, project):
    df_structure = load_dataframe_path_structure_from_cache(new_path)

    if df_structure is None:
        df_structure = fetch_local_directory_stats(new_path)["tree"]

    if df_structure.is_empty():
        st.warning(f"No data found in {new_path}. Path not added.")
        return

    paths = project.paths.copy()
    paths[new_path] = df_structure
    project.paths = paths

    update_path_summary(new_path, project)


def update_path_summary(the_path, project):
    df_structure = project.paths[the_path]
    cache_file = get_dataframe_path_structure_path(the_path)
    if not os.path.exists(cache_file):
        cache_date = "Not cached yet"
    else:
        cache_date = datetime.fromtimestamp(os.path.getmtime(cache_file)).strftime("%Y-%m-%d %H:%M:%S")
    # Explicitly create summary DataFrame with all columns (including cache_date)
    summary_df = (
        df_structure
        .filter(pl.col("parent").is_null())
        .select(["files", "folders", "modification_date", "size"])
        .with_columns([
            pl.col("size")
            .map_elements(format_size, return_dtype=pl.Utf8, skip_nulls=False)
            .alias("size_readable"),
            pl.lit(cache_date).alias("cache_date")
        ])
    )
    # Fix mutation issue here as well:
    path_summaries = project.path_summaries.copy()
    path_summaries[the_path] = summary_df
    project.path_summaries = path_summaries


def cache_all_project_path_structures(project):
    for path, df_structure in project.paths.items():
        store_dataframe_path_structure_to_cache(df_structure, path)


def aggregate_processing_result(original_df, processed_files) -> pl.DataFrame:
    original_cols = set(original_df.columns)
    processed_full_dataframe = original_df.join(processed_files, on="name", how="left", suffix="_new")
    # For each column in processed_files (except the join key "name"),
    # either update the column (if it exists in the original) or add it (if it's new)
    for col in processed_files.columns:
        if col == "name":
            continue
        new_col = f"{col}_new"
        if col in original_cols:
            # If the column already exists in df, update using coalesce:
            # take the new value when present, otherwise the original.
            processed_full_dataframe = processed_full_dataframe.with_columns(
                pl.coalesce(pl.col(new_col), pl.col(col)).alias(col)
            ).drop(new_col)
    return processed_full_dataframe


def load_dataframe_images(project) -> Optional[pl.DataFrame]:

    selected_file_extensions = [
        ext.lower() for ext in project.settings.get("selected_file_extensions", [])
    ]

    data_type_filter = (pl.col("file_extension").str.to_lowercase().is_in(selected_file_extensions)
        if selected_file_extensions else None)

    dfs = OrderedDict()
    for path_str in project.paths:
        cached_df = load_dataframe_images_from_cache(path_str)
        if cached_df is None:
            project.df_images = None
            return None
        if data_type_filter is not None:
            cached_df = cached_df.filter(data_type_filter)

        dfs[path_str] = cached_df

    if dfs:
        dataframe_images = aggregate_folder_dataframes(dfs)
        if dataframe_images is not None:
            dataframe_images = set_colors(dataframe_images, project)
            project.df_images = dataframe_images
            return dataframe_images

    return None


def set_colors(to_be_processed_files, project):
    cmap = project.settings.get("cmap", 'rainbow')
    colors = pick_colors(len(project.paths), colormap=cmap)
    return add_colors(to_be_processed_files, colors)


def hash_file_path(filepath, length=16):
    """
    Generate a deterministic short hash from a file path.

    Args:
        filepath (str): The long file path to hash.
        length (int): The length of the short hash to return (default: 8).

    Returns:
        str: A short hash string.
    """
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the file path (encoded as UTF-8 bytes)
    hash_object.update(str(filepath).encode('utf-8'))

    # Get the hexadecimal digest of the hash
    hex_digest = hash_object.hexdigest()

    # Return the first `length` characters of the hash
    return hex_digest[:length]


def count_file_extensions(project_paths: dict[str, pl.DataFrame]) -> dict[str, int]:
    """
    Returns a dictionary { 'extension': count, 'all_files': total_count } for all files across all paths.
    Files without extensions or with trailing dots are discarded.
    """
    # Collect all DataFrames into a list
    dfs = []
    for df_structure in project_paths.values():
        # Filter rows where 'type' is "file"
        df_files = df_structure.filter(pl.col("type") == "file")
        dfs.append(df_files)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pl.concat(dfs)

    combined_df = combined_df.filter(pl.col("file_extension").is_not_null())

    # Group by extension and get counts
    grouped = combined_df.group_by("file_extension").agg(pl.count())

    # Convert the result to a dictionary
    result = {row["file_extension"]: row["count"] for row in grouped.iter_rows(named=True)}

    # Add total files count to the dictionary
    result["all_files"] = combined_df.height  # Total number of rows (files)

    return result


def filter_dataframe_by_file_extensions(df: pl.DataFrame, selected_file_extensions: List[str]) -> pl.DataFrame:
    """
    Filter a DataFrame to include only rows with the selected file types.
    """
    if not selected_file_extensions:
        return df

    # Convert selected_file_extensions to lowercase for case-insensitive comparison
    selected_file_extensions = [ft.lower() for ft in selected_file_extensions]

    # Filter the DataFrame
    return df.filter(
        pl.col("file_extension").str.to_lowercase().is_in(selected_file_extensions)
    )

def file_structure_cache_missing(project):
    for path in project.paths.keys():
        path_structure = get_dataframe_path_structure_path(path)
        if not os.path.exists(path_structure):
            return True
    return False

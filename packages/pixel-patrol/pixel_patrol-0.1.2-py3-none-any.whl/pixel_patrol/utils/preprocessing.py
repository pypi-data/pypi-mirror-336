import fnmatch
from itertools import product
from typing import Callable, Optional
from typing import Dict, List

import bioio_base
import cv2
import numpy as np
import pywt
from PIL import Image
from bioio import BioImage

SPRITE_SIZE = 64

def _mapping_for_np_array_processing_by_column_name():
    return {
        "mean": calculate_mean,
        "median": calculate_median,
        "std": calculate_std,
        "min": calculate_min,
        "max": calculate_max,
        "laplacian_variance": calculate_variance_of_laplacian,
        "tenengrad": calculate_tenengrad,
        "brenner": calculate_brenner,
        "noise_std": calculate_noise_estimation,
        "wavelet_energy": calculate_wavelet_energy,
        "blocking_artifacts": calculate_blocking_artifacts,
        "ringing_artifacts": calculate_ringing_artifacts,
        "thumbnail": get_thumbnail
    }


def _mapping_for_bioimage_metadata_by_column_name():
    return {
        "metadata": get_bioio_metadata,
    }

def _mapping_for_png_metadata_by_column_name():
    return {
        "metadata": get_PIL_metadata,
    }


def get_bioio_metadata(img: BioImage):
    return {
        "dim_order": img.dims.order,
        "t_size": img.dims.T,
        "c_size": img.dims.C,
        "z_size": img.dims.Z,
        "y_size": img.dims.Y,
        "x_size": img.dims.X,
        "s_size": img.dims.S if "S" in img.dims.order else None,
        "m_size": img.dims.M if "M" in img.dims.order else None,
        "n_images": len(img.scenes),
        "dtype": str(img.dtype),
        "pixel_size_X": img.physical_pixel_sizes.X if img.physical_pixel_sizes.X else 1.0,
        "pixel_size_Y": img.physical_pixel_sizes.Y if img.physical_pixel_sizes.Y else 1.0,
        "pixel_size_Z": img.physical_pixel_sizes.Z if img.physical_pixel_sizes.Z else 1.0,
        "channel_names": img.channel_names,
    }


def get_PIL_metadata(img: Image):
    return {
        "dim_order": "XY" if len(img.size) == 2 else "XYC",
        "t_size": 1,
        "c_size": 1 if len(img.size) == 2 else img.size[2],
        "z_size": 1,
        "y_size": img.height,
        "x_size": img.width,
        "s_size": 1,
        "m_size": 1,
        "n_images": 1,
        "dtype": str(img.mode),
        "pixel_size_X": 1.0,
        "pixel_size_Y": 1.0,
        "pixel_size_Z": 1.0,
        "channel_names": ["Red", "Green", "Blue"],
    }


def column_matches(column, columns):
    """Check if column matches any entry in columns (supporting wildcards)."""
    return any(fnmatch.fnmatch(column, pattern) for pattern in columns)


def extract_metadata(name: str, columns: List[str]) -> Dict:
    metadata = {}
    mapping = _mapping_for_bioimage_metadata_by_column_name()
    np_array = None
    dim_order = None
    try:
        print(name)
        img = BioImage(name)
        dim_order = img.dims.order
        for column in mapping:
            if column_matches(column, columns):
                result = mapping[column](img)
                metadata.update(result)
        try:
            np_array = img.data
        except Exception as e:
            print("Could not load data of file", name, ":", e)
    #
    except bioio_base.exceptions.UnsupportedFileFormatError:
        try:
            mapping = _mapping_for_png_metadata_by_column_name()
            img = Image.open(name)
        except Exception as e:
            # Handle other exceptions or set default metadata
            return None

        for column in mapping:
            if column_matches(column, columns):
                result = mapping[column](img)
                metadata.update(result)
        try:
            np_array = np.array(img)
            dim_order = "XY" if len(np_array.shape) == 2 else "XYC"
        except Exception as e:
            print("Could not load data of file", name, ":", e)

    except IndexError:
        # Return empty metadata or set default values as needed
        pass

    calculate_np_array_stats(columns, metadata, np_array, dim_order)

    return metadata


def generate_thumbnail(np_array: np.array, dim_order: str) -> np.array:
    """
    Reduces a multi-dimensional image to 2D using `dim_order`, then generates a thumbnail.

    Args:
        np_array (np.array): Input image (can be multi-dimensional).
        dim_order (str): A string describing dimension order, e.g., "TZCYX", "CXY", "XY".

    Returns:
        np.array: Thumbnail image (SPRITE_SIZE x SPRITE_SIZE).
    """

    # Reduce all dimensions except XY
    while np_array.ndim > 2:
        i = 0
        for dim in dim_order:
            if dim not in ["X", "Y"]:  # Reduce other dimensions
                center_index = np_array.shape[i] // 2  # Middle slice
                np_array = np_array.take(indices=center_index, axis=i)
                dim_order = dim_order.replace(dim, "")  # Remove reduced dim
            else:
                i+=1

    # Ensure dtype is uint8
    if np_array.dtype != np.uint8:
        np_array = (np_array - np_array.min()) / (np_array.max() - np_array.min()) * 255  # Normalize
        np_array = np_array.astype(np.uint8)

    # Convert to image and resize
    img = Image.fromarray(np_array)
    img = img.resize((SPRITE_SIZE, SPRITE_SIZE))

    return np.array(img)  # Return as NumPy array


def calculate_np_array_stats(columns, metadata, np_array, dim_order):
    if np_array is not None:
        mapping = _mapping_for_np_array_processing_by_column_name()
        for column in mapping:
            if column_matches(column, columns):
                func = mapping[column]
                result = func(np_array, dim_order)
                metadata.update(result)


def calculate_mean(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, np.mean, "mean", agg_func=np.mean)


def calculate_median(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, np.median, "median", agg_func=np.median)


def calculate_std(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, np.std, "std")

def calculate_min(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, np.min, "min", agg_func=np.min)

def calculate_max(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, np.max, "max", agg_func=np.max)

def calculate_variance_of_laplacian(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, variance_of_laplacian, "laplacian_variance", agg_func=np.mean)

def calculate_tenengrad(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, tenengrad, "tenengrad", agg_func=np.mean)

def calculate_brenner(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, brenner, "brenner", agg_func=np.mean)

def calculate_noise_estimation(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, noise_estimation, "noise_estimation", agg_func=np.mean)

def calculate_wavelet_energy(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, wavelet_energy, "wavelet_energy", agg_func=np.mean)

def calculate_ringing_artifacts(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, _check_ringing_artifacts, "ringing_artifacts", agg_func=np.mean)

def calculate_blocking_artifacts(arr: np.array, dim_order: str):
    return compute_hierarchical_stats(arr, dim_order, _check_blocking_artifacts, "blocking_artifacts", agg_func=np.mean)

def get_thumbnail(arr: np.array, dim_order: str):
    return {
        "thumbnail": generate_thumbnail(arr, dim_order).tolist()
    }

def to_gray(image: np.array, dim_order: str):
    """
    Convert an image (or higher-dimensional array) to grayscale without reordering any dimensions.

    If the image has a channel dimension (indicated by "C" in dim_order), the function assumes:
      - If the channel size is 3, the image is in BGR format.
      - If the channel size is 4, the image is in RGBA format (and the alpha channel is ignored).

    The grayscale conversion is performed as a weighted sum over the color channels.
      - For a BGR image, weights = [0.114, 0.587, 0.299].
      - For an RGBA image, weights = [0.299, 0.587, 0.114] (using only R, G, B channels).

    The channel axis is contracted (removed) and the original order of all other dimensions is preserved.
    The function returns a tuple of the grayscale array and the updated dim_order (with "C" removed).

    Args:
        image (np.array): Input image array (can be 2D, 3D, or higher-dimensional).
        dim_order (str): A string describing the dimension order (e.g., "XYC", "BXYC", "TZXYC").

    Returns:
        tuple: (gray_image, new_dim_order) where new_dim_order is dim_order with "C" removed.
    """
    if "C" not in dim_order:
        return image, dim_order

    c_index = dim_order.index("C")
    n_channels = image.shape[c_index]

    if n_channels == 1:
        # Squeeze out the channel dimension if it's a singleton.
        gray = np.squeeze(image, axis=c_index)
        new_dim_order = dim_order.replace("C", "")
        return gray, new_dim_order
    if n_channels == 3:
        # Assume BGR
        weights = np.array([0.114, 0.587, 0.299], dtype=image.dtype)
    elif n_channels == 4:
        # Assume RGBA; ignore the alpha channel by taking only the first three channels.
        weights = np.array([0.299, 0.587, 0.114], dtype=image.dtype)
        image = np.take(image, indices=[0, 1, 2], axis=c_index)
    else:
        raise ValueError(f"Expected channel dimension size 3 (BGR) or 4 (RGBA), got {n_channels}")

    # Compute weighted sum along the channel axis.
    # This contracts the "C" axis with the weights, leaving an array with that axis removed.
    gray = np.tensordot(image, weights, axes=([c_index], [0]))
    # np.tensordot moves the remaining axes so that they are in order:
    # the output shape becomes image.shape[:c_index] + image.shape[c_index+1:]

    # Adjust dim_order by removing "C"
    new_dim_order = dim_order.replace("C", "")

    return gray, new_dim_order


def variance_of_laplacian(image):
    if len(image.shape) > 2:
        return None
    gray = image.astype(np.float64)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return lap.var()

def tenengrad(image):
    if len(image.shape) > 2:
        return None
    gray = image.astype(np.float64)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    return np.mean(mag)

def brenner(image):
    if len(image.shape) > 2:
        return None
    gray = image.astype(np.float32)
    diff = gray[:, 2:] - gray[:, :-2]
    return np.mean(diff**2)

def noise_estimation(image):
    if len(image.shape) > 2:
        return None
    gray = image.astype(np.float32)
    median = cv2.medianBlur(gray, 3)
    noise = gray - median
    return np.std(noise)

def wavelet_energy(image, wavelet='db1', level=1):
    if len(image.shape) > 2:
        return None
    gray = np.float32(image)
    coeffs = pywt.wavedec2(gray, wavelet, level=level)
    energy = 0.0
    for detail in coeffs[1:]:
        for subband in detail:
            energy += np.sum(np.abs(subband))
    return energy

def _check_blocking_artifacts(gray: np.ndarray) -> float:
    """Detects blocking artifacts by analyzing 8x8 block boundaries."""
    gray = np.float32(gray)
    block_size = 8
    height, width = gray.shape
    blocking_effect = 0

    # Horizontal boundaries
    for i in range(block_size, height, block_size):
        row_diff = np.mean(np.abs(gray[i, :] - gray[i-1, :]))
        blocking_effect += row_diff

    # Vertical boundaries
    for j in range(block_size, width, block_size):
        col_diff = np.mean(np.abs(gray[:, j] - gray[:, j-1]))
        blocking_effect += col_diff

    # Normalize by number of boundaries
    num_boundaries = (height // block_size) + (width // block_size)
    return blocking_effect / num_boundaries if num_boundaries > 0 else 0.


def _check_ringing_artifacts(gray: np.ndarray) -> float:
    """Detects ringing artifacts by analyzing noise near edges."""
    # Detect edges using Canny

    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    edges = cv2.Canny(gray, 50, 150)
    if np.sum(edges) == 0:
        return 0  # No edges found

    # Dilate edges to include neighboring pixels
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Mask of pixels near edges (excluding the edges themselves)
    edge_neighborhood = dilated_edges - edges

    # Calculate variance in the neighborhood of edges
    ringing_variance = np.var(gray[edge_neighborhood > 0])
    return float(ringing_variance)


def compute_hierarchical_stats(
    arr: np.ndarray,
    dim_order: str,
    func: Callable[[np.ndarray], float],
    func_name: str,
    agg_func: Optional[Callable[[np.ndarray], float]] = None,
    priority_order: str = "CTZ",
) -> Dict[str, float]:
    """
    Computes hierarchical statistics for a multi-dimensional array.

    Args:
        arr (np.ndarray): The input array.
        dim_order (str): A string describing the order of dimensions (e.g., "XYZCT").
                         Must contain "X" and "Y" for spatial dimensions.
        func (Callable): Function to compute the metric on a slice of the array.
                         Takes a numpy array and an axis string as input.
        func_name (str): The name of the function used (e.g., "tenengrad").
        agg_func (Optional[Callable]): Aggregation function to use for higher-order statistics.
                                       If None, no aggregation is performed, and the metric is computed
                                       directly on higher-level splits.
        priority_order (str): The order of dimensions to prioritize for final aggregation.

    Returns:
        dict: A dictionary with hierarchical statistics.
    """
    if len(dim_order) != arr.ndim:
        raise ValueError(f"dim_order '{dim_order}' does not match array shape {arr.shape}")
    if "X" not in dim_order or "Y" not in dim_order:
        raise ValueError("dim_order must contain both 'X' and 'Y'")

    # Identify non-spatial dimensions: (letter, axis_index)
    non_spatial = [(dim, i) for i, dim in enumerate(dim_order) if dim not in ["X", "Y"]]

    # If there are no non-spatial dimensions, compute the metric directly on the entire array
    if not non_spatial:
        global_stat = func(arr)
        return {func_name: global_stat} if global_stat is not None else {}

    # Compute the lowest level statistics (leaves of the tree)
    detailed_stats = _compute_lowest_level_stats(arr, dim_order, non_spatial, func, func_name)

    # If no aggregation is required, compute metrics directly on higher-level splits
    if agg_func is None:
        higher_level_stats = _compute_higher_level_stats(arr, dim_order, non_spatial, func, func_name)
        return {**detailed_stats, **higher_level_stats}

    # Compute aggregated statistics for each level of the hierarchy
    agg_stats = _compute_aggregated_stats(detailed_stats, non_spatial, agg_func, func_name, priority_order)

    # Combine results
    result = {**detailed_stats, **agg_stats}
    return result

def _compute_lowest_level_stats(
    arr: np.ndarray,
    dim_order: str,
    non_spatial: List[tuple],
    func: Callable[[np.ndarray], float],
    func_name: str,
) -> Dict[str, float]:
    """
    Computes the lowest level statistics for each slice along non-spatial dimensions.
    """
    detailed_stats = {}
    non_spatial_ranges = [range(arr.shape[i]) for _, i in non_spatial]

    for idx_tuple in product(*non_spatial_ranges):
        slicer = [slice(None)] * arr.ndim
        for (dim, axis), idx in zip(non_spatial, idx_tuple):
            slicer[axis] = idx
        slicer = tuple(slicer)

        stat_value = func(arr[slicer])

        if stat_value is not None:
            key_parts = [f"{dim.lower()}{idx}" for (dim, _), idx in zip(non_spatial, idx_tuple)]
            if len(key_parts) > 0:
                key = f"{func_name}_" + "_".join(key_parts)
                detailed_stats[key] = stat_value

    return detailed_stats

def _compute_higher_level_stats(
    arr: np.ndarray,
    dim_order: str,
    non_spatial: List[tuple],
    func: Callable[[np.ndarray], float],
    func_name: str,
) -> Dict[str, float]:
    """
    Computes metrics directly on higher-level splits when no aggregation is possible.
    """
    higher_level_stats = {}

    # Iterate over each non-spatial dimension and compute metrics for higher-level splits
    for dim, axis in non_spatial:
        for idx in range(arr.shape[axis]):
            slicer = [slice(None)] * arr.ndim
            slicer[axis] = idx
            slicer = tuple(slicer)

            stat_value = func(arr[slicer])

            if stat_value is not None:
                key = f"{func_name}_{dim.lower()}{idx}"
                higher_level_stats[key] = stat_value

    # Compute the metric on the entire array
    global_stat = func(arr)
    if global_stat is not None:
        higher_level_stats[func_name] = global_stat

    return higher_level_stats

def _compute_aggregated_stats(
    detailed_stats: Dict[str, float],
    non_spatial: List[tuple],
    agg_func: Callable[[np.ndarray], float],
    func_name: str,
    priority_order: str,
) -> Dict[str, float]:
    """
    Computes aggregated statistics for each level of the hierarchy.
    """
    agg_stats = {}

    # Iterate over each non-spatial dimension and aggregate
    for dim, axis in non_spatial:
        group = {}
        for key, stat_value in detailed_stats.items():
            parts = key[len(func_name) + 1:].split("_")
            dim_idx = next((i for i, (d, _) in enumerate(non_spatial) if d == dim), None)
            if dim_idx is not None and parts[dim_idx].startswith(dim.lower()):
                group.setdefault(parts[dim_idx], []).append(stat_value)

        for part, values in group.items():
            agg_key = f"{func_name}_{part}"
            agg_stats[agg_key] = agg_func(np.array(values))

    # Compute the final aggregated statistic based on priority order
    final_key = func_name
    final_values = []
    for dim in priority_order:
        if dim in [d for d, _ in non_spatial]:
            dim_keys = [k for k in agg_stats.keys() if k.startswith(f"{func_name}_{dim.lower()}")]
            if dim_keys:
                final_values.extend([agg_stats[k] for k in dim_keys])
                break

    if final_values:
        agg_stats[final_key] = agg_func(np.array(final_values))

    return agg_stats
import os
from pathlib import Path
import tempfile

BASE_CACHE_PATH_ENV_VAR = "IMAGE_PREVALIDATION_BASE_CACHE_PATH"
BASE_CACHE_PATH = os.getenv(BASE_CACHE_PATH_ENV_VAR, str(Path.home().joinpath(".pixel_patrol")))

TEMP_DIR = tempfile.TemporaryDirectory()

def get_named_temp_file():
    return tempfile.NamedTemporaryFile(delete=False)

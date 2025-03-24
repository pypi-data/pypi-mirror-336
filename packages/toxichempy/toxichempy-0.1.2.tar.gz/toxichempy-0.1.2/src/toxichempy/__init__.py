try:
    from importlib.metadata import version

    __version__ = version("toxichempy")
except ImportError:
    __version__ = "0.1.2"  # fallback

from ._env_check import check_environment
# from toxichempy.utils.data_io_utils import convert_file, read_file, write_file
# from toxichempy.pipeline_framework.bioassay_data_for_ml import run_bioassay_data_prep_pipeline
# # Import specific functions from data_io_utils.py
# from toxichempy.pipeline_framework.aop_data import build_aop_data
# # Define what should be available when importing `toxichempy.utils`
# __all__ = ["read_file", "write_file", "convert_file","run_bioassay_data_prep_pipeline","build_aop_data"]
from .cli import app  # This allows `toxichempy` to run the CLI

__all__ = ["app"]

check_environment()

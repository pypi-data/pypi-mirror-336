import os
from importlib.resources import files
import logging

# Set up logging
logger = logging.getLogger(__name__)
def get_package_path(subdir = None):
    package_dir = os.path.dirname(os.path.join(files("golding_NEURON"),"golding_NEURON"))
    if subdir is None:
        return package_dir
    if type(subdir) != str:
        logger.error("subdir must be a string")
        raise TypeError("subdir must be a string")
    else: subdir_path = os.path.join(package_dir, subdir)
    if not os.path.exists(subdir_path):
        logger.error(f"Subdirectory {subdir} does not exist")
        raise FileNotFoundError(f"subdir {subdir} does not exist")
    if not os.path.isdir(subdir_path):
        logger.error(f"Subdirectory {subdir} is not a directory")
        raise NotADirectoryError(f"{subdir} is not a directory")
    else:
        return subdir_path

# def list_package_data():
#     """List all files included in the package data."""
#     ## Get the package directory
#     package_dir = os.path.dirname(pkg_resources.resource_filename('golding_NEURON', '__init__.py'))
    
#     ## List files in the main package directory
#     main_files = [f for f in os.listdir(package_dir) 
#                   if os.path.isfile(os.path.join(package_dir, f))]
    
#     ## List files in the data directory
#     data_dir = os.path.join(package_dir, 'data')
#     data_files = [f'data/{f}' for f in os.listdir(data_dir) 
#                  if os.path.isfile(os.path.join(data_dir, f))]
    
#     return main_files + data_files
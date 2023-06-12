""" Configuration file basically for paths

Put here:
* paths to data,
* paths to artifacts,
* S3 bucket names,
* file extensions,
* project name.


Do NOT put here (use a separate file) experiment parameters  like:
* batch size,
* optimizer,
* backbone model.


Also rather do not import another project files here.

Every constant that ends with `_DIR` should be a directory. Such a
directory will be created if nonexistent.

"""

import os

from dotenv import load_dotenv

# BASE PATHS
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

# Envs
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

# Create directories based on constants that end with '_DIR' defined in this file.
DIRECTORIES_TO_CREATE = [v for k, v in globals().copy().items() if k.endswith('_DIR')]

for directory in DIRECTORIES_TO_CREATE:
    os.makedirs(directory, exist_ok=True)

load_dotenv(dotenv_path=ENV_PATH)

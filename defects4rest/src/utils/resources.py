#-------------------------------------------------------------------------------
# Copyright (c) 2026 Rahil Piyush Mehta, Kausar Y. Moshood, Huwaida Rahman Yafie and Manish Motwani
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""
Utility functions for managing defects4rest package resources and project directories.

Provides helpers to:
- Access packaged resources (CSV files, data directories)
- Check system prerequisites
- Create/manage temporary project directories
- Convert importlib.resources Traversables to filesystem Paths
"""

from importlib.resources import files, as_file
from pathlib import Path
from contextlib import contextmanager
import shutil
import sys
import os


def resource(*parts: str):
    """
    Return a Traversable to a packaged resource under defects4rest/.
    Example: resource("data", "defect-data", "awx_info.csv")
    """
    return files("defects4rest").joinpath(*parts)


def data_csv(project: str):
    """
    Return path to defects4rest/data/defect-data/<project>_info.csv
    """
    project = project.lower()
    return resource("data", "defect_data", f"{project}_info.csv")


def check_prereq(cmd):
    """
    Check if a command is available in PATH, exit if not found.
    """
    if shutil.which(cmd) is None:
        print(f"Error: '{cmd}' is not installed or not in your PATH.", file=sys.stderr)
        sys.exit(1)


def get_defects4rest_root(levels_up=2):
    """
    Get the defects4rest root directory by traversing up from current script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(script_dir, *[".."] * levels_up))
    return root_path


# Environment variable for project root directory
ENV_PROJECT_ROOT = "DEFECTS4REST_PROJECT_ROOT"


@contextmanager
def _real_path(traversable):
    """
    Convert an importlib.resources Traversable into a real filesystem Path.
    """
    with as_file(traversable) as p:
        yield Path(p)


def ensure_temp_project_dir(project_name: str) -> Path:
    """
    Create and return the temporary project directory at:
    defects4rest/data/temp_project_data/<project_name>/

    Sets environment variables DEFECTS4REST_PROJECT_ROOT and DEFECTS4REST_PROJECT.
    Note: Only writable if package directory is writable (e.g., editable installs).
    """
    project = project_name.lower()

    data_trav = files("defects4rest").joinpath("data")
    with _real_path(data_trav) as data_dir:
        temp_dir = data_dir / "temp_project_data" / project
        temp_dir.mkdir(parents=True, exist_ok=True)

    os.environ[ENV_PROJECT_ROOT] = str(temp_dir)
    os.environ["DEFECTS4REST_PROJECT"] = project
    return temp_dir
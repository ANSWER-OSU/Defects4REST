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
Git utility functions for checking commits and branches.
"""
import subprocess

def sha_exists(sha):
    """
    Check if a git commit SHA exists in the repository.
    Returns True if the SHA is valid, False otherwise.
    """
    try:
        subprocess.check_output(["git", "cat-file", "-t", sha])
        return True
    except subprocess.CalledProcessError:
        return False

def get_default_branch():
    """
    Get the default branch name from the remote origin.
    Returns the default branch name (e.g., 'main', 'master').
    Falls back to 'master' if unable to determine.
    """
    try:
        output = subprocess.check_output(["git", "remote", "show", "origin"], text=True)
        for line in output.splitlines():
            if "HEAD branch" in line:
                return line.split(":")[-1].strip()
    except subprocess.CalledProcessError:
        return "master"
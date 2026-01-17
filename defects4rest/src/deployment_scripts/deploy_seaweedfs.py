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
SeaweedFS Deployment Script

Deploys SeaweedFS distributed file system using Docker Compose.Clones the repository, checks out specific SHA, and launches the service.
"""
import subprocess
import shutil
import os
import sys
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.utils.git import get_default_branch, sha_exists
from defects4rest.src.utils.issue_metadata import run_issue_hook
from defects4rest.src.api_dep_setup import seaweedfs as seaweedfs_issues

REPO_URL = "https://github.com/seaweedfs/seaweedfs.git"
PROJECT_NAME = 'seaweedfs'
PROJECT_DIR =  str(ensure_temp_project_dir(PROJECT_NAME))
COMPOSE_FILE = "seaweedfs-compose.yml"
COMPOSE_URL = f"https://raw.githubusercontent.com/seaweedfs/seaweedfs/master/docker/{COMPOSE_FILE}"
PROJECT_SUBDIR = "docker"
COMPOSE_PROJECT_NAME = "seaweedfs"

def ensure_compose_file():
    """Download docker-compose file if not present."""
    compose_path = os.path.join(PROJECT_DIR, COMPOSE_FILE)
    if not os.path.isfile(compose_path):
        pretty_step(f"Downloading compose file from {COMPOSE_URL} …")
        run(["wget", "-q", "-O", compose_path, COMPOSE_URL])
    return compose_path

def main(sha=None,issue_id=None):
    """Main deployment function for SeaweedFS."""
    # Verify prerequisites
    pretty_section(f"Deploying Seweedfs (isuue number {issue_id}) at SHA: {sha}")
    for tool in ("git", "docker", "docker-compose", "wget"):
        check_prereq(tool)

    # Remove existing repo for clean deployment
    if os.path.isdir(PROJECT_DIR):
        pretty_step(f"Removing existing repo at {PROJECT_DIR} …")
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(os.path.dirname(PROJECT_DIR), exist_ok=True)

    # Clone repository
    pretty_step(f"Cloning SeaweedFS into {PROJECT_DIR} …")
    run(["git", "clone", REPO_URL, PROJECT_DIR])

    os.chdir(PROJECT_DIR)

    # Verify SHA exists
    if not sha_exists(sha) and sha != "latest":
        pretty_step(f"SHA {sha} not found.")
        sys.exit(1)

    # Checkout specific SHA or latest
    try:
        if sha == "latest":
            run(["git", "fetch", "--all"])
            default_branch = get_default_branch()
            run(["git", "checkout", default_branch])
            run(["git", "pull", "origin", default_branch])
        elif sha:
            run(["git", "fetch", "--all", "--tags"])
            run(["git", "checkout", sha])
        else:
            run(["git", "fetch", "--all"])
            run(["git", "checkout", "main"])
            run(["git", "pull", "origin", "main"])
    except subprocess.CalledProcessError as e:
        print(f"Git checkout failed: {e}", file=sys.stderr)
        return

    compose_path = ensure_compose_file()

    # Launch SeaweedFS with Docker Compose
    pretty_subsection("\nLaunching SeaweedFS with Docker Compose …")
    run([
        "docker", "compose",
        "-f", compose_path,
        "-p", COMPOSE_PROJECT_NAME,
        "up", "-d"
    ], cwd=PROJECT_DIR)

    pretty_section("SeaweedFS is up",color="green")
    print(" Master UI ➜ http://localhost:9333/")

    # Run issue-specific setup hooks
    if issue_id:
        pretty_step("\nRunning pre-requisites for defect…")
        args = {
            "s3_url": "http://localhost:8333",
            "issue_id": issue_id
        }

        info = run_issue_hook(issue_id, args, issues_module=seaweedfs_issues)
        presigned_url = info.get("url") if info else None
        if presigned_url:
            pretty_step(f"\n Pre-requisites completed. Presigned URL: {presigned_url}")
        else:
            pretty_step("\n Pre-requisites completed, but no presigned URL returned.")

def stop():
    """Stop SeaweedFS containers."""
    pretty_section("\nStopping SeaweedFS containers …")
    if os.path.isdir(PROJECT_DIR):
        compose_path = os.path.join(PROJECT_DIR, COMPOSE_FILE)
        if not os.path.isfile(compose_path):
            print("Compose file missing.")
            return
        run([
            "docker", "compose",
            "-f", compose_path,
            "-p", COMPOSE_PROJECT_NAME,
            "stop"
        ], cwd=PROJECT_DIR)
        pretty_step("Containers stopped.")
    else:
        pretty_step("Project directory not found.")

def clean():
    """Clean up SeaweedFS containers and volumes."""
    pretty_section("\n Cleaning SeaweedFS containers and volumes …")
    if not os.path.isdir(PROJECT_DIR):
        pretty_step("Project directory not found.")
        return

    compose_path = os.path.join(PROJECT_DIR, COMPOSE_FILE)
    if not os.path.isfile(compose_path):
        pretty_step("Compose file missing.")
        return

    try:
        run([
            "docker", "compose",
            "-f", compose_path,
            "-p", COMPOSE_PROJECT_NAME,
            "down",
            "--remove-orphans",
            "--volumes"
        ], cwd=PROJECT_DIR)
        pretty_step("Cleanup complete.")
    except subprocess.CalledProcessError as e:
        pretty_step(f"Cleanup failed: {e}", file=sys.stderr)
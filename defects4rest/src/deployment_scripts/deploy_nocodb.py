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
NocoDB Deployment Script

Deploys NocoDB using Docker containers with versions determined by SHA lookups in a CSV file.
Uses SQLite with persistent volume for data storage.
"""
import subprocess
import shutil
import os
import sys
import socket
import csv
import re
import time
import requests
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.utils.issue_metadata import run_issue_hook, _load_bug_row ,resolve_docker_version_for_sha
from defects4rest.src.api_dep_setup import nocodb as nocodb_issues

# Configuration
PROJECT_NAME = 'nocodb'
PROJECT_DIR =  str(ensure_temp_project_dir(PROJECT_NAME))
DATA_DIR = PROJECT_DIR
CSV_PATH = data_csv(PROJECT_NAME)

DOCKER_REPO = "nocodb/nocodb"
CONTAINER_NAME = "nocodb"
START_PORT = 8080
CONTAINER_PORT = "8080"

# Helper functions
def find_free_port(start=START_PORT):
    """Find available port starting from given port."""
    port = start
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                port += 1

_SPLIT_SHA_RE = re.compile(r"[,\|\s;]+")

def _tokenize_shas(value: str) -> list[str]:
    """Split string containing multiple SHAs separated by delimiters."""
    if not value:
        return []
    return [tok.strip() for tok in _SPLIT_SHA_RE.split(value) if tok.strip()]

_HEX_SHA_RE = re.compile(r"\b[0-9a-fA-F]{7,40}\b")

def _extract_shas_from_text(text: str) -> list[str]:
    """Extract SHA-like tokens from arbitrary text."""
    if not text:
        return []
    return list({m.group(0) for m in _HEX_SHA_RE.finditer(text)})

def resolve_docker_tag_from_csv(sha: str, csv_path: str) -> str:
    """Determine Docker image tag based on SHA lookup in CSV."""
    if not os.path.isfile(csv_path):
        print(csv_path)
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {
            "buggy_sha", "patch_sha", "patched_files",
            "buggy_docker_version", "patched_docker_version"
        }
        missing_cols = required - set(reader.fieldnames or [])
        if missing_cols:
            raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing_cols))}")

        for row in reader:
            buggy_sha = (row.get("buggy_sha") or "").strip()
            patch_sha_field = (row.get("patch_sha") or "").strip()
            patched_files_field = (row.get("patched_files") or "").strip()

            # Check patch_sha field
            for candidate in _tokenize_shas(patch_sha_field):
                if sha == candidate:
                    tag = (row.get("patched_docker_version") or "").strip()
                    if not tag:
                        raise ValueError(
                            f"Matched patch_sha in CSV, but patched_docker_version is empty for sha={sha}"
                        )
                    return tag

            # Check buggy_sha
            if sha == buggy_sha:
                tag = (row.get("buggy_docker_version") or "").strip()
                if not tag:
                    raise ValueError(
                        f"Matched buggy_sha in CSV, but buggy_docker_version is empty for sha={sha}"
                    )
                return tag

            # Fallback: extract from patched_files text
            if not patch_sha_field:
                for candidate in _extract_shas_from_text(patched_files_field):
                    if sha == candidate:
                        tag = (row.get("patched_docker_version") or "").strip()
                        if not tag:
                            raise ValueError(
                                f"Matched SHA in patched_files, but patched_docker_version is empty for sha={sha}"
                            )
                        return tag

    raise ValueError(f"SHA {sha} not found in CSV (neither in patch_sha nor buggy_sha, "
                     f"and not inferred from patched_files).")

def wait_for_server(url, timeout=60):
    """Poll URL until server responds or timeout."""
    print("Waiting for server to start...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            time.sleep(1)
    print("Timeout waiting for server.")
    return False

def main(sha=None,issue_id=None):
    """Main deployment function for NocoDB."""
    pretty_section(f"Deploying Nocodb (isuue number {issue_id}) at SHA: {sha}")
    check_prereq("docker")

    if not sha:
        pretty_step("Error: please provide a sha (or 'latest').",color="red")
        sys.exit(1)

    # Determine Docker tag from SHA
    if sha == "latest":
        docker_tag = "latest"
    else:
        try:
            docker_tag = resolve_docker_tag_from_csv(sha, CSV_PATH)
        except Exception as e:
            print(f"Failed to resolve docker tag from CSV: {e}")
            sys.exit(1)

    image_ref = f"{DOCKER_REPO}:{docker_tag}"
    pretty_step(f"\nUsing Docker image: {image_ref}")

    # Setup data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # Remove existing container
    pretty_subsection("Stopping existing container …")
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Pull Docker image
    pretty_subsection(f"\nPulling image {image_ref} …")
    try:
        run(["docker", "pull", image_ref])
    except subprocess.CalledProcessError as e:
        pretty_step(f"docker pull failed: {e}",color="red")
        sys.exit(1)

    # Find available port
    host_port = find_free_port()
    if host_port != START_PORT:
        pretty_step(f"Port {START_PORT} in use. Using port {host_port} instead.")

    # Run container with persistent volume
    pretty_section(f"\nRunning NocoDB at http://localhost:{host_port}/dashboard …")
    run([
        "docker", "run", "-d",
        "--name", CONTAINER_NAME,
        "-v", f"{DATA_DIR}:/usr/app/data/",
        "-p", f"{host_port}:{CONTAINER_PORT}",
        image_ref
    ])

    # Wait for server to be ready
    wait_for_server(f"http://localhost:{host_port}/dashboard")
    pretty_section(f"\nNocoDB container is running ")
    pretty_step(f"http://localhost:{host_port}/dashboard")

    # Run post-deployment hooks
    args = {
        "issue_id": issue_id,
        "project": "nocodb",
        "extra_flag": True,
        "port": host_port
    }
    run_issue_hook(issue_id, args, issues_module = nocodb_issues)

def stop():
    """Stop NocoDB container."""
    pretty_section("Stopping NocoDB container …")
    subprocess.run(["docker", "stop", CONTAINER_NAME], check=False)
    pretty_step("Container stopped.")

def clean():
    """Clean up NocoDB container and data directory."""
    pretty_section("Cleaning up NocoDB container, image, and data …")
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], check=False)
    try:
        shutil.rmtree(DATA_DIR)
        pretty_step(f"Removed data directory: {DATA_DIR}")
    except Exception as e:
        pretty_section(f"Could not remove data directory: {e}")
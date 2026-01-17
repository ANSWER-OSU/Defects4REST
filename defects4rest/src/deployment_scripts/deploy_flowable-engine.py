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
Flowable Engine Deployment Script
This script deploys specific versions of Flowable REST API using Docker containers.
It uses a CSV file to map bug IDs and SHA commits to pre-built Docker images.
"""
import csv
import shlex
import sys
from pathlib import Path
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import data_csv, check_prereq

CSV_PATH = data_csv("flowable-engine")

# Docker image configuration
DEFAULT_IMAGE_REPO = "flowable/flowable-rest"
DEFAULT_PORT = "8080"
NAME_PREFIX = "flowable-rest-bug"

def _load_all_rows(csv_path: str) -> list[dict[str, str]]:
    """Load all rows from bug metadata CSV."""
    csv_file = Path(csv_path)
    if not csv_file.is_file():
        pretty_step(f"CSV not found: {csv_file}", color="red")
        sys.exit(2)
    with csv_file.open(newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        pretty_step(f"CSV has no data rows: {csv_file}", color="red")
        sys.exit(2)
    return rows

def _find_row_for_sha(sha: str, rows: list[dict[str, str]]) -> dict:
    """Find CSV row matching the given SHA."""
    if not sha:
        pretty_step("SHA is required to select a Flowable bug row", color="red")
        sys.exit(2)

    # Check buggy_sha column
    for row in rows:
        if sha == (row.get("buggy_sha") or "").strip():
            return row

    # Check patch_sha column
    for row in rows:
        patch_field = (row.get("patch_sha") or "").strip()
        patches = [s.strip() for s in patch_field.split("|") if s.strip()] if patch_field else []
        if sha in patches:
            return row

    pretty_step(f"No CSV row with buggy_sha or patch_sha matching {sha}", color="red")
    sys.exit(2)

def _decide_variant(row: dict[str, str], sha: str | None, prefer: str | None) -> str:
    """Determine whether to deploy buggy or patched variant."""
    if prefer in {"buggy", "patched"}:
        return prefer

    buggy_sha = (row.get("buggy_sha") or "").strip()
    patch_field = (row.get("patch_sha") or "").strip()
    patches = [s.strip() for s in patch_field.split("|") if s.strip()] if patch_field else []

    # Auto-detect based on SHA
    if sha and sha == buggy_sha:
        return "buggy"
    if sha and sha in patches:
        return "patched"

    return "patched" if row.get("patched_docker_version") else "buggy"

def _image_for(row: dict[str, str], variant: str) -> str:
    """Get full Docker image name for specified variant."""
    tag = (row.get("buggy_docker_version") if variant == "buggy" else row.get("patched_docker_version") or "").strip()
    if not tag:
        pretty_step(f"CSV missing docker tag for variant '{variant}'.", color="red")
        sys.exit(2)
    return f"{DEFAULT_IMAGE_REPO}:{tag}"

def _bug_id(row: dict[str, str]) -> int:
    """Extract bug ID from CSV row."""
    bid_str = (row.get("bug_id") or "").strip()
    try:
        return int(bid_str)
    except ValueError:
        pretty_step(f"Non-integer bug_id in CSV row: {bid_str!r}", color="red")
        sys.exit(2)

def main(sha =  None,issue_id=None):
    """Main deployment function for Flowable REST."""
    port = DEFAULT_PORT
    detach = False
    variant = None
    pretty_section(f"Deploying Flowable REST (issue {issue_id}) at SHA: {sha}")
    check_prereq("docker")

    if not sha:
        pretty_step("SHA is required for deployment", color="red")
        sys.exit(2)

    # Load metadata and find matching row
    rows = _load_all_rows(CSV_PATH)
    row = _find_row_for_sha(sha, rows)

    # Determine configuration
    chosen_variant = _decide_variant(row, sha, variant)
    image = _image_for(row, chosen_variant)
    bind_port = int(port)
    name = "flowable-rest"

    # Pull Docker image
    pretty_subsection(f"Pulling Docker image {image} …")
    run(["docker", "pull", image])

    # Remove existing container if present
    remove_cmd = (
        f"if docker ps -a --format '{{{{.Names}}}}' | grep -qx {shlex.quote(name)}; then "
        f"  echo 'Removing existing container {name} ...'; "
        f"  docker rm -f {shlex.quote(name)} || true; "
        f"fi"
    )
    run(["bash", "-lc", remove_cmd])  # nosec

    # Launch container
    pretty_subsection(f"Launching container {name} …")
    run([
        "docker", "run", "-d",
        "--name", name,
        "-p", f"{bind_port}:8080",
        "--restart", "unless-stopped",
        image,
    ])

    pretty_section("Flowable REST is ready", color="green")
    pretty_step(f"flowable-rest is available at: http://localhost:{bind_port}/flowable-rest/")

def stop():
    """Stop all running Flowable REST bug containers."""
    pretty_section("Stopping Flowable REST containers …")
    check_prereq("docker")

    # Find and remove all bug containers
    script = r"""
set -euo pipefail
for n in $(docker ps -a --format '{{.Names}}' | grep -E '^flowable-rest-bug[0-9]+-(buggy|patched)$' || true); do
  echo "Removing $n ..."
  docker rm -f "$n" || true
done
"""
    run(["bash", "-lc", script])  # nosec
    pretty_step("Stopped all Flowable REST bug containers.")

def clean():
    """Complete cleanup of Flowable REST deployment."""
    pretty_section("Cleaning Flowable REST deployment …")
    stop()
    pretty_step("Cleanup complete")
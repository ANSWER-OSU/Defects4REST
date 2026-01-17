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
Signal CLI REST API Deployment Script

Deploys signal-cli-rest-api using Docker containers with versions determined by SHA lookups in a CSV file.
"""

from __future__ import annotations
import argparse
import csv
import os
import shlex
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from defects4rest.src.utils.shell import run, pretty_step, pretty_section
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.utils.issue_metadata import _load_bug_row

PROJECT_NAME = 'signal-cli-rest-api'
PROJECT_DIR =  str(ensure_temp_project_dir(PROJECT_NAME))
CSV_PATH = data_csv(PROJECT_NAME)
REPO_URL = "https://github.com/bbernhard/signal-cli-rest-api.git"

# Configuration defaults
COMPOSE_FILE = "docker-compose.yml"
DEFAULT_PORT = "8080"
DEFAULT_MODE = "native"
DEFAULT_CONFIG = os.path.expanduser("~/.local/share/signal-cli")
DEFAULT_IMAGE_REPO = "bbernhard/signal-cli-rest-api"
NAME_PREFIX = "signal-cli-bug"

def check_prereq(bin_name: str):
    """Verify required binary is available."""
    if not shutil.which(bin_name):
        print(f"ERROR: required binary '{bin_name}' not found in PATH")
        sys.exit(2)

@dataclass
class BugRow:
    """Container for bug metadata from CSV."""
    bug_id: int
    buggy_sha: str | None
    patch_sha: str | None
    buggy_docker_version: str | None
    patched_docker_version: str | None

    @property
    def default_buggy_port(self) -> int:
        """Calculate default port for buggy variant (80XX)."""
        return int(f"80{self.bug_id:02d}")

    @property
    def default_patched_port(self) -> int:
        """Calculate default port for patched variant (81XX)."""
        return int(f"81{self.bug_id:02d}")

REQUIRED_COLUMNS = {
    "bug_id",
    "buggy_sha",
    "patch_sha",
    "buggy_docker_version",
    "patched_docker_version",
}

def _load_bug_row(csv_path: str, sha: str | None) -> "BugRow":
    """Load bug metadata from CSV based on SHA."""
    p = Path(csv_path)
    if not p.is_file():
        print(f"ERROR: CSV not found: {csv_path}")
        sys.exit(2)

    data = p.read_text(encoding="utf-8", errors="replace")
    try:
        dialect = csv.Sniffer().sniff(data[:2048])
    except csv.Error:
        dialect = csv.get_dialect("excel")

    reader = csv.DictReader(data.splitlines(), dialect=dialect)
    rows = []
    for r in reader:
        rr = { (k or "").lower(): (v or "").strip() for k, v in r.items() }
        if rr:
            rows.append(rr)

    if not sha:
        print("ERROR: sha is required to resolve the CSV row when calling _load_bug_row(csv_path, sha)")
        sys.exit(2)

    chosen = None

    # Check buggy_sha first
    for rr in rows:
        if sha == rr.get("buggy_sha"):
            chosen = rr
            break
    # Then check patch_sha
    if not chosen:
        for rr in rows:
            patch_vals = rr.get("patch_sha", "")
            patch_list = [s.strip() for s in patch_vals.split("|") if s.strip()]
            if sha in patch_list:
                chosen = rr
                break

    if not chosen:
        print(f"ERROR: No CSV row with buggy_sha or patch_sha matching {sha}")
        sys.exit(2)

    try:
        bid = int((chosen.get("bug_id") or "").strip())
    except ValueError:
        print(f"ERROR: Non-integer bug_id in matched CSV row: {chosen.get('bug_id')}")
        sys.exit(2)

    return BugRow(
        bug_id=bid,
        buggy_sha=(chosen.get("buggy_sha") or None),
        patch_sha=(chosen.get("patch_sha") or None),
        buggy_docker_version=(chosen.get("buggy_docker_version") or None),
        patched_docker_version=(chosen.get("patched_docker_version") or None),
    )

def _decide_variant(row: BugRow, sha: str | None, prefer: str | None) -> str:
    """Determine whether to deploy buggy or patched variant."""
    if prefer in {"buggy", "patched"}:
        return prefer
    if sha and row.buggy_sha and sha == row.buggy_sha:
        return "buggy"
    if sha and row.patch_sha and sha == row.patch_sha:
        return "patched"
    return "patched" if row.patched_docker_version else "buggy"

def _image_for(row: BugRow, variant: str) -> str:
    """Get full Docker image name for variant."""
    tag = row.buggy_docker_version if variant == "buggy" else row.patched_docker_version
    if not tag:
        print(f"ERROR: CSV missing docker tag for variant '{variant}'.")
        sys.exit(2)
    return f"{DEFAULT_IMAGE_REPO}:{tag}"

def _default_port(row: BugRow, variant: str, override_port: str | None) -> int:
    """Determine port to bind container to."""
    if override_port:
        return int(override_port)
    return row.default_buggy_port if variant == "buggy" else row.default_patched_port

def _container_name(row: BugRow, variant: str) -> str:
    """Generate unique container name."""
    return f"{NAME_PREFIX}{row.bug_id}-{variant}"

def main(sha = None,issue_id=None,port: str = DEFAULT_PORT,mode: str = DEFAULT_MODE,config_dir: str = DEFAULT_CONFIG,detach: bool = False, *,bug_id: int | None = None,variant: str | None = None):
    """Main deployment function for signal-cli-rest-api."""
    pretty_section(f"Deploying signal-cli-rest-api (isuue number {issue_id}) at SHA: {sha}")
    check_prereq("docker")

    # Load bug metadata and determine configuration
    row = _load_bug_row(CSV_PATH, sha)
    bug_id =row.bug_id
    chosen = _decide_variant(row, sha, variant)
    image = _image_for(row, chosen)
    bind_port = _default_port(row, chosen, port if port != DEFAULT_PORT or bug_id is None else None)

    # Ensure config directory exists
    cfg = Path(os.path.expanduser(config_dir))
    cfg.mkdir(parents=True, exist_ok=True)

    name = _container_name(row, chosen)

    # Pull Docker image
    run(["docker", "pull", image])

    # Remove existing container if present
    run(["bash", "-lc", f"if docker ps -a --format '{{{{.Names}}}}' | grep -qx {shlex.quote(name)}; then docker rm -f {shlex.quote(name)}; fi"])  # nosec

    # Launch container
    cmd = [
        "docker", "run", "-d",
        "--name", name,
        "-p", f"{bind_port}:8080",
        "-e", f"MODE={mode}",
        "-e", "SIGNAL_CLI_CONFIG_DIR=/home/.local/share/signal-cli",
        "-v", f"{cfg}:/home/.local/share/signal-cli",
        "--restart", "unless-stopped",
        image,
    ]
    run(cmd)
    pretty_section("signal-cli-rest-api is ready", color="green")
    print("\n----------------------------------------")
    print(f"Variant     : {chosen}")
    print(f"Bug ID      : {row.bug_id}")
    print(f"Container   : {name}")
    print(f"Image       : {image}")
    print(f"Mode        : {mode}")
    print(f"Config mount: {cfg} → /home/.local/share/signal-cli")
    print(f"API URL     : http://localhost:{bind_port}/v1/qrcodelink?device_name=signal-api")
    print("----------------------------------------\n")

def stop():
    """Stop all signal-cli-rest-api bug containers."""
    pretty_section("Stopping signal-cli-rest-api containers …")
    check_prereq("docker")
    # Find and remove all containers matching naming pattern
    script = r"""
set -euo pipefail
for n in $(docker ps -a --format '{{.Names}}' | grep -E '^signal-cli-bug[0-9]+-(buggy|patched)$' || true); do
  echo "Removing $n ..."
  docker rm -f "$n" || true
done
"""
    run(["bash", "-lc", script])  # nosec
    pretty_step("Stopped.")

def clean():
    """Clean up signal-cli-rest-api deployment."""
    pretty_section("Clearing NetBox containers …")
    stop()
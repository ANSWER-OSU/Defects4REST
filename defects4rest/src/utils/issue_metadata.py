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
Bug information retrieval and management utilities for defects4rest projects.

Provides functions to query bug data from CSV files, resolve Docker versions,
and manage bug-specific hooks.
"""
import csv
import sys
from pathlib import Path
import pandas as pd
from dataclasses import dataclass
from defects4rest.src.utils.resources import data_csv


def get_bug_info(project_name, issue_id):
    """
    Retrieve bug information as a dictionary for programmatic use.

    Reads bug data from the project's CSV file and returns a dictionary containing
    the CSV path, buggy SHA, and list of patched SHAs.

    Args:
        project_name (str): The name of the project.
        issue_id: The issue number/ID to look up.

    Returns:
        dict: A dictionary with keys 'csv_path', 'buggy', and 'patched', or
              None if the project or issue is not found.
    """
    # Get the path to the project's CSV file
    csv_res = data_csv(project_name)
    # Return None if the CSV file doesn't exist
    if not csv_res.is_file():
        return None

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(str(csv_res))
    # Filter to find the row matching the given issue_id
    row = df[df["issue_no"] == issue_id]

    # Return None if the issue was not found
    if row.empty:
        return None

    # Extract the first matching row
    row = row.iloc[0]

    # Extract the buggy SHA
    buggy_sha = row.get("buggy_sha", None)
    # Extract the patch SHA(s) field
    patch_sha_field = row.get("patch_sha", None)

    # Parse patch SHAs into a list
    patched_shas = []
    if patch_sha_field is not None and pd.notna(patch_sha_field):
        # Split and clean multiple patch SHAs
        patched_shas = [sha.strip() for sha in str(patch_sha_field).split(" | ") if sha.strip()]

    # Return a dictionary with the bug information
    return {
        "csv_path": str(csv_res),  # Path to the CSV file
        "buggy": buggy_sha.strip() if isinstance(buggy_sha, str) else None,  # Buggy version SHA
        "patched": patched_shas,  # List of patch SHAs
    }


def _load_bug_row(csv_path: str, sha: str | None) -> "BugRow":
    """
    Load bug row from CSV by matching the given SHA (either buggy or patched).

    Args:
        csv_path: Path to the CSV file containing bug data.
        sha: Git commit SHA to match against buggy_sha or patch_sha columns.

    Returns:
        BugRow: Dataclass containing bug information.
    """
    p = Path(csv_path)
    if not p.is_file():
        print(f"ERROR: CSV not found: {csv_path}")
        sys.exit(2)

    # Read and parse CSV with automatic dialect detection
    data = p.read_text(encoding="utf-8", errors="replace")
    try:
        dialect = csv.Sniffer().sniff(data[:2048])
    except csv.Error:
        dialect = csv.get_dialect("excel")

    reader = csv.DictReader(data.splitlines(), dialect=dialect)
    # Normalize keys to lowercase and strip values
    rows = []
    for r in reader:
        rr = {(k or "").lower(): (v or "").strip() for k, v in r.items()}
        if rr:
            rows.append(rr)

    if not sha:
        print("ERROR: sha is required to resolve the CSV row when calling _load_bug_row(csv_path, sha)")
        sys.exit(2)

    chosen = None

    # First, try to match buggy_sha
    for rr in rows:
        if sha == rr.get("buggy_sha"):
            chosen = rr
            break

    # If not found, try to match patch_sha (may be pipe-separated list)
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

    # Extract and validate bug_id
    try:
        bid = int((chosen.get("bug_id") or "").strip())
    except ValueError:
        print(f"ERROR: Non-integer bug_id in matched CSV row: {chosen.get('bug_id')}")
        sys.exit(2)

    # Build BugRow using existing dataclass defined below
    return BugRow(
        bug_id=bid,
        buggy_sha=(chosen.get("buggy_sha") or None),
        patch_sha=(chosen.get("patch_sha") or None),
        buggy_docker_version=(chosen.get("buggy_docker_version") or None),
        patched_docker_version=(chosen.get("patched_docker_version") or None),
    )


def resolve_docker_version_for_sha(row, sha: str) -> tuple[str, str]:
    """
    Determine if SHA is buggy or patched version and return corresponding Docker version.

    Args:
        row: BugRow object containing bug information.
        sha: Git commit SHA to check.

    Returns:
        tuple: (variant, docker_version) where variant is "buggy" or "patched".
    """
    # Normalize patch_sha in case it's a "|" separated list
    patch_sha = (row.patch_sha or "").strip()
    patch_list = [s.strip() for s in patch_sha.split("|") if s.strip()]

    if sha == (row.buggy_sha or "").strip():
        variant = "buggy"
        docker_version = row.buggy_docker_version
    elif sha in patch_list:
        variant = "patched"
        docker_version = row.patched_docker_version
    else:
        # Fallback: if _load_bug_row already matched this row, then sha must be
        # either the buggy or one of the patch shas — if we get here something is wrong.
        raise ValueError(
            f"SHA {sha} does not match buggy_sha={row.buggy_sha!r} "
            f"or patch_sha={row.patch_sha!r} for bug_id={row.bug_id}"
        )

    if not docker_version:
        raise ValueError(
            f"No docker version set for variant '{variant}' in row for bug_id={row.bug_id}"
        )

    return variant, docker_version


def run_issue_hook(issue, args, issues_module):
    """
    Execute project-specific issue handler if defined.

    Looks for issue-specific handler (e.g., issue_1, issue_2) in issues_module,
    falls back to default handler if available.
    """
    if issue is None:
        return

    func_name = f"issue_{issue}"  # issue_1, issue_2, ...
    handler = getattr(issues_module, func_name, None)

    if handler:
        handler(args)
    else:
        # Optional: default fallback per project
        default = getattr(issues_module, "default", None)
        if default:
            default(args)


@dataclass
class BugRow:
    """
    Represents a single bug entry from the CSV with metadata for both buggy and patched versions.
    """
    bug_id: int
    buggy_sha: str | None
    patch_sha: str | None
    buggy_docker_version: str | None
    patched_docker_version: str | None

    @property
    def default_buggy_port(self) -> int:
        """Generate default port for buggy version (80XX format)."""
        return int(f"80{self.bug_id:02d}")

    @property
    def default_patched_port(self) -> int:
        """Generate default port for patched version (81XX format)."""
        return int(f"81{self.bug_id:02d}")
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

import os
import subprocess
import sys

from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.git import get_default_branch
from defects4rest.src.utils.resources import ensure_temp_project_dir

REPO_URL = "https://github.com/containers/podman.git"
PROJECT_NAME = 'podman'
CLONE_DIR = str(ensure_temp_project_dir(PROJECT_NAME))

# Hardcoded build settings
BUILDTAGS = "selinux seccomp"
PREFIX = "/usr"

# Issue IDs for bugs that require rootless mode
ROOTLESS_BUGS= [25881]

def ensure_go_version():
    """
    Ensure Go 1.16+ is installed and available in PATH.
    """
    try:
        out = subprocess.check_output(["go", "version"], text=True)
        ver = out.split()[2].lstrip("go")
        major, minor, *_ = ver.split(".")
        if int(major) < 1 or (int(major) == 1 and int(minor) < 16):
            sys.exit("Go 1.16+ is required; please install a newer Go toolchain first.")
    except FileNotFoundError:
        sys.exit("go not found in PATH. Please install Go 1.16 or newer.")


def main(sha=None,issue_id=None):
    # Basic environment checks
    pretty_section(f"Deploying podman (issue number {issue_id}) at SHA: {sha}")
    if not sys.platform.startswith("linux"):
        sys.exit("Linux host required to install Podman.")

    if os.geteuid() != 0:
        sys.exit("Sudo required. Please re-run with sudo.")

    ensure_go_version()

    # Clone or update repository
    if os.path.isdir(os.path.join(CLONE_DIR, '.git')):
        pretty_step(f"Repo exists—fetching updates in {CLONE_DIR}")
        run(["git", "-C", CLONE_DIR, "fetch", "--all", "--tags"])
    else:
        pretty_step(f"Cloning Podman into {CLONE_DIR}…")
        run(["git", "clone", REPO_URL, CLONE_DIR])

    os.chdir(CLONE_DIR)

    # Checkout the requested SHA / branch
    try:
        if sha == "latest":
            default_branch = get_default_branch(CLONE_DIR)
            pretty_step(f"'latest' requested—checking out default branch '{default_branch}'")
            run(["git", "checkout", default_branch])
            run(["git", "pull", "origin", default_branch])
        elif sha:
            pretty_step(f"Checking out '{sha}'…")
            run(["git", "checkout", sha])
        else:
            pretty_step("No SHA provided—defaulting to 'main'")
            run(["git", "checkout", "main"])
            run(["git", "pull", "origin", "main"])
    except subprocess.CalledProcessError as e:
        sys.exit(f"Git checkout failed: {e}")


    pretty_step(f"Building with BUILDTAGS='{BUILDTAGS}' PREFIX={PREFIX}")
    build_args = ["make", f"BUILDTAGS={BUILDTAGS}", f"PREFIX={PREFIX}"]

    # Main podman binary
    run(build_args + ["bin/podman"])


    helpers = [
        ("rootlessport", os.path.join(CLONE_DIR, "cmd", "rootlessport"), "bin/rootlessport"),
        ("quadlet",      os.path.join(CLONE_DIR, "cmd", "quadlet"),      "bin/quadlet"),
    ]

    for name, src_dir, target in helpers:
        if os.path.isdir(src_dir):
            pretty_step(f"Building {name} helper…")
            run(build_args + [target])
        else:
            pretty_step(f"{src_dir} not found, skipping {name} build")

    pretty_step("Installing podman (binaries only, skipping manpages and extra targets)…")
    env = os.environ.copy()
    env["PATH"] = f"{CLONE_DIR}/bin:" + env.get("PATH", "")

    run(["make", "install.bin", f"PREFIX={PREFIX}"], env=env)

    # Show Podman version info
    run(["podman", "version"])


    # For bugs that need rootless mode
    if issue_id in ROOTLESS_BUGS:
        pretty_section("Bug requires rootless mode. Please proceed to run `podman system service -t 0 tcp:127.0.0.1:8082` to start rootless server.")
    else:
        pretty_step("Starting Podman REST API Server...")
        subprocess.Popen(
            ["sudo", "podman", "system", "service", "-t", "0", "tcp:127.0.0.1:8082"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        pretty_section("Podman is up and running at http://127.0.0.1:8082")


def clean():
    pretty_section("Cleaning Podman containers, networks, images and volumes (prefix d4rest_*)")

    prefix = "d4rest_"

    # Stop TCP service
    pretty_step("Stopping Podman API service...")
    subprocess.run(["pkill", "-f", "podman system service"], check=False)

    # Remove containers
    pretty_step("Removing containers...")
    subprocess.run(f"podman ps -a --format '{{{{.Names}}}}' | grep '^{prefix}' | xargs -r podman rm -f", shell=True, check=False)

    # Remove images
    pretty_step("Removing images...")
    subprocess.run(f"podman images --format '{{{{.Repository}}}}' | grep '^{prefix}' | xargs -r podman rmi -f", shell=True, check=False)

    # Remove volumes
    pretty_step("Removing volumes...")
    subprocess.run(f"podman volume ls --format '{{{{.Name}}}}' | grep '^{prefix}' | xargs -r podman volume rm -f", shell=True, check=False)

    # Remove networks (optional)
    pretty_step("Removing networks...")
    subprocess.run(f"podman network ls --format '{{{{.Name}}}}' | grep '^{prefix}' | xargs -r podman network rm -f", shell=True, check=False)

    pretty_section("Podman cleanup complete.")

def stop():
    clean()

if __name__ == "__main__":
    main()

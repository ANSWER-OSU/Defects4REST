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
REST Countries Deployment Script

Deploys REST Countries API by building from source using Maven in Docker and deploying the resulting WAR file to a Tomcat container.
"""
import argparse
import subprocess
import shutil
import os
import sys
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.utils.git import get_default_branch, sha_exists

REPO_URL = "https://github.com/apilayer/restcountries.git"
PROJECT_NAME = 'restcountries'
PROJECT_DIR =  str(ensure_temp_project_dir(PROJECT_NAME))

# Docker images for build and runtime
DOCKER_MVN_IMAGE = "maven:3.9.0-eclipse-temurin-8"
TOMCAT_IMAGE = "tomcat:8.5-jdk8-openjdk"
CONTAINER_NAME = "restcountries-tomcat"
HOST_PORT = "8080"

def current_sha():
    """Return current git HEAD SHA."""
    out = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_DIR,
        text=True
    ).strip()
    return out

def safe_rmtree(path: str):
    """Remove directory with safety check to prevent accidental deletion of critical paths."""
    path = os.path.abspath(path)
    if path in ("/", os.path.expanduser("~")):
        raise RuntimeError(f"Refusing to delete dangerous path: {path}")
    shutil.rmtree(path)

def main(sha=None, issue_id=None):
    """Main deployment function for REST Countries."""
    pretty_section(f"Deploying REST Countries (issue number {issue_id}) at SHA: {sha}")

    # Verify prerequisites
    for tool in ("git", "docker"):
        check_prereq(tool)

    # Remove existing repo for clean build
    if os.path.isdir(PROJECT_DIR):
        pretty_step(f"Removing existing repo at {PROJECT_DIR} …")
        safe_rmtree(PROJECT_DIR)

    # Clone repository (use fork for specific issue)
    pretty_subsection("Cloning REST Countries repository …")
    if issue_id == 235 and sha == "01769a8efaef544ddab2f1f044aa7f7172c8db56":
        run(["git", "clone", "https://github.com/plokhotnyuk/restcountries.git", PROJECT_DIR])
    else:
        run(["git", "clone", REPO_URL, PROJECT_DIR])

    os.chdir(PROJECT_DIR)

    # Checkout specific SHA or latest
    try:
        pretty_step("Checking out specific SHA …")
        if sha:
            if sha == "latest":
                pretty_step("Pulling latest default branch …")
                run(["git", "fetch", "--all"])
                default_branch = get_default_branch()
                pretty_step(f"Using default branch: {default_branch}")
                run(["git", "checkout", default_branch])
                run(["git", "pull", "origin", default_branch])
            else:
                if not sha_exists(sha):
                    pretty_step(f"SHA {sha} not found locally; fetching …")
                    run(["git", "fetch", "--all", "--tags"])
                pretty_step(f"Checking out SHA: {sha}")
                run(["git", "checkout", sha])
    except subprocess.CalledProcessError as e:
        sys.exit(1)

    pretty_step(f"Building commit: {current_sha()}")

    # Build WAR file using Maven in Docker
    pretty_step("Building WAR via Docker Maven …")
    abs_dir = os.path.abspath(PROJECT_DIR)
    run([
        "docker", "run", "--rm",
        "-v", f"{abs_dir}:/usr/src/app",
        "-w", "/usr/src/app",
        DOCKER_MVN_IMAGE,
        "mvn", "clean", "package", "-DskipTests"
    ])

    # Find the generated WAR file
    pretty_step("Locating WAR artifact …")
    target_dir = os.path.join(PROJECT_DIR, "target")
    wars = [f for f in os.listdir(target_dir) if f.startswith("restcountries-") and f.endswith(".war")]

    if not wars:
        pretty_step("WAR file not found in target/ directory", color="red")
        sys.exit(1)

    war_file = max(wars, key=lambda f: os.path.getmtime(os.path.join(target_dir, f)))
    war_path = os.path.join(PROJECT_DIR, "target", war_file)
    pretty_step(f"Using WAR: {war_file}")

    # Deploy to Tomcat container
    pretty_step("Deploying WAR to Tomcat …")
    stop()
    run([
        "docker", "run", "-d",
        "--name", CONTAINER_NAME,
        "-p", f"{HOST_PORT}:8080",
        "-v", f"{war_path}:/usr/local/tomcat/webapps/restcountries.war",
        TOMCAT_IMAGE
    ])
    pretty_section("REST Countries is ready", color="green")
    pretty_step(f"RestCountries is available at: http://localhost:{HOST_PORT}/restcountries/rest/v2/all")

def stop():
    """Stop and remove REST Countries container."""
    pretty_section("Stopping REST Countries container …")
    existing = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={CONTAINER_NAME}"],
        capture_output=True, text=True
    ).stdout.strip()

    if existing:
        run(["docker", "stop", CONTAINER_NAME])
        run(["docker", "rm", CONTAINER_NAME])
        pretty_step("Container stopped and removed")
    else:
        pretty_step("No running container found")

def clean():
    """Clean up REST Countries deployment."""
    pretty_section("Cleaning REST Countries deployment …")
    stop()
    pretty_step("Cleanup complete")
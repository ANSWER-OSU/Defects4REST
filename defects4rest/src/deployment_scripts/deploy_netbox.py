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
NetBox Deployment Script

This script deploys NetBox using Docker containers.
The deployment uses pre-built Docker images from Docker Hub, with versions determined by SHA lookups in a CSV file.
"""
import subprocess
import shutil
import os
import secrets
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.utils.issue_metadata import run_issue_hook, _load_bug_row ,resolve_docker_version_for_sha
from defects4rest.src.api_dep_setup import netbox as nocodb_issues
import time

REPO_URL = "https://github.com/netbox-community/netbox-docker.git"

PROJECT_NAME = 'netbox'
PROJECT_DIR =  str(ensure_temp_project_dir(PROJECT_NAME))

ENV_DIR = "env"
DEFAULT_PORT = "8080"

# Container configuration
NETWORK_NAME = "netbox-net"
PG_CONTAINER = "netbox-postgres"
REDIS_CONTAINER = "netbox-redis"
NETBOX_CONTAINER = "netbox"

# Database credentials
DB_NAME = "netbox"
DB_USER = "netbox"
DB_PASSWORD = "netbox"

CSV_PATH = data_csv(PROJECT_NAME)

def write_override(port):
    """Create docker-compose.override.yml for port mapping (currently unused)."""
    override_path = os.path.join(PROJECT_DIR, "docker-compose.override.yml")
    with open(override_path, "w") as f:
        f.write(
            "version: '3.8'\n"
            "services:\n"
            "  netbox:\n"
            f"    ports:\n"
            f"      - \"{port}:8080\"\n"
        )
    print(f"Wrote port override: {port} -> 8080")

def setup_env():
    """Copy .env.example to .env if needed (currently unused)."""
    sample = os.path.join(ENV_DIR, ".env.example")
    target = os.path.join(ENV_DIR, ".env")
    if os.path.exists(sample) and not os.path.exists(target):
        print(f"Copying {sample} → {target}")
        shutil.copy(sample, target)

def ensure_network():
    """Create dedicated Docker bridge network for NetBox containers."""
    # List existing networks
    result = subprocess.run(
        ["docker", "network", "ls", "--format", "{{.Name}}"],
        check=True,
        capture_output=True,
        text=True,
    )
    networks = result.stdout.splitlines()

    # Remove if exists
    if NETWORK_NAME in networks:
        print(f"Removing existing docker network '{NETWORK_NAME}' …")
        subprocess.run(
            ["docker", "network", "rm", NETWORK_NAME],
            check=True,
        )

    # Create network
    print(f"Creating docker network '{NETWORK_NAME}' …")
    subprocess.run(
        ["docker", "network", "create", NETWORK_NAME],
        check=True,
    )

def ensure_postgres():
    """Start PostgreSQL container for NetBox database."""
    # Check if container exists
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, )
    names = result.stdout.decode().splitlines()
    if PG_CONTAINER in names:
        print(f"Postgres container '{PG_CONTAINER}' already exists – leaving it as is.")
        return

    # Create volume and launch container
    print(f"Starting Postgres container '{PG_CONTAINER}' …")
    run(["docker", "volume", "create", "netbox_postgres"])

    run([
        "docker", "run", "-d",
        "--name", PG_CONTAINER,
        "--network", NETWORK_NAME,
        "-e", f"POSTGRES_DB={DB_NAME}",
        "-e", f"POSTGRES_USER={DB_USER}",
        "-e", f"POSTGRES_PASSWORD={DB_PASSWORD}",
        "-v", "netbox_postgres:/var/lib/postgresql/data",
        "postgres:15",
    ])

def ensure_redis():
    """Start Redis container for caching and task queue."""
    # Check if container exists
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, )
    names = result.stdout.decode().splitlines()
    if REDIS_CONTAINER in names:
        print(f"Redis container '{REDIS_CONTAINER}' already exists – leaving it as is.")
        return

    # Create volume and launch container
    print(f"Starting Redis container '{REDIS_CONTAINER}' …")
    run(["docker", "volume", "create", "netbox_redis"])

    run([
        "docker", "run", "-d",
        "--name", REDIS_CONTAINER,
        "--network", NETWORK_NAME,
        "-v", "netbox_redis:/data",
        "redis:7", "redis-server", "--appendonly", "yes",
    ])

def deploy(image_tag: str, port: str, create_superuser: bool = True):
    """Deploy NetBox application container."""
    full_image = f"netboxcommunity/netbox:v{image_tag}"
    pretty_section(f"Using NetBox image: {full_image}")

    # Remove existing container
    result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, )
    names = result.stdout.decode().splitlines()
    if NETBOX_CONTAINER in names:
        print(f"Removing existing NetBox container '{NETBOX_CONTAINER}' …")
        run(["docker", "rm", "-f", NETBOX_CONTAINER])

    # Generate secure secret key
    secret_key = secrets.token_urlsafe(64)

    # Launch NetBox container
    print(f"Starting NetBox container '{NETBOX_CONTAINER}' on port {port} …")
    run([
        "docker", "run", "-d",
        "--name", NETBOX_CONTAINER,
        "--network", NETWORK_NAME,
        "-p", f"{port}:8080",

        # Django configuration
        "-e", f"SECRET_KEY={secret_key}",

        # Database connection
        "-e", f"DB_NAME={DB_NAME}",
        "-e", f"DB_USER={DB_USER}",
        "-e", f"DB_PASSWORD={DB_PASSWORD}",
        "-e", f"DB_HOST={PG_CONTAINER}",
        "-e", "DB_PORT=5432",

        # Redis connection
        "-e", f"REDIS_HOST={REDIS_CONTAINER}",
        "-e", "REDIS_PORT=6379",

        # Debug
        "-e", "DB_WAIT_DEBUG=1",

        # Superuser credentials
        "-e", "SUPERUSER_NAME=admin",
        "-e", "SUPERUSER_PASSWORD=admin",
        "-e", "SUPERUSER_EMAIL=admin@example.com",

        full_image,
    ])

    if create_superuser:
        print("Superuser should be created automatically from env vars.")

def main(sha=None, issue_id=None, port=DEFAULT_PORT, skip_superuser=False):
    """Main deployment function for NetBox."""
    pretty_section(f"Deploying Netbox (isuue number {issue_id}) at SHA: {sha}")

    # Verify prerequisites
    for tool in ("git", "docker", "docker-compose"):
        check_prereq(tool)

    # Clean up existing deployment
    clean(heading=False)

    # Look up Docker version from CSV
    row = _load_bug_row(CSV_PATH, sha)
    variant, docker_version = resolve_docker_version_for_sha(row, sha)

    # Deploy three-container stack
    ensure_network()
    ensure_postgres()
    ensure_redis()
    deploy(docker_version, DEFAULT_PORT, create_superuser=True)

    # Wait for services to initialize
    print("service may take 60 to 90 seconds to start.")
    time.sleep(100)

    # Run post-deployment hooks
    args = {
        "issue_id": issue_id,
        "project": "nocodb",
        "extra_flag": True,
        "port": 8080
    }
    run_issue_hook(issue_id, args, issues_module=nocodb_issues)

    pretty_section("NetBox is ready", color="green")

    print(f"\nNetBox {docker_version} should be live at http://localhost:{port}")
    print("Use these credentials:")
    print("  Username: admin")
    print("  Password: admin")
    print(" Api Token: 0123456789abcdef0123456789abcdef01234567")

def stop(heading=True):
    """Stop all NetBox containers without removing them."""
    if heading:
        pretty_section("Stopping NetBox containers …")
    for name in (NETBOX_CONTAINER, PG_CONTAINER, REDIS_CONTAINER):
        try:
            print(f"  Stopping {name} …")
            run(["docker", "stop", name])
        except subprocess.CalledProcessError as e:
            print(f"  Could not stop {name}: {e}")
    print("Done stopping NetBox containers.")

def clean(heading=True):
    """Complete cleanup of NetBox deployment."""
    if heading:
        pretty_section("Cleaning NetBox containers, volumes, and network …")

    # Stop containers
    stop(False)

    # Remove containers
    for name in (NETBOX_CONTAINER, PG_CONTAINER, REDIS_CONTAINER):
        print(f"  Removing container {name} …")
        subprocess.run(["docker", "rm", "-f", name], check=False)

    # Remove volumes
    for vol in ("netbox_postgres", "netbox_redis"):
        print(f"  Removing volume {vol} …")
        subprocess.run(["docker", "volume", "rm", vol], check=False)

    # Remove network
    print(f"  Removing network {NETWORK_NAME} …")
    subprocess.run(["docker", "network", "rm", NETWORK_NAME], check=False)

    print("Cleanup complete.")
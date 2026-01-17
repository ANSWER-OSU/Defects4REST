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
Deploy enviroCar-server using Dockerfile + docker-compose for Defects4REST.

Steps:
 1. Use get_defects4rest_root() to locate the Defects4REST root.
 2. Clone enviroCar-server (if not already present) into enviroCar-server/.
 3. Checkout the requested SHA.
 4. Patch pom.xml to fix dead / legacy repositories.
 5. Patch mongo.properties & mail.properties
 6. Write Dockerfile and docker-compose.yml into envirocar_docker/ (if missing).
 7. Run `docker compose up -d --build` from envirocar_docker/.
 8. Expose enviroCar at http://localhost:8080 (Jetty runner).
"""

import subprocess
import shutil
import os
import sys
import argparse

from defects4rest.src.utils.resources import ensure_temp_project_dir, get_defects4rest_root, check_prereq 
from defects4rest.src.utils.shell import pretty_step, pretty_section

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

REPO_URL = "https://github.com/enviroCar/enviroCar-server.git"

# Defects4REST root
DEFECTS4REST_ROOT = get_defects4rest_root()  # default levels_up=2

PROJECT_NAME = "envirocar-server"

PROJECT_DIR = str(ensure_temp_project_dir(PROJECT_NAME))
DOCKER_ROOT = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}_docker")
REPO_DIR = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}-src")


# Location of the cloned enviroCar repo inside DOCKER_ROOT
REPO_DIR = os.path.join(DOCKER_ROOT, "enviroCar-server")

POM_PATH = os.path.join(REPO_DIR, "pom.xml")

# Names used in docker-compose.yml
MONGO_SERVICE_NAME = "mongodb"
SERVER_SERVICE_NAME = "envirocar-server"

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def run(cmd, cwd=None, env=None, capture_output=False):
    """Wrapper around subprocess.run with logging and error propagation."""
    pretty_step(f"> {' '.join(cmd)}")
    subprocess.run(
        cmd,
        cwd=cwd,
        env=env or os.environ,
        check=True,
        stdout=(subprocess.PIPE if capture_output else None),
        stderr=(subprocess.STDOUT if capture_output else None),
    )


def run_capture(cmd, cwd=None, env=None):
    """Run a command and return stdout as text."""
    pretty_step(f"> {' '.join(cmd)}")
    cp = subprocess.run(
        cmd,
        cwd=cwd,
        env=env or os.environ,
        check=True,
        capture_output=True,
        text=True,
    )
    return cp.stdout


def current_sha(project_dir: str) -> str:
    """Return the current git HEAD SHA of the given repo directory."""
    out = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=project_dir, text=True
    ).strip()
    return out


def patch_pom_repos(pom_path: str):
    """
    Patch old repositories in pom.xml so Maven can resolve legacy artifacts.

    Patches:
      1) Refractions GeoTools repo:
           http://lists.refractions.net/m2
         -> https://repo.osgeo.org/repository/release/

      2) 52north n52-releases:
           http://52north.org/maven/repo/releases
         -> https://52north.org/maven/repo/releases
    """
    if not os.path.isfile(pom_path):
        pretty_step(f"[patch_pom_repos] pom.xml not found at {pom_path}, skipping patch.")
        return

    with open(pom_path, "r", encoding="utf-8") as f:
        pom = f.read()

    replacements = [
        (
            "http://lists.refractions.net/m2",
            "https://repo.osgeo.org/repository/release/",
            "Refractions -> OSGeo Nexus",
        ),
        (
            "http://52north.org/maven/repo/releases",
            "https://52north.org/maven/repo/releases",
            "52north http -> https",
        ),
    ]

    modified = False
    for old_url, new_url, label in replacements:
        if old_url in pom:
            pom = pom.replace(old_url, new_url)
            modified = True
            pretty_step(f"[patch_pom_repos] Patched {label}: {old_url} -> {new_url}")
        else:
            pretty_step(f"[patch_pom_repos] {label}: {old_url} not found, no change.")

    if modified:
        with open(pom_path, "w", encoding="utf-8") as f:
            f.write(pom)
    else:
        pretty_step(f"[patch_pom_repos] No repository URLs patched.")

def patch_mongo_properties(repo_dir: str):
    """
    Write mongo.properties to connect to the mongodb container.
    """
    mongo_props_path = os.path.join(
        repo_dir, "mongo", "src", "main", "resources", "mongo.properties"
    )
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(mongo_props_path), exist_ok=True)
    
    content = """host=mongodb
port=27017
database=envirocar
"""
    
    with open(mongo_props_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    pretty_step(f"[patch_mongo_properties] Written mongo.properties to {mongo_props_path}")

def patch_mail_properties(repo_dir: str):
    
    """
    Create a dummy mail.properties file to satisfy the application requirements.
    """
    mail_props_path = os.path.join(repo_dir, "mail.properties")
    
    # Create a minimal mail.properties with dummy values
    content = """mail.smtp.host=localhost
mail.smtp.port=25
mail.from=noreply@envirocar.org
mail.smtp.auth=false
mail.smtp.username=dummy
mail.smtp.password=dummy
mail.from.address=noreply@envirocar.org
mail.from.name=enviroCar
"""
    
    with open(mail_props_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    pretty_step(f"[patch_mail_properties] Written mail.properties to {mail_props_path}")


def write_dockerfile(docker_root: str):
    """
    Write Dockerfile into docker_root if it doesn't exist.
    Uses your maven:3.6.3-jdk-8 + Jetty Runner approach.
    """
    dockerfile_path = os.path.join(docker_root, "Dockerfile")
    if os.path.exists(dockerfile_path):
        pretty_step(f"[write_dockerfile] Dockerfile already exists at {dockerfile_path}, overwriting...")

    content = r"""# ============================================
# Dockerfile for enviroCar-server
# ============================================
FROM maven:3.6.3-jdk-8

# Fix Debian Buster repository URLs (Buster is EOL)
RUN sed -i 's|http://deb.debian.org|http://archive.debian.org|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org|http://archive.debian.org|g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

# Install required tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the cloned repository (enviroCar-server/)
COPY ./enviroCar-server /app

# Create MongoDB configuration
RUN mkdir -p /app/mongo/src/main/resources

# Build the application (skip tests to speed up)
RUN mvn clean package -DskipTests 2>&1 | tee /app/build.log

# List build artifacts
RUN echo "=== Build artifacts ===" && \
    find /app -name "*.war" -type f && \
    find /app -name "*.jar" -type f

# Download Jetty Runner for running the WAR file
RUN curl -o /app/jetty-runner.jar https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-runner/9.4.48.v20220622/jetty-runner-9.4.48.v20220622.jar

# Create start script that uses the built WAR
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Waiting for MongoDB to be ready..."\n\
while ! nc.traditional -z mongodb 27017; do\n\
  sleep 1\n\
done\n\
echo "MongoDB is ready!"\n\
echo ""\n\
echo "=== Starting enviroCar server ==="\n\
\n\
WAR_FILE=$(find /app/webapp/target -name "*.war" | head -1)\n\
\n\
if [ -z "$WAR_FILE" ]; then\n\
  echo "ERROR: No WAR file found in /app/webapp/target"\n\
  echo "Attempting to rebuild..."\n\
  cd /app\n\
  mvn clean package -pl webapp -am -DskipTests\n\
  WAR_FILE=$(find /app/webapp/target -name "*.war" | head -1)\n\
fi\n\
\n\
if [ -z "$WAR_FILE" ]; then\n\
  echo "ERROR: Still no WAR file found after rebuild"\n\
  exit 1\n\
fi\n\
\n\
echo "Found WAR file: $WAR_FILE"\n\
echo "Starting Jetty Runner on port 8080..."\n\
echo ""\n\
\n\
java -jar /app/jetty-runner.jar --port 8080 "$WAR_FILE"' > /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
"""
    with open(dockerfile_path, "w", encoding="utf-8") as f:
        f.write(content)
    pretty_step(f"[write_dockerfile] Dockerfile written to {dockerfile_path}")


def write_docker_compose(docker_root: str):
    """
    Write docker-compose.yml into docker_root if it doesn't exist.
    Uses your compose snippet, with platform=linux/amd64 for M1.
    """
    compose_path = os.path.join(docker_root, "docker-compose.yml")
    if os.path.exists(compose_path):
        pretty_step(f"[write_docker_compose] docker-compose.yml already exists at {compose_path}, overwriting...")

    content = r"""version: "3.8"

services:
  # MongoDB service
  mongodb:
    image: mongo:3.6
    platform: linux/amd64
    container_name: envirocar-mongodb
    command: mongod --bind_ip_all
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_DATABASE=envirocar
    volumes:
      - mongodb_data:/data/db
      - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    networks:
      - envirocar-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongo localhost:27017/envirocar --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  # enviroCar Server
  envirocar-server:
    build:
      context: .
      dockerfile: Dockerfile
    platform: linux/amd64
    container_name: envirocar-server
    ports:
      - "8080:8080"
    depends_on:
      mongodb:
        condition: service_healthy
    environment:
      - MONGO_HOST=mongodb
      - MONGO_PORT=27017
      - MONGO_DATABASE=envirocar
    volumes:
      - maven_cache:/root/.m2
    networks:
      - envirocar-network
    restart: unless-stopped
    stdin_open: true
    tty: true

volumes:
  mongodb_data:
    driver: local
  maven_cache:
    driver: local

networks:
  envirocar-network:
    driver: bridge
"""
    with open(compose_path, "w", encoding="utf-8") as f:
        f.write(content)
    pretty_step(f"[write_docker_compose] docker-compose.yml written to {compose_path}")


def write_init_mongo(docker_root: str):
    """
    Write a tiny init-mongo.js if it doesn't exist.
    This can create DB or collections as needed; here it's minimal.
    """
    init_path = os.path.join(docker_root, "init-mongo.js")
    if os.path.exists(init_path):
        pretty_step(f"[write_init_mongo] init-mongo.js already exists at {init_path}, leaving it.")
        return

    content = """// init-mongo.js
// Basic initialization for envirocar DB.
// You can add indexes or users here if needed.

db = db.getSiblingDB("envirocar");
print("Initialized envirocar database.");
"""
    with open(init_path, "w", encoding="utf-8") as f:
        f.write(content)
    pretty_step(f"[write_init_mongo] init-mongo.js written to {init_path}")

def find_compose_cmd():
    """
    Prefer 'docker compose' (modern) and fall back to 'docker-compose' if needed.
    """
    # Try "docker compose"
    if shutil.which("docker") is not None:
        try:
            subprocess.run(
                ["docker", "compose", "version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return ["docker", "compose"]
        except Exception:
            pass

    # Fallback to docker-compose
    if shutil.which("docker-compose") is not None:
        return ["docker-compose"]

    print("Error: neither 'docker compose' nor 'docker-compose' is available.")
    sys.exit(1)


# ---------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------


def main(sha: str = "latest",issue_id=None):
    """
    Entry point used by defects4rest.checkout.

    :param sha: Git commit SHA to checkout (or "latest" to use current branch head).
    """
    # 1) Check prerequisites
    for tool in ("git", "docker"):
        check_prereq(tool)
    compose_cmd = find_compose_cmd()

    # 2) Ensure DOCKER_ROOT exists
    os.makedirs(DOCKER_ROOT, exist_ok=True)

    # 3) Fresh clone every time to avoid local-change conflicts
    if os.path.isdir(REPO_DIR):
        pretty_step(f"Removing existing repo at {REPO_DIR} for a clean checkout...")
        shutil.rmtree(REPO_DIR)

    pretty_section(f"Cloning repo into {REPO_DIR}")
    run(["git", "clone", REPO_URL, REPO_DIR])

    # 4) Checkout requested commit
    os.chdir(REPO_DIR)
    run(["git", "fetch", "--all"])

    if sha and sha.lower() != "latest":
        run(["git", "checkout", sha])
        pretty_step(f"Checked out SHA (requested): {sha}")
    else:
        pretty_step("Using currently checked-out branch (update it manually if needed).")

    # 5) Patch mongo.properties and mail.properties
    patch_mongo_properties(REPO_DIR)
    patch_mail_properties(REPO_DIR)

    actual = current_sha(REPO_DIR)
    pretty_section(f"Building commit: {actual}")

    # 6) Patch pom.xml so legacy repos work
    patch_pom_repos(POM_PATH)

    # 7) Write Dockerfile, docker-compose.yml, and init-mongo.js into DOCKER_ROOT
    write_dockerfile(DOCKER_ROOT)
    write_docker_compose(DOCKER_ROOT)
    write_init_mongo(DOCKER_ROOT)

    # 8) Run docker compose up -d --build
    pretty_step("\n=== Running docker compose up -d --build ===")
    run(compose_cmd + ["up", "-d", "--build"], cwd=DOCKER_ROOT)

    pretty_section("\nenviroCar-server (Jetty) should be running at: http://localhost:8080")
    pretty_step("   Mongo container: envirocar-mongodb")
    pretty_step("   Server container: envirocar-server")
    pretty_step(f"   Git commit: {actual}")


def stop():
    """Stop and remove containers via docker compose down."""
    compose_cmd = find_compose_cmd()
    pretty_section("Stopping enviroCar-server containers …")
    if not os.path.isdir(DOCKER_ROOT):
        pretty_step(f"No DOCKER_ROOT at {DOCKER_ROOT}, nothing to stop.")
        return
    run(compose_cmd + ["down", "-v"], cwd=DOCKER_ROOT)
    pretty_step("docker compose down completed.")


def clean():
    """Alias for stop (compose down will remove containers and networks)."""
    stop()
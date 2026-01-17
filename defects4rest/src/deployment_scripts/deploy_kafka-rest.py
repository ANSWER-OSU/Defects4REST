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
Kafka REST Proxy Deployment Script
This script deploys Kafka REST Proxy along with its required dependencies (Kafka, Zookeeper, Schema Registry) using Docker Compose.
A CSV file maps bug SHAs to Docker image versions, allowing deployment of specific buggy or patched versions for testing.
"""
import subprocess
import shutil
import os
import sys
import re
import csv
import time
import requests
import yaml
from typing import List
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.api_dep_setup import kafka_rest as kafka_rest_issues
from defects4rest.src.utils.issue_metadata import run_issue_hook

REPO_URL = "https://github.com/confluentinc/kafka-rest.git"

# Some bugs require patched versions from forks
PATCHED_SHAS = {
    "4391b34bbc4caadc5aede4c4493bb918b74031a2": {
        "repo": "https://github.com/luinix/kafka-rest.git",
        "ref": "4391b34bbc4caadc5aede4c4493bb918b74031a2",
    }
}
PROJECT_NAME = 'kafka-rest'
CSV_PATH = data_csv(PROJECT_NAME)
PROJECT_DIR = str(ensure_temp_project_dir(PROJECT_NAME))
DOCKER_ROOT = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}_docker")
REPO_DIR = os.path.join(PROJECT_DIR, f"{PROJECT_NAME}-src")

# Container names
KAFKA_REST_CONTAINER = "kafka-rest"
KAFKA_CONTAINER = "kafka-broker"
ZOOKEEPER_CONTAINER = "kafka-zookeeper"
SCHEMA_REGISTRY_CONTAINER = "schema-registry"

# Regex patterns for SHA parsing
_HEX_SHA_RE = re.compile(r"\b[0-9a-fA-F]{7,40}\b")
_SPLIT_SHA_RE = re.compile(r"[,\|\s;]+")

def check_prereq(cmd: str):
    """Ensure required command is available."""
    if shutil.which(cmd) is None:
        print(f"Error: '{cmd}' is not installed or not in your PATH.")
        sys.exit(1)

def run(cmd: List[str], cwd: str = None, env=None):
    """Execute command with logging and error checking."""
    print(f"> {' '.join(cmd)}")
    subprocess.run(
        cmd,
        cwd=cwd,
        env=env or os.environ,
        check=True,
    )

def current_sha(project_dir: str) -> str:
    """Return current git HEAD SHA."""
    out = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=project_dir, text=True
    ).strip()
    return out

def _tokenize_shas(value: str) -> list[str]:
    """Split string containing multiple SHAs separated by delimiters."""
    if not value:
        return []
    return [tok.strip() for tok in _SPLIT_SHA_RE.split(value) if tok.strip()]

def _extract_shas_from_text(text: str) -> list[str]:
    """Extract SHA-like tokens from arbitrary text."""
    if not text:
        return []
    return list({m.group(0) for m in _HEX_SHA_RE.finditer(text)})

def resolve_docker_tag_from_csv(sha: str, csv_path: str) -> str:
    """Determine Docker image version based on git SHA."""
    if not os.path.isfile(csv_path):
        print(csv_path)
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Validate required columns
        required = {
            "buggy_sha", "patch_sha", "patched_files",
            "buggy_docker_version", "patched_docker_version"
        }
        missing_cols = required - set(reader.fieldnames or [])
        if missing_cols:
            raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing_cols))}")

        # Search for matching SHA
        for row in reader:
            buggy_sha = (row.get("buggy_sha") or "").strip()
            patch_sha_field = (row.get("patch_sha") or "").strip()
            patched_files_field = (row.get("patched_files") or "").strip()

            # Check patch SHA
            for candidate in _tokenize_shas(patch_sha_field):
                if sha == candidate:
                    tag = (row.get("patched_docker_version") or "").strip()
                    if not tag:
                        raise ValueError(
                            f"Matched patch_sha in CSV, but patched_docker_version is empty for sha={sha}"
                        )
                    return tag

            # Check buggy SHA
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

def find_compose_cmd() -> List[str]:
    """Determine which Docker Compose command is available."""
    # Try Docker Compose plugin
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

    # Try legacy standalone
    if shutil.which("docker-compose") is not None:
        return ["docker-compose"]

    print("Error: neither 'docker compose' nor 'docker-compose' is available.")
    sys.exit(1)

def write_dockerfile(docker_root: str):
    """Generate multi-stage Dockerfile for building Kafka REST from source."""
    dockerfile_path = os.path.join(docker_root, "Dockerfile")

    content = r"""
# ============================================
# Dockerfile for confluentinc/kafka-rest
# ============================================
############################################
# STAGE 1 — resolve Kafka REST dependencies
############################################
FROM maven:3.9.6-eclipse-temurin-11 AS deps

WORKDIR /deps

# Write Maven settings.xml (Confluent repo, HTTPS)
RUN mkdir -p /root/.m2 && printf '%s\n' \
'<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"' \
'          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
'          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0' \
'                              https://maven.apache.org/xsd/settings-1.0.0.xsd">' \
'  <profiles>' \
'    <profile>' \
'      <id>confluent</id>' \
'      <repositories>' \
'        <repository>' \
'          <id>confluent</id>' \
'          <url>https://packages.confluent.io/maven/</url>' \
'          <releases><enabled>true</enabled></releases>' \
'          <snapshots><enabled>true</enabled></snapshots>' \
'        </repository>' \
'      </repositories>' \
'    </profile>' \
'  </profiles>' \
'  <activeProfiles>' \
'    <activeProfile>confluent</activeProfile>' \
'  </activeProfiles>' \
'</settings>' \
> /root/.m2/settings.xml

# Temporary POM to pull kafka-rest (NO upstream changes)
RUN printf '%s\n' \
'<project xmlns="http://maven.apache.org/POM/4.0.0">' \
'  <modelVersion>4.0.0</modelVersion>' \
'  <groupId>tmp</groupId>' \
'  <artifactId>kafka-rest-runner</artifactId>' \
'  <version>1.0</version>' \
'  <dependencies>' \
'    <dependency>' \
'      <groupId>io.confluent</groupId>' \
'      <artifactId>kafka-rest</artifactId>' \
'      <version>2.1.0-alpha1</version>' \
'    </dependency>' \
'  </dependencies>' \
'</project>' \
> pom.xml

# Download kafka-rest and all transitive dependencies
RUN mvn -q -s /root/.m2/settings.xml \
    dependency:copy-dependencies -DoutputDirectory=lib


############################################
# STAGE 2 — runtime container
############################################
FROM eclipse-temurin:8-jre

ENV KAFKA_REST_HOME=/opt/kafka-rest
WORKDIR ${KAFKA_REST_HOME}

# Copy resolved dependency jars
COPY --from=deps /deps/lib ./lib

# Config
RUN mkdir -p /etc/kafka-rest
COPY kafka-rest.properties /etc/kafka-rest/kafka-rest.properties

EXPOSE 8082

# Start Kafka REST
CMD ["java","-cp","lib/*","io.confluent.kafkarest.KafkaRestMain","/etc/kafka-rest/kafka-rest.properties"]
"""
    with open(dockerfile_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[write_dockerfile] Dockerfile written to {dockerfile_path}")

def write_kafka_rest_properties(docker_root: str):
    """Generate kafka-rest.properties configuration file."""
    props_path = os.path.join(docker_root, "kafka-rest.properties")

    content = """# Basic kafka-rest configuration for local Docker stack

# Where kafka-rest should listen
listeners=http://0.0.0.0:8082

bootstrap.servers=PLAINTEXT://kafka:9092
schema.registry.url=http://schema-registry:8081
zookeeper.connect=kafka-zookeeper:2181


"""
    with open(props_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[write_kafka_rest_properties] kafka-rest.properties written to {props_path}")

def kafka_rest_service(docker_tag: str | None):
    """Generate Docker Compose service definition for Kafka REST."""
    service = {
        "platform": "linux/amd64",
        "container_name": "kafka-rest",
        "depends_on": ["kafka", "schema-registry"],
        "ports": ["8082:8082"],
        "environment": {
            "KAFKA_REST_HOST_NAME": "kafka-rest",
            "KAFKA_REST_BOOTSTRAP_SERVERS": "kafka:9092",
            "KAFKA_REST_LISTENERS": "http://0.0.0.0:8082",
            "KAFKA_REST_SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
            "KAFKA_REST_ZOOKEEPER_CONNECT": "zookeeper:2181",
        },
        "networks": ["kafka-net"],
        "restart": "unless-stopped",
    }

    if docker_tag:
        service["image"] = f"confluentinc/cp-kafka-rest:{docker_tag}"
    else:
        service["build"] = {
            "context": ".",
            "dockerfile": "Dockerfile",
        }
        service["image"] = "kafka-rest-local"

    return service

def write_docker_compose(docker_root: str, docker_tag: str | None):
    """Generate docker-compose.yml for complete Kafka stack."""
    compose_path = os.path.join(docker_root, "docker-compose.yml")

    compose = {
        "version": "3.8",
        "services": {
            "kafka-rest": kafka_rest_service(docker_tag),

            "zookeeper": {
                "image": "confluentinc/cp-zookeeper:7.6.0",
                "platform": "linux/amd64",
                "container_name": "kafka-zookeeper",
                "environment": {
                    "ZOOKEEPER_CLIENT_PORT": "2181",
                    "ZOOKEEPER_TICK_TIME": "2000",
                },
                "ports": ["2181:2181"],
                "networks": ["kafka-net"],
            },


            "kafka": {
                "image": "confluentinc/cp-kafka:6.0.7",
                "platform": "linux/amd64",
                "container_name": "kafka-broker",
                "depends_on": ["zookeeper"],
                "ports": ["9092:9092"],
                "environment": {
                    "KAFKA_BROKER_ID": "1",
                    "KAFKA_ZOOKEEPER_CONNECT": "zookeeper:2181",
                    "KAFKA_REST_ZOOKEEPER_CONNECT": "zookeeper:2181",
                    "KAFKA_LISTENERS": (
                        "PLAINTEXT://0.0.0.0:9092,"
                        "PLAINTEXT_HOST://0.0.0.0:29092"
                    ),
                    "KAFKA_ADVERTISED_LISTENERS": (
                        "PLAINTEXT://kafka:9092,"
                        "PLAINTEXT_HOST://localhost:29092"
                    ),
                    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": (
                        "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT"
                    ),
                    "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": "1",
                    "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR": "1",
                    "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR": "1",
                },
                "networks": ["kafka-net"],
            },

            "schema-registry": {
                "image": "confluentinc/cp-schema-registry:7.6.0",
                "platform": "linux/amd64",
                "container_name": "schema-registry",
                "depends_on": ["kafka"],
                "ports": ["8081:8081"],
                "environment": {
                    "SCHEMA_REGISTRY_HOST_NAME": "schema-registry",
                    "SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS": (
                        "PLAINTEXT://kafka:9092"
                    ),
                },
                "networks": ["kafka-net"],
            },
        },

        "networks": {
            "kafka-net": {"driver": "bridge"}
        },
    }

    with open(compose_path, "w") as f:
        yaml.safe_dump(compose, f, sort_keys=False)

def wait_for_server(url, timeout=60):
    """Poll URL until it responds with HTTP 200 or timeout."""
    pretty_step("Waiting for server to start...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            time.sleep(1)
    pretty_step("Timeout waiting for server.")
    return False

def build_kafka(build_mode, docker_tag: str | None, compose_cmd: None, issue_id, sha):
    """Build and deploy Kafka REST in manual or image mode."""
    if build_mode == "manual":
        pretty_section(f"Building kafka-rest (issue number {issue_id}) manually...")

        # Remove existing repo
        if os.path.isdir(REPO_DIR):
            pretty_step(f"[main] Removing existing repo at {REPO_DIR} for a clean checkout...")
            shutil.rmtree(REPO_DIR)

        # Check for patched fork
        patched = PATCHED_SHAS.get(sha)

        if patched:
            repo_url = patched["repo"]
            ref = patched["ref"]
            print(f"[INFO] Using patched fork: {repo_url} ({ref})")
        else:
            repo_url = REPO_URL
            ref = sha

        # Clone and checkout
        pretty_step(f"[main] Cloning repo into {REPO_DIR}")
        run(["git", "clone", repo_url, REPO_DIR])

        pretty_step("[main] Fetching all refs...")
        run(["git", "fetch", "--all", "--tags"], cwd=REPO_DIR)

        if ref and ref.lower() != "latest":
            pretty_step(f"[main] Checking out {ref}")
            run(["git", "checkout", ref], cwd=REPO_DIR)
        else:
            pretty_step("[main] Using default branch HEAD")

        actual = current_sha(REPO_DIR)
        pretty_step(f"[main] Building commit: {actual}")

        # Generate files and build
        write_kafka_rest_properties(DOCKER_ROOT)
        write_dockerfile(DOCKER_ROOT)
        write_docker_compose(DOCKER_ROOT, None)

        pretty_step("\n=== Running docker compose up -d --build ===")
        run(compose_cmd + ["build", "--no-cache"], cwd=DOCKER_ROOT)
        run(compose_cmd + ["up", "-d"], cwd=DOCKER_ROOT)
    else:
        # Image mode
        pretty_section(f"Deploying kafka-rest (issue number {issue_id}) at version: {docker_tag}")
        os.makedirs(DOCKER_ROOT, exist_ok=True)

        write_kafka_rest_properties(DOCKER_ROOT)
        write_docker_compose(DOCKER_ROOT, docker_tag)

        pretty_step("Running docker compose up -d --build")
        run(compose_cmd + ["up", "-d", "--build"], cwd=DOCKER_ROOT)

def main(sha: str = "latest", issue_id=None):
    """Main deployment function for Kafka REST."""
    pretty_section(f"Deploying Kafa-rest (issue number {issue_id}) at SHA: {sha}")
    for tool in ("git", "docker"):
        check_prereq(tool)
    compose_cmd = find_compose_cmd()

    # Handle SHA lookup
    if sha == "latest":
        docker_tag = "latest"
    else:
        docker_tag = resolve_docker_tag_from_csv(sha, CSV_PATH)
        if docker_tag == "0":
            build_kafka("manual", None, compose_cmd, issue_id, sha)
        else:
            build_kafka("image", docker_tag, compose_cmd, issue_id, sha)

    # Wait for server
    if not wait_for_server("http://localhost:8082", timeout=120):
        sys.exit(1)

    pretty_section("kafka-rest should now be running",color="green")
    pretty_step("   REST base URL: http://localhost:8082")
    pretty_step("   Kafka broker:  localhost:9092")
    pretty_step("   Schema Registry: http://localhost:8081")

    # Run post-deployment hooks
    args = {
        "issue_id": issue_id,
        "project": "kafka_rest",
        "extra_flag": True,
    }

    run_issue_hook(issue_id, args, issues_module=kafka_rest_issues)

def stop():
    """Stop Kafka REST stack."""
    pretty_section("Stopping kafka-rest containers …")
    compose_cmd = find_compose_cmd()
    if not os.path.isdir(DOCKER_ROOT):
        pretty_step(f"[stop] No DOCKER_ROOT at {DOCKER_ROOT}, nothing to stop.")
        return
    run(compose_cmd + ["down"], cwd=DOCKER_ROOT)
    pretty_step("[stop] docker compose down completed.")

def clean():
    """Complete cleanup of Kafka REST deployment."""
    stop()
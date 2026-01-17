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
AWX deployment automation for Defects4REST using Docker Compose.

Automates AWX installation by resolving versions from CSV, generating config files,
cleaning previous installations, starting containers, and verifying readiness at
http://localhost:8080.
"""

import csv
import re
import secrets
import base64
import time
import requests

from typing import List
from defects4rest.src.utils.resources import *
from defects4rest.src.utils.shell import pretty_section, pretty_step
from defects4rest.src.utils.git import *

CSV_PATH = "defects4rest/data/defect_data/awx_info.csv"

# Regex patterns for SHA parsing
_HEX_SHA_RE = re.compile(r"\b[0-9a-fA-F]{7,40}\b")
_SPLIT_SHA_RE = re.compile(r"[,\|\s;]+")

AWX_DIR = os.path.expanduser("~/.awx/awxcompose")
PG_DATA_DIR = os.path.expanduser("~/.awx/pgdocker/10/data")
AWX_URL = "http://localhost:80"
AWX_USER = "admin"
AWX_PASSWORD = "password"

def run(cmd: List[str], cwd: str = None, env=None, check=True):
    print(f"> {' '.join(cmd)}")
    subprocess.run(
        cmd,
        cwd=cwd,
        env=env or os.environ,
        check=check,
    )

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
        pretty_step(csv_path)
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

def cleanup_existing():
    """Clean up any existing AWX installation."""
    pretty_step("Cleaning up existing installation...")

    if os.path.exists(AWX_DIR):
        os.chdir(AWX_DIR)
        run(["docker", "compose", "down", "-v"], check=False)

        # Clean postgres data
        if os.path.exists(PG_DATA_DIR):
            pretty_step("  Removing postgres data directory ...")
            shutil.rmtree(PG_DATA_DIR, ignore_errors=True)
        else:
            pretty_step("  No existing postgres data found. Skipping cleanup.")
        pretty_step("  Cleanup complete")
    else:
        pretty_step("  No existing installation found. Skipping cleanup.")

def create_directory_structure():
    """Create the required directory structure."""
    pretty_step("Creating directory structure...")
    os.makedirs(AWX_DIR, exist_ok=True)
    os.makedirs(PG_DATA_DIR, exist_ok=True)
    redis_socket_dir = os.path.join(AWX_DIR, "redis_socket")
    os.makedirs(redis_socket_dir, exist_ok=True)
    os.chmod(redis_socket_dir, 0o777)
    pretty_step(f"  Created: {AWX_DIR}")
    pretty_step(f"  Created: {PG_DATA_DIR}")

def generate_secret_key():
    """Generate a random secret key."""
    return base64.b64encode(secrets.token_bytes(32)).decode()

def resolve_awx_image(docker_tag: str) -> str:
    dh_url = f"https://registry.hub.docker.com/v2/repositories/ansible/awx/tags/{docker_tag}"

    try:
        resp = requests.get(dh_url, timeout=5)
        if resp.status_code == 200:
            pretty_step(f"  Found on DockerHub: ansible/awx:{docker_tag}")
            return f"ansible/awx:{docker_tag}"
        else:
            pretty_step(f"  Not found on DockerHub (status {resp.status_code}), using quay.io")
    except requests.RequestException as e:
        pretty_step(f"  DockerHub lookup failed ({e}), defaulting to quay.io")

    return f"quay.io/ansible/awx:{docker_tag}"

def create_config_files(docker_tag):
    """Create all required configuration files."""
    pretty_step(f"Creating configuration files for AWX {docker_tag}...")

    # SECRET_KEY
    secret_key = generate_secret_key()
    with open(os.path.join(AWX_DIR, "SECRET_KEY"), "w") as f:
        f.write(secret_key)
    pretty_step(f"  Created: SECRET_KEY")

    # credentials.py
    credentials_py = '''DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "awx",
        'USER': "awx",
        'PASSWORD': "awxpass",
        'HOST': "postgres",
        'PORT': "5432",
    }
}

BROADCAST_WEBSOCKET_SECRET = "YnJvYWRjYXN0d2Vic29ja2V0c2VjcmV0"
'''
    with open(os.path.join(AWX_DIR, "credentials.py"), "w") as f:
        f.write(credentials_py)
    pretty_step(f"  Created: credentials.py")

    # environment.sh
    environment_sh = '''DATABASE_USER="awx"
DATABASE_NAME="awx"
DATABASE_HOST="postgres"
DATABASE_PORT="5432"
DATABASE_PASSWORD="awxpass"
AWX_ADMIN_USER="admin"
AWX_ADMIN_PASSWORD="password"
'''
    with open(os.path.join(AWX_DIR, "environment.sh"), "w") as f:
        f.write(environment_sh)
    pretty_step(f"  Created: environment.sh")

    # redis.conf
    redis_conf = '''unixsocket /var/run/redis/redis.sock
unixsocketperm 660
port 0
bind 127.0.0.1
'''
    with open(os.path.join(AWX_DIR, "redis.conf"), "w") as f:
        f.write(redis_conf)
    pretty_step(f"  Created: redis.conf")

    # nginx.conf
    nginx_conf = '''worker_processes  1;
pid        /tmp/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    server_tokens off;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /dev/stdout main;

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    sendfile        on;

    upstream uwsgi {
        server 127.0.0.1:8050;
    }

    upstream daphne {
        server 127.0.0.1:8051;
    }

    server {
        listen 8052 default_server;
        server_name _;
        keepalive_timeout 65;

        add_header Strict-Transport-Security max-age=15768000;
        add_header X-Frame-Options "DENY";

        location /nginx_status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            deny all;
        }

        location /static/ {
            alias /var/lib/awx/public/static/;
        }

        location /favicon.ico { alias /var/lib/awx/public/static/favicon.ico; }

        location /websocket {
            proxy_pass http://daphne;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }

        location / {
            rewrite ^(.*)$http_host(.*[^/])$ $1$http_host$2/ permanent;
            uwsgi_read_timeout 120s;
            uwsgi_pass uwsgi;
            include /etc/nginx/uwsgi_params;
            proxy_set_header X-Forwarded-Port 443;
            uwsgi_param HTTP_X_FORWARDED_PORT 443;
        }
    }
}
'''
    with open(os.path.join(AWX_DIR, "nginx.conf"), "w") as f:
        f.write(nginx_conf)
    pretty_step(f"  Created: nginx.conf")

    # docker-compose.yml
    image_ref = resolve_awx_image(docker_tag)
    docker_compose = f'''version: '2'
services:

  web:
    image: {image_ref}
    platform: linux/amd64
    container_name: awx_web
    depends_on:
      - redis
      - postgres
    ports:
      - "80:8052"
    hostname: awxweb
    user: root
    restart: unless-stopped
    volumes:
      - supervisor-socket:/var/run/supervisor
      - rsyslog-socket:/var/run/awx-rsyslog/
      - rsyslog-config:/var/lib/awx/rsyslog/
      - "./SECRET_KEY:/etc/tower/SECRET_KEY"
      - "./environment.sh:/etc/tower/conf.d/environment.sh"
      - "./credentials.py:/etc/tower/conf.d/credentials.py"
      - "./nginx.conf:/etc/nginx/nginx.conf:ro"
      - "./redis_socket:/var/run/redis/:rw"

  task:
    image: {image_ref}
    platform: linux/amd64
    container_name: awx_task
    depends_on:
      - redis
      - web
      - postgres
    command: /usr/bin/launch_awx_task.sh
    hostname: awx
    user: root
    restart: unless-stopped
    volumes:
      - supervisor-socket:/var/run/supervisor
      - rsyslog-socket:/var/run/awx-rsyslog/
      - rsyslog-config:/var/lib/awx/rsyslog/
      - "./SECRET_KEY:/etc/tower/SECRET_KEY"
      - "./environment.sh:/etc/tower/conf.d/environment.sh"
      - "./credentials.py:/etc/tower/conf.d/credentials.py"
      - "./redis_socket:/var/run/redis/:rw"
    environment:
      SUPERVISOR_WEB_CONFIG_PATH: '/etc/supervisord.conf'

  redis:
    image: redis
    platform: linux/amd64
    container_name: awx_redis
    restart: unless-stopped
    command: ["/usr/local/etc/redis/redis.conf"]
    volumes:
      - "./redis.conf:/usr/local/etc/redis/redis.conf:ro"
      - "./redis_socket:/var/run/redis/:rw"

  postgres:
    image: postgres:12
    platform: linux/amd64
    container_name: awx_postgres
    restart: unless-stopped
    volumes:
      - "{PG_DATA_DIR}/:/var/lib/postgresql/data:Z"
    environment:
      POSTGRES_USER: awx
      POSTGRES_PASSWORD: awxpass
      POSTGRES_DB: awx

volumes:
  supervisor-socket:
  rsyslog-socket:
  rsyslog-config:
'''
    with open(os.path.join(AWX_DIR, "docker-compose.yml"), "w") as f:
        f.write(docker_compose)
    pretty_step(f"  Created: docker-compose.yml")

def wait_for_awx():
    """Wait for AWX to be ready."""
    pretty_step("Waiting for AWX to be ready (this may take 2-3 minutes)...")
    max_wait = 480  # 8 minutes
    start_time = time.time()

    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{AWX_URL}/api/v2/ping/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                pretty_step(f"  AWX {data.get('version', 'unknown')} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass

        elapsed = int(time.time() - start_time)
        pretty_step(f"  Waiting... ({elapsed}s elapsed)")
        time.sleep(10)

    pretty_step("  ERROR: AWX did not become ready in time", "red")
    return False

def main(sha=None,issue_id=None):

    # Handle SHA lookup
    if sha == "latest":
        docker_tag = "latest"
    else:
        docker_tag = resolve_docker_tag_from_csv(sha, CSV_PATH)


    pretty_section(f"Deploying awx (issue number {issue_id}) at version: {docker_tag}")

    create_directory_structure()
    create_config_files(docker_tag)
    cleanup_existing()

    """Start AWX containers."""
    pretty_step("Starting AWX containers...")
    os.chdir(AWX_DIR)
    run(["docker", "compose", "up", "-d"])

    if not wait_for_awx():
        pretty_step("\nFailed to start AWX. Check Docker logs:")
        pretty_step("  docker logs awx_web")
        pretty_step("  docker logs awx_task")
        sys.exit(1)

    pretty_section(f"AWX is running at http {AWX_URL}")

def stop():
    pretty_step("Stopping AWX containers ...")
    if os.path.exists(AWX_DIR):
        os.chdir(AWX_DIR)
        run(["docker", "compose", "stop"])
        pretty_step("  Containers stopped.")
    else:
        pretty_step("  No existing installation found..")

def clean():
    pretty_section("Cleaning up AWX containers and volumes ...")
    stop()
    """Perform full cleanup of AWX installation."""
    pretty_step("\nPerforming full cleanup...")
    if os.path.exists(AWX_DIR):
        os.chdir(AWX_DIR)
        run(["docker", "compose", "down", "-v"], check=False)

    pretty_step("  Cleanup complete")

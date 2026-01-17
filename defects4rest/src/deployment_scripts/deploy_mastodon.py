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

import subprocess
import shutil
import os
import sys
import requests
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv
from defects4rest.src.utils.issue_metadata import run_issue_hook, _load_bug_row ,resolve_docker_version_for_sha
from defects4rest.src.utils.git import sha_exists, get_default_branch
from defects4rest.src.api_dep_setup import mastodon as mastodon_isuue

# Default Mastodon repo
REPO_URL = "https://github.com/mastodon/mastodon.git"
PROJECT_DIR = os.path.abspath("defects4rest/data/mastodon/mastodon-docker")
ENV_SAMPLE = ".env.production.sample"
ENV_TARGET = ".env.production"

PATCHED_SHAS = {
    "e964cdcec3fb17351b4b5c93e96662da2b2d249b": "https://github.com/ClearlyClaire/mastodon.git",
    "adf76a6aa357720348f51aa8d2c06dcd6469a728": "https://github.com/ClearlyClaire/mastodon.git",

    # Add more patched SHAs here
}


def mastodon_oauth_flow(
        base_url="http://localhost:3000",
        admin_email="admin@localhost",
        admin_password="add11dc7cd2870781b7110e89657002b",
        client_name="Test Client",
        retry_with_existing_app=True
):
    """
    Complete Mastodon OAuth flow - returns credentials needed for API testing.

    Args:
        base_url: Mastodon instance URL
        admin_email: Admin email (use email, not username)
        admin_password: Admin password
        client_name: Name for the OAuth application
        retry_with_existing_app: If True, try to reuse existing app on failure

    Returns:
        dict: {
            'client_id': str,
            'client_secret': str,
            'access_token': str,
            'token_type': str,
            'scope': str
        }

    Raises:
        Exception: If OAuth flow fails
    """

    print("=" * 60)
    pretty_step("Starting Mastodon OAuth Flow")
    print("=" * 60)

    # Step 1: Register OAuth Application
    pretty_step("\n[1/2] Registering OAuth Application...")

    try:
        app_response = requests.post(
            f"{base_url}/api/v1/apps",
            data={
                "client_name": client_name,
                "redirect_uris": "urn:ietf:wg:oauth:2.0:oob",
                "scopes": "read write follow",
                "website": "https://example.com"
            }
        )

        if app_response.status_code != 200:
            raise Exception(
                f"Failed to register OAuth app. "
                f"Status: {app_response.status_code}, "
                f"Response: {app_response.text}"
            )

        app_data = app_response.json()
        client_id = app_data['client_id']
        client_secret = app_data['client_secret']

        pretty_step(f"OAuth App Registered")
        pretty_step(f"Client ID: {client_id}")
        pretty_step(f"Client Secret: {client_secret}")

    except Exception as e:
        pretty_step(f"Failed to register app: {e}","red")
        raise

    # Step 2: Get Access Token using Password Grant
    pretty_step("\n[2/2] Getting Access Token...")

    # Try different username formats
    username_attempts = [
        ("email format", admin_email),
        ("username only", admin_email.split('@')[0]),
    ]

    token_data = None
    last_error = None

    for attempt_name, username in username_attempts:
        pretty_step(f"   Trying with {attempt_name}: {username}")

        try:
            token_response = requests.post(
                f"{base_url}/oauth/token",
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "password",
                    "username": username,
                    "password": admin_password,
                    "scope": "read write follow"
                }
            )

            if token_response.status_code == 200:
                token_data = token_response.json()
                pretty_step(f"Success with {attempt_name}!")
                break
            else:
                last_error = token_response.json()
                pretty_step(f"Failed with {attempt_name}: {last_error.get('error', 'unknown')}",color="red")

        except Exception as e:
            last_error = str(e)
            pretty_step(f"Exception with {attempt_name}: {e}",color="red")

    # If password grant failed, provide manual instructions
    if not token_data:
        print("\n" + "=" * 60)
        print("Password grant failed. Manual token generation required.")
        print("=" * 60)
        print("\nOption 1: Use Rails Console (Recommended)")
        print("-" * 60)
        print("Run these commands in your Mastodon container:\n")
        print("docker exec -it mastodon-web-1 bash")
        print("RAILS_ENV=production bundle exec rails console\n")
        print("Then paste this Ruby code:\n")
        print(f"""
user = User.find_by(email: '{admin_email}')
app = Doorkeeper::Application.find_by(client_id: '{client_id}')
token = Doorkeeper::AccessToken.create!(
  application_id: app.id,
  resource_owner_id: user.id,
  scopes: 'read write follow',
  expires_in: 7200
)
puts "ACCESS_TOKEN: #{{token.token}}"
""")
        print("\nOption 2: Use Web Browser")
        print("-" * 60)
        print(
            f"1. Open: {base_url}/oauth/authorize?client_id={client_id}&scope=read+write+follow&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code")
        print(f"2. Login with email: {admin_email}")
        print(f"3. Click 'Authorize'")
        print(f"4. Copy the authorization code")
        print(f"5. Run this curl command:\n")
        print(f"""curl -X POST {base_url}/oauth/token \\
  -d "client_id={client_id}" \\
  -d "client_secret={client_secret}" \\
  -d "grant_type=authorization_code" \\
  -d "code=YOUR_CODE_HERE" \\
  -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob"
""")

        raise Exception(
            f"Failed to get access token. Last error: {last_error}"
        )

    access_token = token_data['access_token']

    pretty_step(f"Access Token Obtained")
    pretty_step(f"   Token: {access_token}")

    credentials = {
        'client_id': client_id,
        'client_secret': client_secret,
        'access_token': access_token,
        'token_type': token_data.get('token_type', 'Bearer'),
        'scope': token_data.get('scope', 'read write follow'),
        'created_at': token_data.get('created_at')
    }

    print("\n" + "=" * 60)
    print("OAuth Flow Complete!")
    print("=" * 60)

    return credentials

def main(sha=None, issue_id=None):
    # Ensure required tools
    pretty_section(f"Deploying Mastodom (isuue number {issue_id}) at SHA: {sha}")
    for tool in ("git", "docker", "docker-compose"):
        check_prereq(tool)
    # Determine repo URL based on SHA
    repo_url = PATCHED_SHAS.get(sha, REPO_URL)
    print(repo_url)
    if sha in PATCHED_SHAS:
        print(f"[INFO] Using patched fork for SHA {sha}: {repo_url}")

    # Clone repo if not exists
    # if not os.path.isdir(PROJECT_DIR):
    #     print(f"[INFO] Cloning Mastodon into '{PROJECT_DIR}' …")
    #     run(["git", "clone", repo_url, PROJECT_DIR])
    if os.path.isdir(PROJECT_DIR):
        print(f"[INFO] Deleting existing folder: {PROJECT_DIR}")
        shutil.rmtree(PROJECT_DIR)

    print(f"[INFO] Cloning Mastodon into '{PROJECT_DIR}' …")
    run(["git", "clone", repo_url, PROJECT_DIR])
    os.chdir(PROJECT_DIR)
    print("[INFO] Resetting local changes from previous deployments …")
    try:
        run(["git", "reset", "--hard"])
        run(["git", "clean", "-fd"])
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Could not reset local changes: {e}")

    # Add fork remote if SHA is patched
    if sha in PATCHED_SHAS:
        fork_url = PATCHED_SHAS[sha]
        try:
            run(["git", "remote", "add", "patched_fork", fork_url])
            print(f"[INFO] Added remote 'patched_fork' -> {fork_url}")
        except subprocess.CalledProcessError:
            # Remote probably already exists, safe to ignore
            print(f"[INFO] Remote 'patched_fork' already exists")

    # Fetch all branches and tags
    print("[INFO] Fetching all remotes …")
    run(["git", "fetch", "--all", "--tags"])

    # Reset any local changes from previous deployments


    # Check SHA existence
    # Check SHA existence (with better fallback logic)
    if sha and sha != "latest" and not sha_exists(sha):
        # 1) First try fetching the SHA directly (works for dangling commits if server allows it)
        primary_remote = "patched_fork" if sha in PATCHED_SHAS else "origin"
        print(f"[INFO] SHA {sha} not found locally. Trying direct fetch from {primary_remote} …")
        try:
            run(["git", "fetch", primary_remote, sha])
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Direct fetch from {primary_remote} failed: {e}")

        # 2) If still missing and it's a patched SHA, then fetch all branches from fork (your existing behavior)
        if not sha_exists(sha) and sha in PATCHED_SHAS:
            print(f"[INFO] SHA {sha} still missing. Fetching all branches from patched fork …")
            run(["git", "fetch", "patched_fork", "+refs/heads/*:refs/remotes/patched_fork/*"])
            # (optional) also fetch tags from fork
            run(["git", "fetch", "patched_fork", "--tags"])

        # 3) Final check
        if not sha_exists(sha):
            print(f"[ERROR] SHA {sha} still not found after all fetch attempts. Aborting.")
            print("[HINT] The SHA may not exist in this fork, or GitHub may not serve it unless reachable from a ref.")
            sys.exit(1)

    # Checkout SHA or branch
    try:
        if sha:
            if sha == "latest":
                default_branch = get_default_branch()
                pretty_step(f"Checking out latest default branch: {default_branch}")
                run(["git", "checkout", default_branch])
                run(["git", "pull", "origin", default_branch])
            else:
                pretty_step(f"Checking out SHA: {sha}")
                run(["git", "checkout", sha])
        else:
            pretty_step("No SHA provided. Pulling latest 'main' branch …")
            run(["git", "checkout", "main"])
            run(["git", "pull", "origin", "main"])
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Checkout failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Copy .env.sample → .env.production if not exists
    if os.path.exists(ENV_SAMPLE) and not os.path.exists(ENV_TARGET):
        pretty_step(f" Copying {ENV_SAMPLE} → {ENV_TARGET}")
        shutil.copy(ENV_SAMPLE, ENV_TARGET)

    # Update LOCAL_DOMAIN, DB_HOST, REDIS_HOST, and LOCAL_HTTPS in env file
    if os.path.exists(ENV_TARGET):
        lines = []
        with open(ENV_TARGET, "r") as f:
            for line in f:
                line_stripped = line.strip()
                if not line_stripped.startswith("LOCAL_DOMAIN=") and \
                   not line_stripped.startswith("DB_HOST=") and \
                   not line_stripped.startswith("REDIS_HOST=") and \
                   not line_stripped.startswith("LOCAL_HTTPS="):
                    lines.append(line.rstrip())
        lines.append("LOCAL_DOMAIN=localhost")
        lines.append("DB_HOST=db")
        lines.append("REDIS_HOST=redis")
        lines.append("LOCAL_HTTPS=false")
        with open(ENV_TARGET, "w") as f:
            f.write("\n".join(lines) + "\n")
        pretty_step(f" Set LOCAL_DOMAIN=localhost, DB_HOST=db, REDIS_HOST=redis, LOCAL_HTTPS=false in {ENV_TARGET}")

    # Generate SECRET_KEY_BASE and OTP_SECRET if not present
    pretty_step("Checking for required secrets …")
    env_content = ""
    if os.path.exists(ENV_TARGET):
        with open(ENV_TARGET, "r") as f:
            env_content = f.read()

    missing_secrets = []
    has_valid_secret_key = False
    has_valid_otp = False

    # Check if secrets exist and are not empty
    for line in env_content.split('\n'):
        line = line.strip()
        if line.startswith("SECRET_KEY_BASE=") and len(line.split('=', 1)) > 1:
            secret_value = line.split('=', 1)[1].strip()
            if secret_value and not secret_value.startswith('#'):
                has_valid_secret_key = True
        if line.startswith("OTP_SECRET=") and len(line.split('=', 1)) > 1:
            otp_value = line.split('=', 1)[1].strip()
            if otp_value and not otp_value.startswith('#'):
                has_valid_otp = True

    if not has_valid_secret_key:
        missing_secrets.append("SECRET_KEY_BASE")
    if not has_valid_otp:
        missing_secrets.append("OTP_SECRET")

    if missing_secrets:
        print(f"[INFO] Generating missing secrets: {', '.join(missing_secrets)}")
        # Generate secrets using OpenSSL directly instead of rake
        import secrets as secrets_module
        import string

        def generate_secret(length=128):
            """Generate a cryptographically secure random secret"""
            alphabet = string.ascii_letters + string.digits
            return ''.join(secrets_module.choice(alphabet) for _ in range(length))

        secret_key_base = generate_secret(128) if not has_valid_secret_key else None
        otp_secret = generate_secret(128) if not has_valid_otp else None

        # Remove any existing empty or commented entries
        lines = []
        with open(ENV_TARGET, "r") as f:
            for line in f:
                line_stripped = line.strip()
                # Skip empty SECRET_KEY_BASE or OTP_SECRET lines
                if line_stripped.startswith("SECRET_KEY_BASE="):
                    continue
                if line_stripped.startswith("OTP_SECRET="):
                    continue
                lines.append(line.rstrip())

        # Add new secrets
        lines.append("")
        lines.append("# Generated Secrets")
        if secret_key_base:
            lines.append(f"SECRET_KEY_BASE={secret_key_base}")
        if otp_secret:
            lines.append(f"OTP_SECRET={otp_secret}")

        with open(ENV_TARGET, "w") as f:
            f.write("\n".join(lines) + "\n")

        print(f"[INFO] Added secrets to {ENV_TARGET}")

    # Generate encryption keys if not already present
    print("[INFO] Checking for ActiveRecord encryption keys …")
    needs_encryption_keys = False
    if os.path.exists(ENV_TARGET):
        with open(ENV_TARGET, "r") as f:
            content = f.read()
            if "ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY=" not in content or \
                    "ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY=" not in content or \
                    "ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT=" not in content:
                needs_encryption_keys = True

    if needs_encryption_keys:
        pretty_step("Generating ActiveRecord encryption keys …")
        # Generate encryption keys using Python
        import secrets as secrets_module
        import base64

        def generate_encryption_key():
            """Generate a base64 encoded 32-byte key"""
            key_bytes = secrets_module.token_bytes(32)
            return base64.b64encode(key_bytes).decode('utf-8')

        primary_key = generate_encryption_key()
        deterministic_key = generate_encryption_key()
        key_derivation_salt = generate_encryption_key()

        with open(ENV_TARGET, "a") as f:
            f.write("\n# ActiveRecord Encryption Keys\n")
            f.write(f"ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY={primary_key}\n")
            f.write(f"ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY={deterministic_key}\n")
            f.write(f"ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT={key_derivation_salt}\n")
        pretty_step(f"pretty_stepAdded encryption keys to {ENV_TARGET}")

    # Fix Gemfile.lock for json-canonicalization compatibility
    gemfile_lock = "Gemfile.lock"
    if os.path.exists(gemfile_lock):
        pretty_step("Fixing Gemfile.lock for json-canonicalization compatibility …")
        try:
            subprocess.run(
                ["sed", "-i", "", "s/json-canonicalization (0.3.2)/json-canonicalization (1.0.0)/", gemfile_lock],
                check=True,
                cwd=PROJECT_DIR
            )
            pretty_step("Updated json-canonicalization version in Gemfile.lock")
        except subprocess.CalledProcessError as e:
            pretty_step(f"Failed to update Gemfile.lock: {e}",color="red")

    # Disable eager loading and force_ssl for local development
    prod_config = "config/environments/production.rb"
    if os.path.exists(prod_config):
        pretty_step("[INFO] Configuring production environment for local development …")
        try:
            subprocess.run(
                ["sed", "-i", "", "s/config.eager_load = true/config.eager_load = false/", prod_config],
                check=True,
                cwd=PROJECT_DIR
            )
            subprocess.run(
                ["sed", "-i", "", "s/config.force_ssl = true/config.force_ssl = false/", prod_config],
                check=True,
                cwd=PROJECT_DIR
            )
            print("[INFO] Disabled eager loading and force_ssl")
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Failed to configure production environment: {e}")
    # Build and start Mastodon
    pretty_step("Building and starting Mastodon in detached mode …")
    run(["docker-compose", "up", "--build", "-d"])

    # Wait for database to be ready
    pretty_step("Waiting for database to be ready …")
    import time
    time.sleep(10)

    # Create database user and database directly with psql
    pretty_step(" Creating database user and database …")
    db_created = False
    try:
        # Create user
        subprocess.run(
            ["docker-compose", "exec", "-T", "db", "psql", "-U", "postgres", "-c",
             "CREATE USER mastodon CREATEDB;"],
            cwd=PROJECT_DIR,
            capture_output=True,
            check=False  # Ignore if user already exists
        )

        # Create database
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "psql", "-U", "postgres", "-c",
             "CREATE DATABASE mastodon_production OWNER mastodon;"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=False  # Ignore if already exists
        )

        if result.returncode == 0 or "already exists" in result.stderr:
            db_created = True
            pretty_step("Database created or already exists")
        else:
            pretty_step(f"Database creation output: {result.stderr if result.stderr else 'OK'}")
            db_created = True  # Assume it exists if no error
    except subprocess.CalledProcessError as e:
        pretty_step(f"Database setup warning: {e}")
        db_created = True  # Try to continue anyway

    # Check if database is already migrated
    pretty_step("Checking database state …")
    tables_exist = False
    try:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "psql", "-U", "mastodon", "-d", "mastodon_production", "-c",
             "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 and result.stdout:
            # Check if we have more than 0 tables
            tables_exist = "0" not in result.stdout or result.stdout.count('\n') > 3
    except:
        pass

    # Run database migrations
    migration_success = False
    if db_created:
        pretty_step("Running database migrations …")
        try:
            # Use db:schema:load for fresh databases, db:migrate for existing ones
            task = "db:migrate" if tables_exist else "db:schema:load"
            result = subprocess.run(
                ["docker-compose", "run", "--rm", "web", "bundle", "exec", "rake", task],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True,
                check=True
            )
            pretty_step(f"[INFO] Database migrations complete (used {task})")
            migration_success = True
        except subprocess.CalledProcessError as e:
            pretty_step(f"[WARN] Database migration failed with exit code {e.returncode}")
            if e.stderr:
                print(f"[ERROR] {e.stderr[:500]}")
            pretty_step("[INFO] You may need to run manually:")
            pretty_step("       docker-compose run --rm web bundle exec rake db:schema:load")

    # Run database seed (only if migrations succeeded)
    if migration_success:
        pretty_step("[INFO] Seeding database …")
        try:
            subprocess.run(
                ["docker-compose", "run", "--rm", "web", "bundle", "exec", "rake", "db:seed"],
                cwd=PROJECT_DIR,
                check=False  # Don't fail if seed has issues
            )
            print("[INFO] Database setup complete")
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Database seed had issues: {e}")

    # Create admin account (only if migrations succeeded)
    if migration_success:
        print("[INFO] Setting up admin account …")
        admin_username = "testadmin"
        admin_email = "admin@localhost"
        password = None

        # Try to create account first
        result = subprocess.run(
            ["docker-compose", "run", "--rm", "web", "bin/tootctl", "accounts", "create",
             admin_username, "--email", admin_email, "--confirmed", "--role", "Owner"],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR
        )

        # Extract password from output
        for line in result.stdout.split('\n'):
            if "New password:" in line:
                password = line.split("New password:")[-1].strip()
                break

        # If account already exists, reset password to get credentials
        if not password:
            output = result.stdout + result.stderr
            if "taken" in output or result.returncode != 0:
                print(f"[INFO] Admin account '{admin_username}' already exists. Resetting password …")
                reset_result = subprocess.run(
                    ["docker-compose", "run", "--rm", "web", "bin/tootctl", "accounts", "modify",
                     admin_username, "--reset-password"],
                    capture_output=True,
                    text=True,
                    cwd=PROJECT_DIR
                )
                # Extract password from reset output
                for line in reset_result.stdout.split('\n'):
                    if "New password:" in line:
                        password = line.split("New password:")[-1].strip()
                        break
        args = {
            "issue_id": issue_id,
            "project": "nocodb",
            "extra_flag": True,
            "port": "http://localhost:3000"
        }

        mastodon_oauth_flow(admin_email=admin_email, admin_password=password)
        run_issue_hook(issue_id, args, issues_module=mastodon_isuue)

        pretty_section("NetBox is ready", color="green")

        # Display credentials
        if password:
            print("\n" + "="*60)
            print("MASTODON IS READY!")
            print("="*60)
            print(f"URL:      http://localhost:3000")
            print(f"Username: {admin_username}")
            print(f"Password: {password}")
            print(f"Email:    {admin_email}")
            print(f"Role:     Owner (Admin)")
            print("="*60 + "\n")
        else:
            print(f"[WARN] Could not retrieve admin password.")
            print(f"[INFO] Reset password manually with:")
            print(f"       docker-compose run --rm web bin/tootctl accounts modify {admin_username} --reset-password")
    else:
        print("[WARN] Skipping admin account creation due to migration failure")
        print("[INFO] Fix the database issues and run:")
        print("       docker-compose run --rm web bin/tootctl accounts create testadmin --email admin@localhost --confirmed --role Owner")

    pretty_step("[INFO] Mastodon is up and running at http://localhost:3000")

    base_url = "http://localhost:3000",
    admin_email = "admin@localhost",
    admin_password = "add11dc7cd2870781b7110e89657002b",
    client_name = "Test Client",

    mastodon_oauth_flow(admin_email=admin_email,admin_password=password )

def stop():
    print("[INFO] Stopping Mastodon containers …")
    if os.path.isdir(PROJECT_DIR):
        os.chdir(PROJECT_DIR)
        try:
            run(["docker-compose", "stop"])
            print("[INFO] Mastodon containers stopped.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Stop failed: {e}")
    else:
        print(f"[WARN] Directory '{PROJECT_DIR}' not found. Cannot stop.")


def clean():
    print("[INFO] Removing Mastodon containers and volumes …")
    if not os.path.isdir(PROJECT_DIR):
        print(f"[WARN] Directory '{PROJECT_DIR}' not found. Nothing to clean.")
        return
    os.chdir(PROJECT_DIR)
    try:
        run(["docker-compose", "down", "--remove-orphans", "--volumes"])
        print("[INFO] Cleanup successful.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Cleanup failed: {e}")


if __name__ == "__main__":
    sha = sys.argv[1] if len(sys.argv) > 1 else None
    main(sha)
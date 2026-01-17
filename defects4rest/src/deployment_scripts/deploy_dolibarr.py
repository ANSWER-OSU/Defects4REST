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
Dolibarr Deployment Script
This script automates the deployment of Dolibarr ERP/CRM using Docker.
It clones the repository, checks out a specific commit, builds a Docker image, and launches the application with a MariaDB database.
"""
import subprocess
import shutil
import os
import sys
from textwrap import dedent
from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.git import sha_exists, get_default_branch
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq

# Repository and file configuration
REPO_URL = "https://github.com/dolibarr/dolibarr.git"
BASE_COMPOSE = "docker-compose.yml"
OVERRIDE_COMPOSE = "docker-compose.override.yml"
LOCAL_DOCKERFILE = "Dockerfile"

# Get the root directory of the Defects4REST project (2 levels up from this script)
PROJECT_DIR = str(ensure_temp_project_dir("dolibarr"))

# This defines a basic Dolibarr setup with MariaDB database
FALLBACK_COMPOSE_CONTENT = dedent("""\
version: "3.1"
services:
  db:
    image: mariadb:10.5
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    environment:
      MARIADB_ROOT_PASSWORD: rootpassword
      MARIADB_DATABASE: dolibarr
      MARIADB_USER: dolibarr
      MARIADB_PASSWORD: dolibarr
    volumes:
      - db_data:/var/lib/mysql

  dolibarr:
    image: dolibarr/dolibarr:latest
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      DOLI_DB_HOST: db
      DOLI_DB_NAME: dolibarr
      DOLI_DB_USER: dolibarr
      DOLI_DB_PASSWORD: dolibarr
    volumes:
      - dolibarr_html:/var/www/html
      - dolibarr_documents:/var/www/documents

volumes:
  db_data:
  dolibarr_html:
  dolibarr_documents:
""")

# Override compose configuration that builds Dolibarr from local source
OVERRIDE_COMPOSE_CONTENT = dedent("""\
version: "3.1"
services:
  dolibarr:
    build: .
    image: dolibarr_local:from_source
    depends_on:
      - db
    volumes:
      - dolibarr_html:/var/www/html
      - dolibarr_documents:/var/www/documents
""")

# Dockerfile for building Dolibarr with PHP 7.4
DOCKERFILE_CONTENT = dedent("""\
FROM php:7.4-apache

RUN apt-get update && apt-get install -y \
    libpng-dev libjpeg-dev libfreetype6-dev libzip-dev zip unzip default-mysql-client \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install gd mysqli pdo pdo_mysql zip \
 && rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite && \
    cat >/etc/apache2/conf-available/dolibarr.conf <<'EOF'
<Directory /var/www/html>
    AllowOverride All
    Require all granted
</Directory>
DirectoryIndex index.php index.html
EOF
RUN a2enconf dolibarr

COPY htdocs/ /var/www/html/

RUN mkdir -p /var/www/documents && \
    chown -R www-data:www-data /var/www/html /var/www/documents && \
    chmod -R 755 /var/www/html

EXPOSE 80
""")

# Special Dockerfile for bug #26307 that requires PHP 8.1
DOCKERFILE_CONTENT_26307 = dedent("""\
FROM php:8.1-apache

RUN apt-get update && apt-get install -y \
    libpng-dev libjpeg-dev libfreetype6-dev libzip-dev zip unzip default-mysql-client \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install gd mysqli pdo pdo_mysql zip \
 && rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite && \
    cat >/etc/apache2/conf-available/dolibarr.conf <<'EOF'
<Directory /var/www/html>
    AllowOverride All
    Require all granted
</Directory>
DirectoryIndex index.php index.html
EOF
RUN a2enconf dolibarr

COPY htdocs/ /var/www/html/

RUN mkdir -p /var/www/documents && \
    chown -R www-data:www-data /var/www/html /var/www/documents && \
    chmod -R 755 /var/www/html

EXPOSE 80
""")

def get_compose_cmd():
    """
    Determine which Docker Compose command is available on the system.

    Returns:
        list: Command array for Docker Compose ('docker compose' or 'docker-compose')
    """
    # Try Docker Compose plugin first
    try:
        subprocess.run(
            ["docker", "compose", "version"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return ["docker", "compose"]
    except Exception:
        pass

    # Try legacy docker-compose standalone
    legacy = shutil.which("docker-compose")
    if legacy:
        try:
            subprocess.run(
                [legacy, "version"],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return [legacy]
        except Exception as e:
            raise RuntimeError(
                "Found 'docker-compose' but it failed to run. On Python 3.12, "
                "install 'python3-distutils' or switch to the Docker Compose plugin.\n"
                f"Underlying error: {e}"
            )

    # Neither variant found
    raise RuntimeError(
        "Neither 'docker compose' nor 'docker-compose' is available.\n"
        "Install the plugin: sudo apt install -y docker-compose-plugin"
    )

def ensure_files(issue_id=None):
    """
    Create or update required Docker configuration files.

    Args:
        issue_id (int, optional): Issue number for special configurations (e.g., 26307 for PHP 8.1)
    """
    # Create base compose file if missing
    if not os.path.exists(BASE_COMPOSE):
        print(f"{BASE_COMPOSE} not found in repo. Writing a fallback compose …")
        with open(BASE_COMPOSE, "w") as f:
            f.write(FALLBACK_COMPOSE_CONTENT)

    # Always create override to build from local source
    pretty_step(f"Writing {OVERRIDE_COMPOSE} (build from local) …")
    with open(OVERRIDE_COMPOSE, "w") as f:
        f.write(OVERRIDE_COMPOSE_CONTENT)

    # Create or refresh Dockerfile
    if not os.path.exists(LOCAL_DOCKERFILE):
        pretty_step(f"Writing {LOCAL_DOCKERFILE} …")
    else:
        pretty_step(f"{LOCAL_DOCKERFILE} exists — refreshing to known-good content …")

    with open(LOCAL_DOCKERFILE, "w") as f:
        # Use PHP 8.1 for bug #26307, otherwise use PHP 7.4
        if issue_id == 26307:
            pretty_step("Using PHP 8.1 Dockerfile for bug #26307")
            f.write(DOCKERFILE_CONTENT_26307)
        else:
            f.write(DOCKERFILE_CONTENT)

def get_container_name():
    """
    Find the running Dolibarr container name.

    Returns:
        str: Name of the running Dolibarr container
    """
    # Try common container naming patterns first
    possible_names = [
        "dolibarr-dolibarr-1",
        "dolibarr_dolibarr_1",
        f"{os.path.basename(PROJECT_DIR)}-dolibarr-1",
        f"{os.path.basename(PROJECT_DIR)}_dolibarr_1",
    ]

    for name in possible_names:
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={name}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                return result.stdout.strip()
        except subprocess.CalledProcessError:
            continue

    # Fallback: find any container with "dolibarr" that's not the database
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=dolibarr", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        containers = result.stdout.strip().split('\n')
        if containers and containers[0]:
            for container in containers:
                if 'db' not in container.lower():
                    return container
    except subprocess.CalledProcessError:
        pass

    raise RuntimeError("Could not find dolibarr container. Is it running?")

def wait_for_installation():
    """
    Pause execution and wait for user to complete manual Dolibarr installation wizard.
    """
    print("")
    pretty_step("Please complete the Dolibarr installation wizard at http://localhost:8080")
    print("")
    pretty_step("Use these database settings:")
    pretty_step("  Host: db")
    pretty_step("  Database: dolibarr")
    pretty_step("  User: dolibarr")
    pretty_step("  Password: dolibarr")
    print("")
    pretty_step("Press Enter once you've completed the installation and can see the login page...", color="green")
    input()

def configure_api_and_modules():
    """
    Automatically configure Dolibarr by enabling all modules and granting admin permissions.

    This discovers all available modules, enables them in the database, activates them
    to generate permissions, and grants all permissions to the admin user.
    """
    pretty_section("Enabling all modules and configuring permissions...")

    # Find the Dolibarr container
    try:
        container_name = get_container_name()
        pretty_step(f"Found container: {container_name}")
    except RuntimeError as e:
        pretty_step(f"Warning: {e}", color="yellow")
        container_name = "dolibarr-dolibarr-1"

    try:
        # Query database for admin user ID
        pretty_step("Finding admin user...")
        result = subprocess.run(
            ["docker", "exec", container_name, "mysql", "-h", "db", "-u", "dolibarr",
             "-pdolibarr", "dolibarr", "-sNe", "SELECT rowid FROM llx_user WHERE admin=1 LIMIT 1"],
            capture_output=True, text=True, check=True
        )
        admin_user_id = result.stdout.strip()

        # Fallback to user ID 1 if no admin found
        if not admin_user_id:
            pretty_step("No admin user found, using user ID 1", color="yellow")
            admin_user_id = "1"
        else:
            pretty_step(f"Found admin user with ID: {admin_user_id}")

        # Scan filesystem for all module class files
        pretty_step("Discovering all available modules...")

        result = subprocess.run(
            ["docker", "exec", container_name, "find",
             "/var/www/html/", "-path", "*/core/modules/mod*.class.php", "-type", "f"],
            capture_output=True, text=True, check=True
        )

        module_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # Extract module names from filenames (e.g., "modProductOrService.class.php" -> "PRODUCTORSERVICE")
        module_names = []
        for module_file in module_files:
            if module_file:
                basename = os.path.basename(module_file)
                if basename.startswith('mod') and basename.endswith('.class.php'):
                    module_name = basename[3:-10]  # Remove 'mod' prefix and '.class.php' suffix
                    if module_name:
                        module_names.append(module_name.upper())

        # Remove duplicates and sort
        module_names = sorted(list(set(module_names)))

        pretty_step(f"Found {len(module_names)} modules to enable")

        # Build SQL to enable REST API and all discovered modules
        pretty_step("Enabling all discovered modules in config...")

        sql_commands = """
-- Enable REST API module
INSERT INTO llx_const (name, value, type, note, visible, entity) 
VALUES ('MAIN_MODULE_API', '1', 'chaine', 'Enable API module', '0', '1')
ON DUPLICATE KEY UPDATE value='1';

INSERT INTO llx_const (name, value, type, note, visible, entity) 
VALUES ('MAIN_MODULE_WEBSERVICES', '1', 'chaine', 'Enable webservices', '0', '1')
ON DUPLICATE KEY UPDATE value='1';

-- Remove API endpoint restrictions
DELETE FROM llx_const WHERE name = 'API_ENDPOINT_RULES';

-- Enable API Explorer
INSERT INTO llx_const (name, value, type, note, visible, entity) 
VALUES ('API_EXPLORER_ENABLED', '1', 'chaine', 'Enable API Explorer', '0', '1')
ON DUPLICATE KEY UPDATE value='1';

"""

        # Add INSERT statement for each discovered module
        for module in module_names:
            sql_commands += f"INSERT INTO llx_const (name, value, type, note, visible, entity) VALUES ('MAIN_MODULE_{module}', '1', 'chaine', '', '0', '1') ON DUPLICATE KEY UPDATE value='1';\n"

        # Write SQL to temporary file in container and execute
        run(["docker", "exec", "-i", container_name, "sh", "-c",
             f"cat > /tmp/setup.sql << 'EOFSQL'\n{sql_commands}\nEOFSQL\n"])

        run(["docker", "exec", container_name, "sh", "-c",
             "mysql -h db -u dolibarr -pdolibarr dolibarr < /tmp/setup.sql"])

        # Activate modules using Dolibarr's internal API to generate permission definitions
        pretty_step("Activating modules to generate permissions (this may take a minute)...")

        activation_script = """<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

define('NOCSRFCHECK', 1);
define('NOTOKENRENEWAL', 1);

$_SERVER['REMOTE_ADDR'] = '127.0.0.1';

require_once '/var/www/html/master.inc.php';
require_once DOL_DOCUMENT_ROOT.'/core/lib/admin.lib.php';

global $db, $conf, $user;

// Load admin user
$user = new User($db);
$user->fetch(1);
$user->admin = 1;

echo "Activating modules and generating permissions...\\n";

// Get enabled modules from config
$sql = "SELECT name FROM llx_const WHERE name LIKE 'MAIN_MODULE_%' AND value = '1'";
$resql = $db->query($sql);
$modules_to_activate = array();

if ($resql) {
    while ($obj = $db->fetch_object($resql)) {
        $module_const = $obj->name;
        $module_name = str_replace('MAIN_MODULE_', '', $module_const);

        // Convert to proper module class name format
        $module_class = 'mod' . ucfirst(strtolower($module_name));
        $modules_to_activate[] = $module_class;
    }
}

echo "Found " . count($modules_to_activate) . " modules to activate\\n";

$activated_count = 0;
foreach ($modules_to_activate as $module_class) {
    $file_path = DOL_DOCUMENT_ROOT.'/core/modules/'.$module_class.'.class.php';

    if (file_exists($file_path)) {
        try {
            require_once $file_path;

            if (class_exists($module_class)) {
                $module_obj = new $module_class($db);

                // Call init to generate permissions
                $result = $module_obj->init();

                if ($result > 0) {
                    $activated_count++;
                }
            }
        } catch (Exception $e) {
            // Skip modules that fail
        }
    }
}

echo "Successfully activated $activated_count modules\\n";
echo "Permissions have been generated\\n";
"""

        # Write and execute PHP activation script
        run(["docker", "exec", "-i", container_name, "sh", "-c",
             f"cat > /tmp/activate.php << 'EOFPHP'\n{activation_script}\nEOFPHP\n"])

        try:
            run(["docker", "exec", container_name, "php", "/tmp/activate.php"])
        except subprocess.CalledProcessError as e:
            pretty_step("Some modules failed to activate, continuing...", color="yellow")

        # Grant all generated permissions to admin user
        pretty_step("Granting all permissions to admin user...")
        permissions_sql = f"""
DELETE FROM llx_user_rights WHERE fk_user = {admin_user_id};

INSERT INTO llx_user_rights (fk_user, fk_id, entity)
SELECT {admin_user_id}, id, 1 FROM llx_rights_def;

UPDATE llx_user SET admin = 1, statut = 1 WHERE rowid = {admin_user_id};
"""

        # Write and execute permissions SQL
        run(["docker", "exec", "-i", container_name, "sh", "-c",
             f"cat > /tmp/permissions.sql << 'EOFSQL'\n{permissions_sql}\nEOFSQL\n"])

        run(["docker", "exec", container_name, "sh", "-c",
             "mysql -h db -u dolibarr -pdolibarr dolibarr < /tmp/permissions.sql"])

        # Verify the setup by counting permissions
        result = subprocess.run(
            ["docker", "exec", container_name, "mysql", "-h", "db", "-u", "dolibarr",
             "-pdolibarr", "dolibarr", "-sNe", "SELECT COUNT(*) FROM llx_rights_def"],
            capture_output=True, text=True, check=True
        )
        perm_count = result.stdout.strip()

        # Display success summary
        print("")
        pretty_step("✓ REST API enabled", color="green")
        pretty_step(f"✓ {len(module_names)} modules enabled", color="green")
        pretty_step(f"✓ {perm_count} permissions granted to admin user", color="green")
        print("")
        pretty_section("Configuration Complete!", color="green")
        print("")
        pretty_step("Dolibarr is ready at: http://localhost:8080")
        print("")
        pretty_step("Enabled modules include:")
        for i, module in enumerate(module_names[:15]):
            pretty_step(f"  - {module}")
        if len(module_names) > 15:
            pretty_step(f"  ... and {len(module_names) - 15} more")
        print("")

    except subprocess.CalledProcessError as e:
        pretty_step(f"Configuration failed: {e}", color="red")
        sys.exit(1)

def main(sha=None, issue_id=None):
    """
    Main deployment function for Dolibarr.

    Args:
        sha (str, optional): Git commit SHA to checkout for default branch
        issue_id (int, optional): Issue number for special configurations
    """
    pretty_section(f"Deploying dolibarr (issue number {issue_id}) at SHA: {sha}")

    # Verify required tools are available
    for tool in ("git", "docker"):
        check_prereq(tool)

    compose = get_compose_cmd()
    print(PROJECT_DIR)

    project_dir_abs = os.path.abspath(PROJECT_DIR)
    parent_dir = os.path.dirname(project_dir_abs)

    # Change directory if currently in project directory
    try:
        cwd_abs = os.path.abspath(os.getcwd())
        if cwd_abs == project_dir_abs or cwd_abs.startswith(project_dir_abs + os.sep):
            os.chdir(parent_dir)
    except FileNotFoundError:
        os.chdir(parent_dir)

    # Clean up existing deployment if compose file exists
    compose_file = os.path.join(project_dir_abs, "docker-compose.yml")
    if os.path.exists(compose_file):
        clean(heading=False)

    # Remove existing repo
    if os.path.isdir(project_dir_abs):
        pretty_subsection("Removing existing Dolibarr repository …")
        pretty_step(f"Deleting '{project_dir_abs}' …")
        shutil.rmtree(project_dir_abs)

    # Ensure parent directory exists
    os.makedirs(parent_dir, exist_ok=True)

    # Clone repository
    pretty_subsection("Cloning Dolibarr repository …")
    pretty_step(f"Cloning into '{project_dir_abs}' …")
    run(["git", "clone", REPO_URL, project_dir_abs], cwd=parent_dir)

    # Change to project directory for all subsequent operations
    os.chdir(PROJECT_DIR)

    try:
        pretty_subsection("Checking out specific SHA …")
        if sha:
            if sha == "latest":
                # Pull latest from default branch
                print("Pulling latest default branch …")
                run(["git", "fetch", "--all"])
                default_branch = get_default_branch()
                print(f"Using default branch: {default_branch}")
                run(["git", "checkout", default_branch])
                run(["git", "pull", "origin", default_branch])
            else:
                # Check out specific commit
                if not sha_exists(sha):
                    print(f"SHA {sha} not found locally; fetching …")
                    run(["git", "fetch", "--all", "--tags"])
                print(f"Checking out SHA: {sha}")
                run(["git", "checkout", sha])
    except subprocess.CalledProcessError as e:
        print(f"Checkout failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Create Docker configuration files
    ensure_files(issue_id=issue_id)

    # Build and launch Docker containers
    pretty_subsection("Building Docker image …")
    pretty_step("\nLaunching Dolibarr (built from local checkout) via Docker Compose …")
    try:
        run(compose + [
            "-f", BASE_COMPOSE,
            "-f", OVERRIDE_COMPOSE,
            "up", "-d", "--remove-orphans", "--build"
        ])

        pretty_section("Dolibarr container is running", color="green")
        pretty_step("Dolibarr is live at: http://localhost:8080")
        pretty_step("Use these database settings:")
        pretty_step("  Database server: db")
        pretty_step("  Database: dolibarr")
        pretty_step("  User: dolibarr")
        pretty_step("  Password: dolibarr")
        print("")

    except subprocess.CalledProcessError as e:
        pretty_step(f"Launch failed: {e}", file=sys.stderr)
        sys.exit(1)

def stop():
    """
    Stop running Dolibarr containers without removing volumes or data.
    """
    pretty_section("Stopping Dolibarr containers …")
    if os.path.isdir(PROJECT_DIR):
        os.chdir(PROJECT_DIR)
        try:
            compose = get_compose_cmd()
            # Build file arguments
            files = ["-f", BASE_COMPOSE]
            if os.path.exists(OVERRIDE_COMPOSE):
                files += ["-f", OVERRIDE_COMPOSE]
            run(compose + files + ["stop"])
            pretty_step(f"Containers stopped successfully")
        except subprocess.CalledProcessError as e:
            pretty_step(f"Stop failed: {e}")
        except RuntimeError as e:
            print(str(e))
    else:
        pretty_step(f"Directory '{PROJECT_DIR}' not found. Cannot stop.", color="red")

def clean(heading=True):
    """
    Complete cleanup of Dolibarr deployment including containers, networks, and volumes.
    Args:
        heading (bool): Whether to print section heading
    """
    if heading:
        pretty_section("Cleaning up Dolibarr containers and volumes")
    if not os.path.isdir(PROJECT_DIR):
        print(f"Directory '{PROJECT_DIR}' not found. Nothing to clean.")
        return

    os.chdir(PROJECT_DIR)
    # Build file arguments
    files = ["-f", BASE_COMPOSE]
    if os.path.exists(OVERRIDE_COMPOSE):
        files += ["-f", OVERRIDE_COMPOSE]

    try:
        compose = get_compose_cmd()
        # Remove everything including volumes
        run(compose + files + ["down", "--remove-orphans", "--volumes"])
        pretty_step("Cleanup successful.")
    except subprocess.CalledProcessError as e:
        pretty_step(f"Cleanup failed: {e}")
    except RuntimeError as e:
        print(str(e))
# Defects4REST



**A comprehensive benchmark framework for systematically deploying, testing, and analyzing bugs in REST API applications.**

Defects4REST enables researchers and developers to reproduce real-world bugs in REST API services by deploying specific buggy and patched versions of applications in isolated Docker containers.



## Table of Contents

- [Features](#features)
- [Supported Projects](#supported-projects)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Info Command](#info-command)
  - [Checkout Command](#checkout-command)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Adding New Projects](#adding-new-projects)


## Features

- **Reproducible Bug Deployment** - Deploy exact buggy or patched versions of REST APIs using Git SHA references
- **Multi-Project Support** - 12+ real-world REST API projects with documented bugs
- **Container Isolation** - Each deployment runs in isolated Docker containers with automatic port management

## Supported Projects

| Project | Issues | Reproduction folder |
|---------|:------:|-------------------|
| [AWX](https://github.com/ansible/awx) | 5 | [Open folder](defects4rest/data/bug_reproduction/awx/) |
| [Dolibarr](https://github.com/Dolibarr/dolibarr) | 25 | [Open folder](defects4rest/data/bug_reproduction/dolibarr/) |
| [EnviroCar Server](https://github.com/enviroCar/enviroCar-server) | 4 | [Open folder](defects4rest/data/bug_reproduction/enviroCar-server/) |
| [Flowable Engine](https://github.com/flowable/flowable-engine) | 5 | [Open folder](defects4rest/data/bug_reproduction/flowable-engine/) |
| [Kafka REST](https://github.com/confluentinc/kafka-rest) | 3 | [Open folder](defects4rest/data/bug_reproduction/kafka-rest/) |
| [Mastodon](https://github.com/mastodon/mastodon) | 5 | [Open folder](defects4rest/data/bug_reproduction/mastodon/) |
| [NetBox](https://github.com/netbox-community/netbox) | 6 | [Open folder](defects4rest/data/bug_reproduction/netbox/) |
| [NocoDB](https://github.com/nocodb/nocodb) | 6 | [Open folder](defects4rest/data/bug_reproduction/nocodb/) |
| [Podman](https://github.com/containers/podman) | 23 | [Open folder](defects4rest/data/bug_reproduction/podman/) |
| [REST Countries](https://github.com/apilayer/restcountries) | 16 | [Open folder](defects4rest/data/bug_reproduction/restcountries/) |
| [SeaweedFS](https://github.com/seaweedfs/seaweedfs) | 9 | [Open folder](defects4rest/data/bug_reproduction/seaweedfs/) |
| [Signal CLI REST API](https://github.com/bbernhard/signal-cli-rest-api) | 3 | [Open folder](defects4rest/data/bug_reproduction/signal-cli-rest-api/) |

---

## Installation

### Prerequisites

- **Python 3.9+**
- **Docker** and **Docker Compose**
- **Git**
- **Make** (for AWX)
- **Maven** (for REST Countries)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/defects4REST.git
cd defects4REST

# Install in development mode
pip install -e .

# Verify installation
defects4rest --help
```


---

## Quick Start

```bash
# View information about a specific bug
defects4rest info -p netbox -i 18991

# Deploy the buggy version of issue #18991 for NetBox
defects4rest checkout -p netbox -i 18991 --buggy --start

# Deploy the patched version
defects4rest checkout -p netbox -i 18991 --patched --start

# Stop the running containers
defects4rest checkout -p netbox -i 18991 --stop

# Clean up all resources
defects4rest checkout -p netbox -i 18991 --clean
```

---

## Usage

### Info Command

Display detailed information about a specific bug in a project.

```bash
defects4rest info -p <project_name> -i <issue_id>
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `-p, --project` | Project name (e.g., `awx`, `netbox`, `mastodon`) |
| `-i, --issue` | Issue/bug identifier number |

**Example:**

```bash
defects4rest info -p netbox -i 18991
```

**Example Output:**


    ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                     Netbox (Issue #18991)                                                  
    ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
   
    
    Project Metadata
    Project       : netbox
    Bug ID        : 18991
    Issue Number  : 18991
    Issue URL     : https://github.com/netbox-community/netbox/issues/18991
    Title         : Path tracing broken for front/rear ports in REST API
    Days to Fix   : 2
    
    Patched Files
    - netbox/dcim/tests/test_api.py
    - netbox/utilities/fields.py
    
    Patched File Types
    - source-file
    - test-file
    
    SHAs
    Buggy SHA     : 9a1d9365cd7c703413ca8d15c0b8b737067c275e
    Patch SHA(s)  : 636148f9654b82f7e664645f3e781a4591a22132
                    fd2bcda8b8777b955222644a5ff94417ba510cb2
   


### Checkout Command

Deploy, manage, and clean up project instances at specific versions.

```bash
defects4rest checkout -p <project> -i <issue> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `-p` | Project name |
| `-i` | Issue/bug identifier |
| `--buggy` | Deploy the buggy version |
| `--patched N` | Deploy the Nth patched version (1-indexed) |
| `--start` | Start the deployment |
| `--stop` | Stop running containers (preserves data) |
| `--clean` | Remove all containers, volumes, and networks |

**Examples:**

```bash

# Deploy buggy version
defects4rest checkout -p kafka-rest -i 475 --buggy --start

# Deploy first patch
defects4rest checkout -p kafka-rest -i 475 --patched 1 --start

# Deploy second patch (if multiple patches exist)
defects4rest checkout -p kafka-rest -i 475 --patched 2 --start

# Stop containers
defects4rest checkout -p kafka-rest -i 475 --stop

# Full cleanup
defects4rest checkout -p kafka-rest -i 475 --clean
```

---

## Configuration

### Bug Metadata Format

Bug information is stored in CSV files under `defects4rest/data/defect_data/`:

```csv
bug_id,issue_no,repo,issue_url,title,description,buggy_sha,patch_sha,patched_files,patched_file_types,days_to_fix
```

**Key Fields:**

| Field | Description |
|-------|-------------|
| `bug_id` | Internal bug identifier |
| `issue_no` | GitHub/repository issue number |
| `repo` | Repository URL |
| `issue_url` | Direct link to the issue |
| `title` | Bug title/summary |
| `description` | Detailed bug description |
| `buggy_sha` | Git commit SHA of the buggy version |
| `patch_sha` | Git commit SHA(s) of patches (pipe-separated for multiple) |
| `patched_files` | Files modified in the fix (pipe-separated) |
| `patched_file_types` | File extensions affected (e.g., py, js) |
| `days_to_fix` | Time from bug report to fix |


## Architecture

```
Defects4REST-private/
├── defects4rest/                                               # Main package directory
│   ├── cli.py                                                  # Main CLI entry point
│   ├── data/
│   │   ├── defect_data/                                        # Bug metadata CSV files
│   │   ├── docker_files/                                       # Docker configuration templates
│   │   └── temp_project_data/                                  # Runtime temporary directories
│   └── src/
│       ├── api_dep_setup/                                      # Issue-specific setup hooks
│       ├── command_scripts/                                    # CLI command implementations
│       ├── deployment_scripts/                                 # Project-specific deployers
│       └── utils/                                              # Shared utilities
├── bug_mining_framework/                                       # GitHub issue mining scripts
├── manual_bug_reproduction/                                    # Manual bug reproduction steps
│   └── <project>/                                              # Per-project folders
│       └── <project>#<N>/                                      # Per-issue folders
│           ├── readme.md                                       # Step-by-step reproduction
|           ├── <project>#<issue_number>_buggy_spec.json/yaml   # OpenAPI specification for buggy version
            └── <project>#<issue_number>_patched_spec.json/yaml # OpenAPI specification for patched version
├── pyproject.toml
└── README.md
```

### Component Overview

#### defects4rest/ (Main Package)
- **cli.py**: Command-line interface entry point
- **data/**: Bug metadata, Docker configs
- **src/**: All source code modules
  - **command_scripts/**: CLI command implementations (info, checkout)
  - **deployment_scripts/**: Project-specific deployers
  - **api_dep_setup/**: Issue-specific setup hooks
  - **utils/**: Shared utilities (git, shell, metadata parsing)

#### issue_mining/
Scripts for mining bugs from GitHub repositories.

#### manual_bug_reproduction/
Muanual bug reproduction steps guides with OpenAPI specifications for both buggy and patched versions.

### Deployment Script Interface

Each project deployer must implement three functions:

```python
def main(sha=None, issue_id=None):
    """
    Deploy the project at the specified SHA.

    Args:
        sha: Git commit SHA to checkout (None for latest)
        issue_id: Bug/issue identifier for port allocation
    """
    pass

def stop():
    """Stop running containers without removing volumes."""
    pass

def clean():
    """Remove all containers, volumes, and networks."""
    pass
```

---

## Adding New Projects

## Step 1: Create Bug Metadata CSV

- If you already have a CSV file in the correct format then Skip this step

- If you need to generate the CSV  [`bug_mining_framework/README.md`](bug_mining_framework/README.md)

**CSV format requirements:** Must follow format in [Bug Metadata Format](#bug-metadata-format) 
section above (includes columns: bug_id, issue_no, repo, issue_url, title, description, 
buggy_sha, patch_sha, patched_files, patched_file_types, days_to_fix).


### Step 2: Create Deployment Script

Create a Python file at:
```
defects4rest/src/deployment_scripts/deploy_<project>.py
```

### Step 3: Implement Required Functions

```python
import subprocess
import os

PROJECT_NAME = "your-project"
CONTAINER_NAME = f"{PROJECT_NAME}-container"

def main(sha=None, issue_id=None):
    """Deploy the project."""
    # 1. Clone or update repository
    # 2. Checkout specified SHA
    # 3. Build Docker image
    # 4. Start containers
    pass

def stop():
    """Stop containers."""
    subprocess.run(["docker", "stop", CONTAINER_NAME])

def clean():
    """Full cleanup."""
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME])
    subprocess.run(["docker", "volume", "prune", "-f"])
```

### Step 4: (Optional) Add Setup Hooks

For issues requiring test data initialization, create:
```
defects4rest/src/api_dep_setup/<project>.py
```

```python
def issue_1():
    """Setup hook for issue #1."""
    # Create test data, initialize database, etc.
    pass
```

### Step 5: Test Your Integration

```bash
# Test info command
defects4rest info -p your-project -i 1

# Test deployment
defects4rest checkout -p your-project -i 1 --buggy --start

# Test cleanup
defects4rest checkout -p your-project -i 1 --clean
```

### Step 6: Add Bug Reproduction Steps

Create manual reproduction guides for each bug:
```
manual_bug_reproduction/<project>/<project>#<issue_number>/
├── readme.md                                       # Step-by-step reproduction instructions
├── <project>#<issue_number>_buggy_spec.json/yaml   # OpenAPI specification for buggy version
└── <project>#<issue_number>_patched_spec.json/yaml # OpenAPI specification for patched version
```

Example: `manual_bug_reproduction/netbox/netbox#18991/`

Each readme.md should include:
- Description
- GitHub Issue URL
- Triggering Endpoints
- Triggering Behavior
- Expected vs actual behavior


# Contributing

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

### Component Overview

#### `defects4rest/`
- `cli.py`: Command-line interface entry point
- `data/`: Bug metadata, Docker configs
- `src/`: All source code modules
  - `command_scripts/`: CLI command implementations (info, checkout)
  - `deployment_scripts/`: Project-specific deployers
  - `api_dep_setup/`: Issue-specific setup hooks
  - `utils/`: Shared utilities (git, shell, metadata parsing)

#### `issue_mining/`
Scripts for mining bugs from GitHub repositories.

#### `manual_bug_reproduction/`
Manual bug reproduction steps guides with OpenAPI specifications for both buggy and patched versions.

## Adding new projects

### Step 1: Create Bug Metadata CSV

- If you already have a CSV file in the correct format then Skip this step

- If you need to generate the CSV  [`bug_mining_framework/README.md`](bug_mining_framework/README.md)

**CSV format requirements:** Must follow format in Bug Metadata Format explained above.


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

# Each project deployer must implement three functions:
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

### Step 4: Add Setup Hooks (if required)

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

Example: [netbox#18991](manual_bug_reproduction/netbox/netbox#18991/README.md)

Each readme.md should include:
- Description
- GitHub Issue URL
- Triggering Endpoints
- Triggering Behavior
- Expected vs actual behavior
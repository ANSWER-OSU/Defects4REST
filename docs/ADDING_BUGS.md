# Adding New Bugs to Defects4REST

This guide provides detailed step-by-step instructions for adding new bugs to the Defects4REST framework, either for existing projects or entirely new projects.

## Overview

Adding a new bug to Defects4REST involves three main components:

1. **CSV Metadata** — Bug information in the project's CSV file
2. **Bug Documentation** — README with reproduction steps
3. **Deployment Support** — Ensuring the deployment script supports the bug's version

### Directory Structure

```
Defects4REST/
├── defects4rest/
│   └── data/
│       └── defect_data/
│           └── <project>_info.csv    # Bug metadata
├── bug_replication/
│   └── <project>/
│       ├── README.md                  # Project overview
│       └── <project>#<issue>/
│           └── README.md              # Bug reproduction steps
└── defects4rest/
    └── src/
        └── deployment_scripts/
            └── deploy_<project>.py    # Deployment script
```

---

## Adding Bugs to Existing Projects

### Step 1: Update the CSV File

Add a new row to the project's CSV file at:
`defects4rest/data/defect_data/<project>_info.csv`

#### CSV Columns

```csv
bug_id,issue_no,repo,issue_url,title,description,patched_file_types,text_for_topic_modeling,prediction,confidence,buggy_sha,patch_sha,patched_files,days_to_fix,buggy_docker_version,patched_docker_version
```

#### Example Row

```csv
7,18363,netbox,https://github.com/netbox-community/netbox/issues/18363,cant create vm mac-address via api,"API POST request to create a MAC address fails with a 400 error",source-file|test-file,"mac address api validation error",bug,0.95,9a1d9365cd7c703413ca8d15c0b8b737067c275e,636148f9654b82f7e664645f3e781a4591a22132,netbox/dcim/api/serializers.py|netbox/dcim/tests/test_api.py,3,v4.2.1,v4.2.2
```

### Step 2: Create Bug Documentation

Create the bug directory and README:

```bash
mkdir -p bug_replication/<project>/<project>#<issue_no>
```

Create `bug_replication/<project>/<project>#<issue_no>/README.md` with the following sections:

| Section | Description |
|---------|-------------|
| Description | Brief description of the bug |
| GitHub Issue URL | Link to the original issue |
| Triggering Endpoints | List of affected API endpoints |
| Triggering Behavior | Step-by-step reproduction with curl commands |
| Buggy Response | HTTP status code and response body |
| Expected Response | What the correct response should be |

See existing bug READMEs for examples: [netbox#18363](../bug_replication/netbox/netbox%2318363/README.md)

### Step 3: Add OpenAPI Specification

Create the OpenAPI spec at:

```
bug_replication/<project>/<project>#<issue_no>/<project>#<issue_no>_spec.json/yaml
```

### Step 4: Update Project README

Add the new bug to the Available Defects table in `bug_replication/<project>/README.md`.

---

## Adding a New Project

### Step 1: Evaluate Project Suitability

Ensure the project:

- Has a REST API
- Is open-source with public issue tracker
- Has documented API bugs

### Step 2: Create Bug Metadata CSV

- If you already have a CSV file in the correct format, skip this step
- If you need to generate the CSV, see [`bug_mining_framework/README.md`](../bug_mining_framework/README.md)

**CSV format requirements:** Must follow the format in [Bug Metadata Format](#bug-metadata-format) explained above.

### Step 3: Create Project Structure

```bash
# Create directories
mkdir -p bug_replication/<project>
mkdir -p defects4rest/data/defect_data
```

### Step 4: Create CSV File

Place the CSV file at `defects4rest/data/defect_data/<project>_info.csv`

### Step 5: Create Deployment Script

Create `defects4rest/src/deployment_scripts/deploy_<project>.py`:

```python
"""
<Project Name> Deployment Script

Deploys <Project Name> at specific git commits for bug reproduction.
"""
import subprocess
import os
import sys
from defects4rest.src.utils.shell import run, pretty_step, pretty_section
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq
from defects4rest.src.utils.git import get_default_branch, sha_exists

REPO_URL = "https://github.com/<org>/<repo>.git"
PROJECT_NAME = '<project>'
PROJECT_DIR = str(ensure_temp_project_dir(PROJECT_NAME))
CONTAINER_NAME = "<project>-container"
HOST_PORT = "8080"

def main(sha=None, issue_id=None):
    """Main deployment function."""
    pretty_section(f"Deploying {PROJECT_NAME} (issue #{issue_id}) at SHA: {sha}")

    # Check prerequisites
    for tool in ("git", "docker"):
        check_prereq(tool)

    # Clone repository
    if os.path.isdir(PROJECT_DIR):
        pretty_step(f"Removing existing repo at {PROJECT_DIR}")
        shutil.rmtree(PROJECT_DIR)

    run(["git", "clone", REPO_URL, PROJECT_DIR])
    os.chdir(PROJECT_DIR)

    # Checkout specific SHA
    if sha and sha != "latest":
        if not sha_exists(sha):
            run(["git", "fetch", "--all", "--tags"])
        run(["git", "checkout", sha])

    # Build and deploy (customize for your project)
    # Example: Docker Compose
    run(["docker-compose", "up", "-d"])

    pretty_section(f"{PROJECT_NAME} is ready at http://localhost:{HOST_PORT}")

def stop():
    """Stop containers."""
    pretty_section(f"Stopping {PROJECT_NAME}...")
    run(["docker-compose", "down"], cwd=PROJECT_DIR)

def clean():
    """Clean up deployment."""
    pretty_section(f"Cleaning {PROJECT_NAME}...")
    run(["docker-compose", "down", "-v", "--remove-orphans"], cwd=PROJECT_DIR)
```

### Step 6: Create Project README

Create `bug_replication/<project>/README.md` with the following sections:

| Section | Description |
|---------|-------------|
| Overview | Brief description of the project |
| Available Defects | Table with Issue ID, Defect Type, Sub Defect Type, Description, Replication link |
| Deploying, Managing, and Inspecting | CLI commands for checkout, stop, clean, info |
| Accessing | Base URL, authentication details |
| Troubleshooting | Docker logs command |
| References | Links to project GitHub and documentation |

See existing project READMEs for examples: [netbox](../bug_replication/netbox/README.md)

### Step 7: Register the Project

Update the main README.md to include your project in the Supported Projects table.

---

## Bug Documentation Format

### Defect Type Categories

Use these standardized categories:

| Defect Type | Sub Defect Type |
|-------------|-----------------|
| **Configuration and Environment Issues (T1)** | Container and Resource Quota Handling Errors (ST1) |
| | Job Execution and Workflow Configuration Defects (ST2) |
| | Environment-Specific Behavior and Configuration Bugs (ST3) |
| **Data Validation and Query Processing Errors (T2)** | Schema and Payload Validation Errors in POST APIs (ST4) |
| | Query Filter and Search Parameter Handling Errors (ST5) |
| **Authentication, Authorization, and Session Management Issues (T3)** | Authentication and Token Management Errors (ST6) |
| | Session, Token, and Account Lifecycle Management Errors (ST7) |
| **Integration, Middleware, and Runtime Environment Failures (T4)** | Middleware Integration Failures in REST APIs (ST8) |
| | Process Signal and Grouping Issues in Containerized APIs (ST9) |
| | Runtime and Dependency Errors (ST10) |
| **Data Storage, Access, and Volume Errors (T5)** | Volume and File Upload/Access Errors (ST11) |
| | Database/Table User Access Handling Errors (ST12) |
| **Distributed Systems and Cluster Failures (T6)** | Index and Cluster Coordination Failures (ST13) |

### Patched File Types

| Type | Description |
|------|-------------|
| `source-file` | Main application code |
| `test-file` | Test files |
| `config-file` | Configuration files |
| `build-file` | Build scripts (Makefile, pom.xml) |
| `doc-file` | Documentation |
| `other-file` | Other files |

---

## Testing Your Addition

### 1. Verify CSV Entry

```bash
defects4rest info -p <project> -i <issue>
```

Should display all bug information correctly.

### 2. Test Buggy Deployment

```bash
defects4rest checkout -p <project> -i <issue> --buggy
```

Then reproduce the bug using the curl commands in your README.

### 3. Test Patched Deployment

```bash
defects4rest checkout -p <project> -i <issue> --patched
```

Verify the bug is fixed.

### 4. Test Cleanup

```bash
defects4rest checkout -p <project> -i <issue> --clean
```

Verify all containers and volumes are removed.

---

## Checklist

Before submitting your addition, verify:

### CSV File
- [ ] All required columns are filled
- [ ] `buggy_sha` points to a commit before the fix
- [ ] `patch_sha` points to the fix commit(s)
- [ ] `patched_files` lists all modified files
- [ ] `patched_file_types` uses standard categories

### Bug README
- [ ] Description clearly explains the bug
- [ ] GitHub issue URL is correct
- [ ] Triggering endpoints are listed
- [ ] Step-by-step reproduction with curl commands
- [ ] Buggy response is documented
- [ ] Expected response is documented

### Project README (if new project)
- [ ] Overview describes the project
- [ ] Available Defects table is complete
- [ ] Deployment commands are documented
- [ ] Access credentials are documented
- [ ] Troubleshooting section exists

### Deployment Script (if new project)
- [ ] `main(sha, issue_id)` function implemented
- [ ] `stop()` function implemented
- [ ] `clean()` function implemented
- [ ] Handles both buggy and patched deployments

### Testing
- [ ] `defects4rest info` shows correct information
- [ ] Buggy version deploys and bug is reproducible
- [ ] Patched version deploys and bug is fixed
- [ ] Cleanup removes all resources

---

## Getting Help

If you need help adding a new bug:

1. Check existing bug READMEs for examples
2. Review deployment scripts for similar projects
3. Open an issue on GitHub with questions

## See Also

- [Main README](../README.md)

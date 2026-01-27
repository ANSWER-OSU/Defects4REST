# Adding New Bugs to Defects4REST

This document describes the process of adding new bugs to Defects4REST. The process involves mining bugs from GitHub, collecting metadata, and creating the necessary deployment and documentation files.

## Overview

Adding bugs to Defects4REST consists of the following high-level steps:

1. **Mine bugs** from GitHub using the bug mining framework
2. **Filter** for REST API bugs (manually or using GPT-4)
3. **Create deployment script** (for new projects only)
4. **Document reproduction steps** for each bug
5. **Add OpenAPI specifications** for affected endpoints
6. **Verify** bugs are reproducible

The [Bug Mining Framework](../bug_mining_framework/README.md) automates steps 1-2 by extracting bug data from GitHub repositories and generating CSV files compatible with Defects4REST.

---

## Bug Requirements

Each bug in Defects4REST must satisfy the following criteria:

| Criterion | Description |
|-----------|-------------|
| REST API related | The bug affects REST API behavior (responses, validation, authentication) |
| Reproducible | The bug can be triggered via HTTP requests |
| Issue tracked | The bug has an associated issue in the project's issue tracker |
| Fix available | A patch commit exists in the repository |

---

## Adding Bugs to Existing Projects

For projects already in Defects4REST, follow these steps:

1. **Mine bugs** using the Bug Mining Framework (see [Step 1](#step-1-mine-bugs-from-github))
2. **Filter** for REST API bugs (see [Step 2](#step-2-filter-for-rest-api-bugs))
3. **Append** new bugs to the existing CSV (see [Step 3](#step-3-add-csv-to-defects4rest))
4. **Document** reproduction steps for each bug (see [Step 5](#step-5-document-reproduction-steps))
5. **Add** OpenAPI specifications (see [Step 6](#step-6-add-openapi-specification))
6. **Update** the project README table (see [Step 7](#step-7-update-project-readme))
7. **Verify** bugs are reproducible (see [Step 8](#step-8-verify-the-bug))

**Note:** Do not manually add rows to the CSV. Always use the bug mining framework to ensure correct commit SHAs and metadata.

---

## Adding a New Project

For new projects not yet in Defects4REST, follow all steps below including creating a deployment script.

---

## Step 1: Mine Bugs from GitHub

Use the Bug Mining Framework to automatically extract bug data from GitHub repositories.

### Quick Start

```bash
cd bug_mining_framework

# Install dependencies
pip install -r requirements.txt

# Run the mining tool
python3 github_issue_processor.py \
  --repo-url "https://github.com/owner/repo" \
  --token "YOUR_GITHUB_TOKEN" \
  --resultpath "./results"
```

### Output Files

The tool generates:

```
results/issues_xml/<repo>/
├── <repo>_Issue123.xml           # Individual bug records (XML)
├── <repo>_Issue124.xml
├── AAAmastertracker_<repo>.csv   # Index of all processed issues
└── <repo>_info.csv               # CSV for Defects4REST
```

For detailed instructions, see [Bug Mining Framework README](../bug_mining_framework/README.md).

---

## Step 2: Filter for REST API Bugs

The mining tool extracts **all** bugs. You must filter for REST API bugs.

### Option A: Manual Filtering

1. Open the generated CSV:
   ```bash
   open ./results/issues_xml/<repo>/<repo>_info.csv
   ```

2. Review `title` and `description` columns

3. Delete rows that are not REST API bugs

4. Save the filtered file

### Option B: GPT-4 Classification

Use automated classification (requires OpenAI API key):

```bash
python classify_rest_api_bugs.py ./results/issues_xml/<repo>/
```

This produces `rest_api_issues.csv` containing only high-confidence REST API bugs.

---

## Step 3: Add CSV to Defects4REST

### For New Projects

Copy the filtered CSV to the Defects4REST data directory:

```bash
cp ./results/issues_xml/<repo>/<repo>_info.csv \
   ../defects4rest/data/defect_data/<repo>_info.csv
```

### For Existing Projects

If the project already exists in Defects4REST, append the new bugs to the existing CSV:

1. Open both CSVs (existing and newly mined)
2. Copy new rows from the mined CSV
3. Append to the existing CSV
4. Update `bug_id` values to continue the sequence

**Note:** Always use the bug mining framework to extract bug metadata. Do not manually add rows to the CSV — the mining tool ensures correct commit SHAs and patched file information.

### CSV Schema

| Column | Description |
|--------|-------------|
| `bug_id` | Unique identifier (auto-increment) |
| `issue_no` | GitHub issue number |
| `repo` | Repository name |
| `issue_url` | Full URL to the issue |
| `title` | Issue title |
| `description` | Issue description |
| `buggy_sha` | Commit hash containing the bug |
| `patch_sha` | Commit hash(es) of the fix (pipe-separated) |
| `patched_files` | Files modified (pipe-separated) |
| `patched_file_types` | File type categories (pipe-separated) |
| `days_to_fix` | Days between issue creation and fix |
| `buggy_docker_version` | Docker Hub image tag for buggy version (optional) |
| `patched_docker_version` | Docker Hub image tag for patched version (optional) |

### Docker Hub Deployment (Optional)

Some projects publish Docker images to Docker Hub. For these projects, you can specify `buggy_docker_version` and `patched_docker_version` columns with the image tags. This allows Defects4REST to pull pre-built images instead of building from git commits, simplifying deployment.

---

## Step 4: Create Deployment Script (New Projects Only)

If adding bugs to a **new project**, create a deployment script at:

```
defects4rest/src/deployment_scripts/deploy_<project>.py
```

### Required Functions

The script must implement three functions:

| Function | Purpose |
|----------|---------|
| `main(sha, issue_id)` | Clone repo, checkout SHA, build and start containers |
| `stop()` | Stop containers without removing volumes |
| `clean()` | Stop containers and remove all resources |

### Example Structure

```python
def main(sha=None, issue_id=None):
    """Deploy the project at the specified commit."""
    # 1. Clone repository (or pull if exists)
    # 2. Checkout the specified SHA
    # 3. Build and start Docker containers
    # 4. Wait for service to be ready
    pass

def stop():
    """Stop running containers."""
    pass

def clean():
    """Remove all containers, volumes, and networks."""
    pass
```

See existing scripts for reference:
- `deploy_netbox.py`
- `deploy_mastodon.py`
- `deploy_dolibarr.py`

---

## Step 5: Document Reproduction Steps

For each bug, create documentation at:

```
bug_replication/<project>/<project>#<issue>/README.md
```

### Required Sections

| Section | Content |
|---------|---------|
| Description | What the bug is and its impact |
| GitHub Issue URL | Link to the original issue |
| Triggering Endpoints | List of affected API endpoints |
| Triggering Behavior | Step-by-step curl commands to reproduce |
| Buggy Response | HTTP status and response when bug is present |
| Expected Response | Correct HTTP status and response |

### Writing Guidelines

- Include **exact curl commands** that can be copy-pasted
- Document any **prerequisites** (test data, tokens)
- Show **actual response bodies** (not just status codes)
- Enable someone **unfamiliar with the project** to reproduce the bug

See existing documentation: [netbox#18363](../bug_replication/netbox/netbox%2318363/README.md)

---

## Step 6: Add OpenAPI Specification

Create an OpenAPI spec at:

```
bug_replication/<project>/<project>#<issue>/<project>#<issue>_spec.json
```

Or YAML format:
```
bug_replication/<project>/<project>#<issue>/<project>#<issue>_spec.yaml
```

The specification should describe the endpoints relevant to reproducing the bug.

---

## Step 7: Update Project README

Add the new bug to the "Available Defects" table in:

```
bug_replication/<project>/README.md
```

For new projects, create this README following existing examples: [netbox/README.md](../bug_replication/netbox/README.md)

---

## Step 8: Verify the Bug

Test that the bug is reproducible:

```bash
# Verify metadata
defects4rest info -p <project> -i <issue>

# Deploy buggy version
defects4rest checkout -p <project> -i <issue> --buggy --start

# Run reproduction steps from your README
# Bug should be present

# Deploy patched version
defects4rest checkout -p <project> -i <issue> --patched --start

# Run same steps
# Bug should be fixed

# Cleanup
defects4rest checkout -p <project> -i <issue> --clean
```

---

## Directory Structure

```
Defects4REST/
├── defects4rest/
│   ├── data/defect_data/
│   │   └── <project>_info.csv          # Bug metadata CSV
│   └── src/deployment_scripts/
│       └── deploy_<project>.py         # Deployment automation
│
├── bug_replication/
│   └── <project>/
│       ├── README.md                    # Project overview
│       └── <project>#<issue>/
│           ├── README.md                # Reproduction steps
│           └── <project>#<issue>_spec.json  # OpenAPI spec
│
└── bug_mining_framework/
    ├── github_issue_processor.py        # Main mining script
    ├── launch_minebugs.sh               # Batch processing
    └── mine_bugs.sh                     # SLURM wrapper
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Deployment fails | Check Docker logs: `docker logs <container>` |
| Bug not reproducible | Verify correct SHA and any required setup |
| CSV not loading | Check file path and column format |
| Service won't start | Check port conflicts: `docker ps` |

---

## See Also

- [Bug Mining Framework](../bug_mining_framework/README.md) — Automated bug extraction from GitHub
- [Main README](../README.md) — Project overview and usage

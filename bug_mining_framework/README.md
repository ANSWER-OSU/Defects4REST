# Bug Mining Framework

This framework automatically extracts bug data from GitHub repositories and generates CSV datasets compatible with Defects4REST. The tool fetches closed issues, identifies associated commits, and produces structured metadata for each bug.

## Overview

The bug mining process consists of the following steps:

1. **Extract** all closed issues from a GitHub repository
2. **Identify** commits that fix each issue (patch commits)
3. **Derive** the buggy commit (parent of the first patch commit)
4. **Generate** CSV and XML files with bug metadata
5. **Filter** for REST API bugs (manually or using GPT-4)

The output CSV can be directly used with Defects4REST after filtering for REST API bugs.

---

## Prerequisites

| Requirement | Description |
|-------------|-------------|
| Python 3.x | Required for running the mining script |
| GitHub Token | Personal access token with `repo` scope |
| Dependencies | `requests` (install via requirements.txt) |

### Getting a GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: `Bug Mining Tool`
4. Select scope: `repo`
5. Click "Generate token"
6. Copy the token (you won't see it again)

---

## Installation

```bash
cd bug_mining_framework

# Install dependencies
pip install -r requirements.txt

# Make scripts executable (Linux/macOS)
chmod +x mine_bugs.sh launch_minebugs.sh
```

---

## Usage

### Single Repository

```bash
python3 github_issue_processor.py \
  --repo-url "https://github.com/owner/repo" \
  --token "YOUR_GITHUB_TOKEN" \
  --resultpath "./results"
```

**Example using `restcountries` repository:**
Replace the repository URL with the repository you want to mine bugs from.

```bash
python3 github_issue_processor.py \
  --repo-url "https://github.com/apilayer/restcountries" \
  --token "github_pat_11AQT..." \
  --resultpath "./results"
```

### Multiple Repositories

For batch processing, edit `launch_minebugs.sh`:

1. Add repositories to the `REPOS` array:
   ```bash
   REPO_URL=(
       "https://github.com/apilayer/restcountries"
       "https://github.com/strapi/strapi"
   )
   ```

2. Set your token:
   ```bash
   GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"
   ```

3. Run:
   ```bash
   bash launch_minebugs.sh
   ```

---

## Output

The tool generates the following files for each repository:

```
results/issues_xml/<repo>/
├── <repo>_Issue123.xml           # Individual bug record (XML)
├── <repo>_Issue124.xml
├── AAAmastertracker_<repo>.csv   # Index of processed issues
└── <repo>_info.csv               # CSV for Defects4REST
```

### CSV Schema

| Column | Description | Example |
|--------|-------------|---------|
| `bug_id` | Auto-incremented identifier | `1`, `2`, `3` |
| `issue_no` | GitHub issue number | `12345` |
| `repo` | Repository URL | `https://github.com/owner/repo` |
| `issue_url` | Direct link to issue | `https://github.com/owner/repo/issues/12345` |
| `title` | Issue title | `Fix null pointer exception` |
| `description` | Issue description | `Users reported crashes...` |
| `buggy_sha` | Commit SHA before fix | `abc123def456...` |
| `patch_sha` | Fix commit SHA(s), pipe-separated | `def456\|ghi789` |
| `patched_files` | Modified files, pipe-separated | `src/main.py\|tests/test.py` |
| `patched_file_types` | File extensions | `py\|js\|md` |
| `days_to_fix` | Days from issue open to close | `7` |
| `buggy_docker_version` | Docker Hub image tag for buggy version (optional) | `v4.2.1` |
| `patched_docker_version` | Docker Hub image tag for patched version (optional) | `v4.2.2` |

**Note:** Some projects use Docker Hub images instead of building from source. For these projects, `buggy_docker_version` and `patched_docker_version` specify the image tags to pull, eliminating the need to build from git commits.

---

## Filtering for REST API Bugs

The mining tool extracts **all** bugs from a repository. You must filter for REST API bugs before using the data with Defects4REST.

### Option A: Manual Filtering

1. Open the CSV:
   ```bash
   open ./results/issues_xml/<repo>/<repo>_info.csv
   ```

2. Review `title` and `description` columns

3. Delete rows that are not REST API bugs

4. Save the file

5. Copy to Defects4REST:
   ```bash
   cp ./results/issues_xml/<repo>/<repo>_info.csv \
      ../defects4rest/data/defect_data/<repo>_info.csv
   ```

### Option B: GPT-4 Classification

Automatically classify bugs using OpenAI's API.

**Warning:** This option incurs API costs.

1. Install dependencies:
   ```bash
   pip install openai pandas
   ```

2. Get an OpenAI API key from https://platform.openai.com/api-keys

3. Edit `classify_rest_api_bugs.py`:
   ```python
   client = OpenAI(api_key="sk-proj-YOUR_KEY_HERE")
   ```

4. Run classification:
   ```bash
   python classify_rest_api_bugs.py ./results/issues_xml/<repo>/
   ```

5. Copy filtered results:
   ```bash
   cp rest_api_issues.csv ../defects4rest/data/defect_data/<repo>_info.csv
   ```

---

## Complete Workflow Example

```bash
# 1. Extract bugs from repository
python3 github_issue_processor.py \
  --repo-url "https://github.com/strapi/strapi" \
  --token "github_pat_..." \
  --resultpath "./results"

# 2. Filter for REST API bugs (manual or GPT-4)
open ./results/issues_xml/strapi/strapi_info.csv
# Delete non-REST API bugs and save

# 3. Copy to Defects4REST
cp ./results/issues_xml/strapi/strapi_info.csv \
   ../defects4rest/data/defect_data/strapi_info.csv

# 4. Verify with Defects4REST
defects4rest info -p strapi -i 12345
```

---

## Rate Limiting

The tool automatically handles GitHub API rate limits:

- Detects HTTP 401/HTTP 403 errors
- Saves checkpoint with current progress
- Waits until rate limit resets
- Resumes from checkpoint on restart

No manual intervention is required.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Error 401: Bad credentials | Generate a new token at https://github.com/settings/tokens |
| Error 403: Rate limit | Wait (the script handles this automatically) |
| Permission denied | Run `chmod +x mine_bugs.sh launch_minebugs.sh` |
| No qualifying issues found | Repository has no closed issues with commits — try a different repository |
| ModuleNotFoundError: openai | Run `pip install openai pandas` |

---

## See Also

- [Adding New Bugs](../docs/ADDING_BUGS.md) — Complete guide for adding bugs to Defects4REST
- [Main README](../README.md) — Defects4REST overview and usage

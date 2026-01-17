# GitHub Bug Mining Framework

Automatically extract bug data from GitHub repositories and generate CSV datasets with optional REST API bug classification.

---

## Quick Start Guide

### Step 1: Get a GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: `Bug Mining Tool`
4. Select scope: `repo`
5. Click "Generate token"
6. COPY THE TOKEN (you won't see it again!)


### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Make Scripts Executable

```bash
chmod +x mine_bugs.sh launch_minebugs.sh
```

### Step 4: Run the Tool

You can process repositories in two ways:
- Single repository - Process one repo at a time (good for testing)
- Multiple repositories - Batch process several repos (see [Processing Multiple Repositories](#processing-multiple-repositories) section below.)

**For a single repository:**

```bash
python3 github_issue_processor.py \
  --repo-url "https://github.com/owner/repo" \
  --token "YOUR_GITHUB_TOKEN" \
  --resultpath "./results"
```

**Example:**

```bash
python3 github_issue_processor.py \
  --repo-url "https://github.com/apilayer/restcountries" \
  --token "github_pat_11AQT..." \
  --resultpath "./results"
```


### Step 5: Check Your Output

The tool generates both XML files and CSV like this:

```
results/
└── issues_xml/
    └── restcountries/
        ├── restcountries_Issue123.xml          ← XML files
        ├── restcountries_Issue124.xml
        ├── ...
        ├── AAAmastertracker_restcountries.csv  ← XML tracker
        └── restcountries_info.csv              ← CSV for Defects4REST 
```


## Step 6: Filter REST API Bugs (Choose One)

**Important:** The tool extracts ALL bugs for the given repo. You need to filter for REST API bugs.

### Option A: Manual Filtering 

**1.** Open the CSV:
   ```bash
   open ./results/issues_xml/<repo>/<repo>_info.csv
   ```

**2.** Review and filter:
   - Read `title` and `description` columns
   - Delete non-REST API bugs
   - Save the file

**3.** Copy to Defects4REST:
   ```bash
   cp ./results/issues_xml/<repo>/<repo>_info.csv \
      ./defects4rest/data/defect_data/<repo>_info.csv
   ```

### Option B: Automated GPT-4 Classification

Use LLM to automatically identify REST API bugs.
**Cost Warning:** This option uses OpenAI's API Key and will incur costs.

**1**. Install additional dependencies:
```bash
pip install openai pandas
```

**2.** Get OpenAI API key:
- Go to https://platform.openai.com/api-keys
- Create and copy your API key

**3.** Update the classification script:

Edit `classify_rest_api_bugs.py`:
```python
client = OpenAI(api_key="sk-proj-YOUR_KEY_HERE")
```

**4.** Run classification:
```bash
python classify_rest_api_bugs.py ./results/issues_xml/<project_name>/
```

**Output:**
- `rest_api_issues.csv` - High-confidence REST API bugs only (≥70%)

**5.** Copy to Defects4REST:

The classification CSV has the same format as the original, so just copy and rename it:

```bash
cp rest_api_issues.csv ./defects4rest/data/defect_data/_info.csv
```

---

## Processing Multiple Repositories
Instead of running the script manually for each repository, you can automate the process to extract bugs from multiple repositories in one go. This is useful when you want to build a dataset from several projects.

**Edit the Batch Script**

**Step 1.** Open `launch_minebugs.sh` in a text editor

**Step 2.** Find the `REPOS` array (line 4):
   ```bash
   REPOS=(
       "https://github.com/apilayer/restcountries"
   )
   ```

**Step 3.** Add your repositories:
   ```bash
   REPOS=(
       "https://github.com/apilayer/restcountries"
       "https://github.com/strapi/strapi"
       "https://github.com/supabase/supabase"
   )
   ```

**Step 4.** Update your token (line 51):
   ```bash
   GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"
   ```

**Step 5.** Save and run:
   ```bash
   bash launch_minebugs.sh
   ```

---

## Output Format

### Files Generated

For each repository:

```
results/issues_xml/<repo>/
├── <repo>_Issue123.xml                  ← Individual bug XML files
├── <repo>_Issue124.xml
├── AAAmastertracker_<repo>.csv          ← XML file tracker
└── <repo>_info.csv                      ← Defects4REST CSV 
```

### CSV Columns

| Column | Description | Example |
|--------|-------------|---------|
| `bug_id` | Internal bug ID (auto-increment) | `1`, `2`, `3` |
| `issue_no` | GitHub issue number | `12345` |
| `repo` | Repository URL | `https://github.com/owner/repo` |
| `issue_url` | Direct link to issue | `https://github.com/owner/repo/issues/12345` |
| `title` | Bug title | `Fix null pointer exception` |
| `description` | Bug description | `Users reported crashes...` |
| `buggy_sha` | Commit SHA before fix | `abc123def456...` |
| `patch_sha` | Fix commit SHA(s), pipe-separated | `def456\|ghi789` |
| `patched_files` | Modified files, pipe-separated | `src/main.py\|tests/test.py` |
| `patched_file_types` | File extensions | `py\|js\|md` |
| `days_to_fix` | Days from open to close | `7` |

---

## Complete Workflow Examples

### Example 1: Manual Filtering (Simple)

```bash
# Extract bugs
python3 github_issue_processor.py \
  --repo-url "https://github.com/strapi/strapi" \
  --token "github_pat_..." \
  --resultpath "./results"

# Manual filtering
open ./results/issues_xml/strapi/strapi_info.csv
# Delete non-REST API bugs and save

# Copy to Defects4REST
cp ./results/issues_xml/strapi/strapi_info.csv \
   ./defects4rest/data/defect_data/strapi_info.csv

# Use with Defects4REST
defects4rest info -p strapi -i 12345
```

---

### Example 2: GPT-4 Classification (Automated)

```bash
# Extract bugs
python3 github_issue_processor.py \
  --repo-url "https://github.com/strapi/strapi" \
  --token "github_pat_..." \
  --resultpath "./results"

# GPT-4 classification
python classify_rest_api_bugs.py ./results/issues_xml/strapi/

# Copy filtered bugs to Defects4REST
cp rest_api_issues.csv ./defects4rest/data/defect_data/strapi_info.csv

# Use with Defects4REST
defects4rest info -p strapi -i 12345
```

---

## Common Issues

### "Error 401: Bad credentials"

**Problem:** Invalid GitHub token

**Solution:** Generate a new token at https://github.com/settings/tokens


### "Error 403: Rate limit"

**Problem:** Too many API requests

**Solution:** Wait (the script handles this automatically)


### "Permission denied"

**Problem:** Scripts aren't executable

**Solution:**
```bash
chmod +x mine_bugs.sh launch_minebugs.sh
```

### "No qualifying issues found"

**Problem:** Repository has no closed issues with commits

**Solution:** This is normal - try a different repository


### "ModuleNotFoundError: No module named 'openai'"

**Problem:** Missing dependencies for classification

**Solution:**
```bash
pip install openai pandas
```

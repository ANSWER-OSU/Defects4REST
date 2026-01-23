## awx#7243

## Description


Unauthenticated GET request returns 500 instead of expected 401 indicating improper authentication error handling.


## GitHub Issue URL

[
https://github.com/ansible/awx/issues/7243
](
https://github.com/ansible/awx/issues/7243
)

## Triggering Endpoints:

* `/api/v2/workflow_job_templates`
* `/api/v2/workflow_job_templates/{id}/workflow_nodes/`
* `/api/v2/workflow_job_template_nodes/{id}/create_approval_template/`


## Triggering Behavior:

**Step 1.** Create a new Workflow Job Template

```bash
curl -s -X POST "http://localhost:8052/api/v2/workflow_job_templates/" \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Workflow 7243","organization":1}'
```

**Response:** JSON response containing a workflow ID (e.g., "id": 433)

**Step 2.** Create a Workflow Node

```bash
curl -s -X POST "http://localhost:8052/api/v2/workflow_job_templates/433/workflow_nodes/" \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d "{\"workflow_job_template\":1}"
```

**Response:** JSON with the node ID (e.g., "id": 12)

**Step 3.** Test without Authentication

```bash
curl -v "http://localhost:8052/api/v2/workflow_job_template_nodes/12/create_approval_template/"
```

**Buggy Response:** HTTP/1.1 500 Internal Server Error

**Expected Response:** HTTP 401 Unauthorized

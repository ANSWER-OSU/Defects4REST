# **awx#8305**

 
## Description
Deleting a workflow approval via the API results in a 500 error due to a backend workflow handling issue after the approval step is completed.
## GitHub Issue URL
https://github.com/ansible/awx/issues/8305
## Triggering Endpoints

 - /api/v2/workflow_job_templates/
 - /api/v2/workflow_job_templates/{id}/workflow_nodes/
 - api/v2/workflow_job_templates/{id}/launch/
 - /api/v2/workflow_approvals/{id}/approve/
 - /api/v2/workflow_approvals/
 - /api/v2/workflow_approvals/{id}/

## Triggering Behavior

**Step 1.** Create a Workflow Template with Approval Step

```
curl -X POST http://localhost/api/v2/organizations/ \
  -u admin:password \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test Org", "description": "Test organization"}'
```
Response: `201 Created` with organization ID (e.g., `"id": 2`)



**Step 2.** Create a Workflow Template 

```bash
curl -X POST http://localhost/api/v2/workflow_job_templates/ \
  -u admin:password \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test Workflow", "organization": 2}'
```

**Response:** `201 Created` with workflow template ID (e.g., `"id": 8`)


**Step 3.** Create a Workflow Node

```bash
curl -X POST http://localhost/api/v2/workflow_job_templates/8/workflow_nodes/ \
  -u admin:password \
  -H 'Content-Type: application/json' \
  -d '{"unified_job_template": null}'
```

**Response:** `201 Created` with node ID (e.g., `"id": 1`)


**Step 4.** Create an Approval Template for the Node

```bash
curl -X POST http://localhost/api/v2/workflow_job_template_nodes/1/create_approval_template/ \
  -u admin:password \
  -H 'Content-Type: application/json' \
  -d '{"name": "Approval Step", "description": "Requires approval", "timeout": 0}'
```

**Response:** `201 Created` with approval template ID (e.g., `"id": 9`)

**Step 5.** Launch the Workflow

```bash
curl -X POST http://localhost/api/v2/workflow_job_templates/8/launch/ \
  -u admin:password \
  -H 'Content-Type: application/json'
```

**Response:** `201 Created` with workflow job ID (e.g., `"id": 1`)

**Step 6.** Wait and Get the Workflow Approval ID

```bash
# Wait a 5 seconds for the approval to be created
# List workflow approvals
curl -s -u admin:password http://localhost/api/v2/workflow_approvals/ | python3 -m json.tool
```

**Expected Response:** List of approvals with ID (e.g., `"id": 2`)

**Step 7.** Approve the Workflow Approval

```bash
curl -X POST http://localhost/api/v2/workflow_approvals/2/approve/ \
  -u admin:password \
  -H 'Content-Type: application/json'
```

**Response:** `204 No Content` or `400` if already approved



**Step 9.** DELETE the Workflow Approval (BUG TRIGGER)

```bash
curl -X DELETE http://localhost/api/v2/workflow_approvals/2/ \
  -u admin:password \
  -w "\nHTTP Status: %{http_code}\n"
```


## Buggy Response
HTTP 500 Internal Server Error with body 

    {
      "detail": "Internal Server Error"
    }

## Expected Response:
HTTP 204 No Content


## Flowable-engine#1939

## Description

API rejects the `likeIgnoreCase` operation for task variable queries, indicating unsupported or inconsistent query parameter handling.

## GitHub Issue URL

[https://github.com/flowable/flowable-engine/issues/1939](https://github.com/flowable/flowable-engine/issues/1939)

## Triggering Endpoints:

* `/flowable-rest/service/query/tasks`

## Triggering Behavior:

**Step 1.** Query tasks including both task and process variables, attempting to use `likeIgnoreCase` on a task variable:

```bash
curl -u "rest-admin:test" \
  -X POST 'http://localhost:8080/flowable-rest/service/query/tasks' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
        "includeTaskLocalVariables": true, 
        "includeProcessVariables": true, 
        "taskVariables": [
          {"name": "var_2","value": "%Cd","operation": "likeIgnoreCase"} 
        ]
      }' | jq
```

**Buggy Response:** HTTP 400 rejects the `likeIgnoreCase` operation for task variables

```json
{
  "message": "Bad request",
  "exception": "Unsupported variable query operation: LIKE_IGNORE_CASE"
}
```

**Expected Response:** HTTP 200 with uniform behavior across variables

```json
{
  "data": [],
  "total": 0,
  "start": 0,
  "sort": "id",
  "order": "asc",
  "size": 0
}
```


## Flowable-engine#3856

## Description

The REST API fails to serialize UUID variable types due to a missing converter in the backend integration logic, resulting in null values in the response.

## GitHub Issue URL

[https://github.com/flowable/flowable-engine/issues/3856](https://github.com/flowable/flowable-engine/issues/3856)

## Triggering Endpoints:

* `/runtime/process-instances`
* `/query/historic-variable-instances`

## Triggering Behavior:

**Step 1.** Start a process with variable `"animalId"` of type UUID and assign it a value:

```bash
curl -u rest-admin:test -X POST \
  http://localhost:8080/flowable-rest/service/runtime/process-instances \
  -H "Content-Type: application/json" \
  -d '{
        "processDefinitionKey": "uuidProcess",
        "variables": [
          {
            "name": "animalId",
            "type": "uuid",
            "value": "201d919d-9974-4813-8628-ae815f311678"
          }
        ]
      }'
```

**Step 2.** Query historic variable instances for the created variable:

```bash
curl -u rest-admin:test -X POST \
  http://localhost:8080/flowable-rest/service/query/historic-variable-instances \
  -H "Content-Type: application/json" \
  -d '{
        "variableName": "animalId"
      }' | jq .
```

**Buggy Response:** HTTP 200 showing null value

```json
{
  "variable": {
    "name": "animalId",
    "type": "uuid",
    "value": null,   
    "scope": "global"
  }
} 
```

**Expected Response:** HTTP 200 showing the assigned value

```json
{
  "variable": {
    "name": "animalId",
    "type": "uuid",
    "value": "201d919d-9974-4813-8628-ae815f311678",  
    "scope": "global"
  }
}
```


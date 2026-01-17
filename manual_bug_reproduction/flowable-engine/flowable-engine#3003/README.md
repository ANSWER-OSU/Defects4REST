## Flowable-engine#3003

## Description

API returns incorrect media type for `.form` files, which affects correct file access and handling.

## GitHub Issue URL

[https://github.com/flowable/flowable-engine/issues/3003](https://github.com/flowable/flowable-engine/issues/3003)

## Triggering Endpoints:

* `/app-repository/deployment`
* `/app-repository/deployments/{id}/resources`

## Triggering Behavior:

**Step 1.** Upload to the App Repository to get deployment `{id}`:

```bash
curl -X POST -v -u "rest-admin:test" -F "file=@bug.zip" "http://localhost:8080/flowable-rest/app-repository/deployments"
```

**Response:** HTTP 200 with `{id : 1}` — this deployment `id` will be used in the next step.

**Step 2.** List resources using the deployment id:

```bash
curl -s -u "rest-admin:test" "http://localhost:8080/flowable-rest/app-repository/deployments/1/resources" | jq
```

**Buggy Response:** `.form` has mediaType `"text/xml"` which should be `"application/json"`

```json
[
  {
    "id": "demo.form",
    "name": "demo.form",
    "mediaType": "text/xml"
  },
  {
    "id": "demo.app",
    "name": "demo.app",
    "mediaType": "application/json"
  }
]
```

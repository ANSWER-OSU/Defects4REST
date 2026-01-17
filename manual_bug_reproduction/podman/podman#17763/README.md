# podman#17763

## Description
Podman’s REST API omits the image tag in the /history endpoint response while Docker returns it under the same environment and API version. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/17763

## Triggering Endpoint(s)
- `images/{image_id}/history`

## Triggering Behavior
**Step 1.** Pull an image
```
curl -v -s -X POST "http://127.0.0.1:8082/v1.24/images/create?fromImage=alpine&tag=3.17.2"
```
**Response:** HTTP 200.
```
{"status":"Already exists","progressDetail":{},"id":"63b65145d645"}
{"status":"Pulling fs layer","progressDetail":{},"id":"b2aa39c304c2"}
{"status":"Download complete","progressDetail":{},"id":"b2aa39c304c2"}
{"status":"Download complete","progressDetail":{},"id":"b2aa39c304c2"}
```

**Step 2.** Retrieve the image's ID
```
curl -v -s "http://127.0.0.1:8082/v1.24/images/json" | jq -r '.[0].Id'
```
**Response:** HTTP 200
```
sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad
```

**Step 3.** Query image history via compat endpoint
```
curl -v -s "http://127.0.0.1:8082/v1.24/images/sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad/history" | jq .[0].Tags
```
## Buggy Response
HTTP 200
```
null
```
## Expected Response
HTTP 200
```
[
  "docker.io/library/alpine:latest"
]
```

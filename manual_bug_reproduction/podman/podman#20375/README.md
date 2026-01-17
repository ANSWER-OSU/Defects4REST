# podman#20375

## Description
Podman's REST API returns a different and incorrect "Size" value compared to Docker for the same image history endpoint under the same environment. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/20375

## Triggering Endpoint(s)
- `/images/create`
- `/images/json`
- `/images/{image_id}/history`

## Triggering Behavior
**Step 1.** Pull an image
```
curl -X POST "http://127.0.0.1:8082/v1.24/images/create?fromImage=alpine&tag=3.17.2"
```
**Response:** HTTP 200.
```
{"status":"Already exists","progressDetail":{},"id":"63b65145d645"}
{"status":"Pulling fs layer","progressDetail":{},"id":"b2aa39c304c2"}
{"status":"Download complete","progressDetail":{},"id":"b2aa39c304c2"}
{"status":"Download complete","progressDetail":{},"id":"b2aa39c304c2"}
```
**Step 2.** Retrieve the image ID
```
curl -s http://127.0.0.1:8082/v1.24/images/json | jq -r '.[0].Id'
```
**Response:** HTTP 200
```
sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad
```

**Step 3.** Retrieve the history information
```
curl -s "http://127.0.0.1:8082/v1.24/images/sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad/history" | jq .
```
## Buggy Response
HTTP 200. `Size` field reports `0` for all layers.
```
[
  {
    "Id": "sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad",
    "Created": 1766016749,
    "CreatedBy": "CMD [\"/bin/sh\"]",
    "Tags": [
      "docker.io/library/alpine:latest"
    ],
    "Size": 0,
    "Comment": "buildkit.dockerfile.v0"
  },
  {
    "Id": "sha256:<missing>",
    "Created": 1766016749,
    "CreatedBy": "ADD alpine-minirootfs-3.23.2-x86_64.tar.gz / # buildkit",
    "Tags": null,
    "Size": 0,
    "Comment": "buildkit.dockerfile.v0"
  }
]
```

## Expected Response
HTTP 200. Base layer `Size` reflects actual layer size.
```
[
  {
    "Id": "sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad",
    "Created": 1766016749,
    "CreatedBy": "CMD [\"/bin/sh\"]",
    "Tags": [
      "docker.io/library/alpine:latest"
    ],
    "Size": 0,
    "Comment": "buildkit.dockerfile.v0"
  },
  {
    "Id": "sha256:<missing>",
    "Created": 1766016749,
    "CreatedBy": "ADD alpine-minirootfs-3.23.2-x86_64.tar.gz / # buildkit",
    "Tags": [
      "docker.io/library/alpine:latest"
    ],
    "Size": 8724480,
    "Comment": "buildkit.dockerfile.v0"
  }
]
```

# podman#24886

## Description
API request fails with 500 error because the JSON payload includes -1 for a field defined as uint64 which cannot accept negative values.

## GitHub Issue URL
https://github.com/containers/podman/issues/24886

## Triggering Endpoint(s)
- `/libpod/containers/create`

## Triggering Behavior
**Step 1.** Pull an image
```
curl -X POST \
  "http://127.0.0.1:8082/v4.0.0/libpod/images/pull?reference=docker.io/library/alpine
```
**Response:** HTTP 200.
```
{"stream":"Trying to pull docker.io/library/alpine:latest...\n"}
{"stream":"Getting image source signatures\n"}
{"stream":"Copying blob sha256:1074353eec0db2c1d81d5af2671e56e00cf5738486f5762609ea33d606f88612\n"}
{"stream":"Copying config sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad\n"}
{"stream":"Writing manifest to image destination\n"}
{"images":["e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad"],"id":"e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad"}
```

**Step 2.** Create container with `r_limits = -1`
```
curl -X POST http://127.0.0.1:8082/v4.0.0/libpod/containers/cre
ate \
  -H "Content-Type: application/json" \
  -d '{
    "image": "docker.io/library/alpine",
    "command": ["/bin/sh"],
    "r_limits": [
      {
        "type": "memlock",
        "soft": -1,
        "hard": -1
      }
    ]
  }'
```
## Buggy Response:
HTTP 500.
```
{
  "cause": "json: cannot unmarshal number -1 into Go struct field POSIXRlimit.ContainerResourceConfig.r_limits.soft of type uint64",
  "message": "decode(): json: cannot unmarshal number -1 into Go struct field POSIXRlimit.ContainerResourceConfig.r_limits.soft of type uint64",
  "response": 500
}
```

## Expected Response:
HTTP 200.
```
{
  "Id": "7781e9720a037ce1e502d407c5053c9b4ff63c3cebfd81edd1842270d759029c",
  "Warnings": []
}
```

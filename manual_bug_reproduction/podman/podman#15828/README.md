# podman#17204

## Description
The API does not return the correct status when the fromImage query parameter references a nonexistent image. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/15828

## Triggering Endpoint(s)
- `/images/create`

## Triggering Behavior
**Step 1.** Pull a nonexistent image
```
curl -v -X POST   "http://127.0.0.1:8082/v1.40/images/create?fromImage=reg.example.com/foo:does-not-exist"
```
## Buggy Response
HTTP 200
```
{"progressDetail":{},"errorDetail":{"message":"initializing source docker://reg.example.com/foo:does-not-exist: pinging container registry reg.example.com: Get \"https://reg.example.com/v2/\": dial tcp: lookup reg.example.com on 182.8.64.11:53: no such host"},"error":"initializing source docker://reg.example.com/foo:does-not-exist: pinging container registry reg.example.com: Get \"https://reg.example.com/v2/\": dial tcp: lookup reg.example.com on 182.8.64.11:53: no such host"}
```

## Expected Response
HTTP 500
```
{"progressDetail":{},"errorDetail":{"message":"initializing source docker://reg.example.com/foo:does-not-exist: pinging container registry reg.example.com: Get \"https://reg.example.com/v2/\": dial tcp: lookup reg.example.com on 182.8.64.13:53: no such host"},"error":"initializing source docker://reg.example.com/foo:does-not-exist: pinging container registry reg.example.com: Get \"https://reg.example.com/v2/\": dial tcp: lookup reg.example.com on 182.8.64.13:53: no such host"}
```

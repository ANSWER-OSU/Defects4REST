# podman#17778

## Description
Podman rejects POST requests with a string value for the pull field that Docker accepts due to stricter schema validation. (HTTP 400)

## GitHub Issue URL
https://github.com/containers/podman/issues/17778

## Triggering Endpoint(s)
- `/build`

## Triggering Behavior
**Step 1.** Build image with `pull=always (string)`
```
curl -v   -X POST   -H "Content-Type: application/x-tar"   --data-binary "@ctx.tar"   "http://127.0.0.1:8082/v1.40/build?pull=always"
```
## Buggy Response
HTTP 400 Bad Request

## Expected Response
HTTP 200
```
{"stream":"STEP 1/1: FROM alpine\n"}
{"stream":"Trying to pull docker.io/library/alpine:latest...\n"}
{"stream":"Getting image source signatures\n"}
{"stream":"Copying blob sha256:1074353eec0db2c1d81d5af2671e56e00cf5738486f5762609ea33d606f88612\n"}
{"stream":"Copying config sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad\n"}
{"stream":"Writing manifest to image destination\n"}
{"stream":"Storing signatures\n"}
{"stream":"COMMIT\n"}
{"stream":"--\u003e e7b39c54cdec\n"}
{"stream":"e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad\n"}
{"aux":{"ID":"sha256:e7b39c54cdeca0d2aae83114bb605753a5f5bc511fe8be7590e38f6d9f915dad"}}
{"stream":"Successfully built e7b39c54cdec\n"}
```

# podman#13831

## Description
The API build fails because it cannot find the Dockerfile or Containerfile at the expected file path during the remote build process. (HTTP 400)

## GitHub Issue URL
https://github.com/containers/podman/issues/13831

## Triggering Endpoint(s)
- `/libpod/build`

## Triggering Behavior
**Step 1.** Call the build endpoint with remote
```
curl -v -X POST \
  "http://127.0.0.1:8082/v2.0.0/libpod/build?remote=https%3A%2F%2Fgithub.com%2Falpinelinux%2Fdocker-alpine"

```

## Buggy Response
HTTP 400
```
{"cause":"stat /var/tmp/libpod_builder585316184/build/Containerfile: no such file or directory","message":"failed to parse query parameter 'dockerfile': \"Dockerfile\": stat /var/tmp/libpod_builder585316184/build/Containerfile: no such file or directory","response":400}
```

## Expected Response
HTTP 200

# podman#14647

## Description
Content-Type header is incorrectly set to text/plain instead of application/json only when the container list is empty indicating environment-specific response behavior. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/14647

## Triggering Endpoint(s)
- `/libpod/containers/json`

## Triggering Behavior
**Step 1.** List containers (libpod API)
```
curl -v -X GET \
  "http://127.0.0.1:8082/v4.3.0/libpod/containers/json" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json"
```
## Buggy Response
HTTP 200. Content type is `text/plain`
```
...
< Content-Type: text/plain; charset=us-ascii
```

## Expected Response
HTTP 200. Content type is `application/json`
```
...
< Content-Type: application/json
```

# podman#13986

## Description
The API rejects valid status filter values like removing and restarting resulting in incorrect query parameter handling. (HTTP 500)

## GitHub Issue URL
https://github.com/containers/podman/issues/13986

## Triggering Endpoint(s)
- `/libpod/containers`

## Triggering Behavior
**Step 1.** Filter containers by status=removing
```
curl -v --get   --data-urlencode 'filters={"status":["removing"]}'   "http://127.0.0.1:8082/v4.3.0/libpod/containers/json"
```

## Buggy Response
HTTP 500
```
{"cause":"removing is not a valid status","message":"removing is not a valid status","response":500}
```
## Expected Response
HTTP 200

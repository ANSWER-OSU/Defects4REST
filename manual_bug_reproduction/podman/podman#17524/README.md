# podman#17524

## Description
The API response for the "Titles" field returns a single string instead of an array only when accessed via the podman socket in a specific environment and version. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/17524

## Triggering Endpoint(s)
- `/containers/{name}/top`

## Triggering Behavior
**Step 1.** Create a container
```
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["sleep","infinity"]}' \
  "http://127.0.0.1:8082/v1.40/containers/create?name=d4rest_toptest"
```
**Response:** HTTP 200
```
{"Id":"784bef951452750876b134109b8f26a844b1aa23b9aa48223b13726ef7fd73b2","Warnings":[]}
```

**Step 2.** Start the container
```
curl -v -s -X POST \
  "http://127.0.0.1:8082/v1.40/containers/d4rest_toptest/start"
```
**Response:** HTTP 204

**Step 3.** Query container top
```
curl -v -s \
  "http://127.0.0.1:8082/v1.40/containers/d4rest_toptest/top"
```
## Buggy Response
HTTP 200
```
{"Titles":["PID   USER     TIME  COMMAND"]}
```
## Expected Response
HTTP 200
```
{"Titles":["PID","USER","TIME","COMMAND"]}
```

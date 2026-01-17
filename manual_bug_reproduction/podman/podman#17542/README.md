# podman#17542

## Description
The API fails to handle negative timeout query parameters as allowed by the Docker spec resulting in a parameter parsing error. (HTTP 400)

## GitHub Issue URL
https://github.com/containers/podman/issues/17542

## Triggering Endpoint(s)
- `/containers/{name}/start`
- `/containers/{name}/stop`

## Triggering Behavior
**Step 1.** Create a container
```
curl -v -s -X POST   -H "Content-Type: application/json"   -d '{"Image":"alpine","Cmd":["sleep","infinity"]}'   "http://127.0.0.1:8082/v1.40/containers/create?name=d4rest_testneg"
```
**Response:** HTTP 201
```
{"Id":"85e0088f1c28b817328f74357ea161fd3ec347a061d963423fa2d2eaf080450b","Warnings":[]}
```
**Step 2.** Start the container
```
curl -v -s -X POST   "http://127.0.0.1:8082/v1.40/containers/d4rest_testneg/start"
```
**Response:** HTTP 204

**Step 3.** Stop container with negative timeout parameter `t=-1`
```
curl -v -X POST \
  "http://127.0.0.1:8082/v1.40/containers/d4rest_testneg/stop?t=-1"
```
## Buggy Response
HTTP 400
```
{"cause":"schema: error converting value for \"t\"","message":"failed to parse parameters for /v1.40/containers/d4rest_testneg/stop?t=-1: schema: error converting value for \"t\"","response":400}
```
## Expected Response
HTTP 204

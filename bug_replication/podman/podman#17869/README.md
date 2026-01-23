# podman#17869

## Description
The API response uses "Id" instead of the expected "id" field causing schema incompatibility with clients expecting the correct field name. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/17869

## Triggering Endpoint(s)
- `/containers/create`
- `/containers/{name}/start`
- `/containers/{name}/stats`

## Triggering Behavior
**Step 1.** Create a container
```
curl -v -X POST   "http://127.0.0.1:8082/containers/create?name=d4rest_testctr"   -H "Content-Typ
e: application/json"   -d '{"Image":"docker.io/library/alpine:latest","Cmd":["sleep","infinity"]}'
```
**Response:** HTTP 200
```
{"Id":"9b992d17e4cb28fb38df2f3a78f65da4378abfbe91092ff5ae683f79b9c73d41","Warnings":[]}
```

**Step 2.** Start the container
```
curl -v -X POST "http://127.0.0.1:8082/containers/d4rest_testctr/start"
```
**Response:** HTTP 204

**Step 3.** Call stats
```
curl -v "http://127.0.0.1:8082/containers/d4rest_testctr/stats?stream=false" | jq
```
## Buggy Response
HTTP 200. The "i" in "Id" is in uppercase
```
{
"name": "d4rest_testctr",
  "Id": "9b992d17e4cb28fb38df2f3a78f65da4378abfbe91092ff5ae683f79b9c73d41",
  ...
}
```

## Expected Response
HTTP 200. The "i" in "id" is in lowercase
```
{
"name": "d4rest_testctr",
  "id": "7c72439dfd3924b9361b3c8a5df48b6ec5cb204b07277021659e367c057d73bf",
  ...
}
```

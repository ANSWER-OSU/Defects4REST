# podman#14208

## Description
Podman API incorrectly returns HTTP 500 instead of the expected HTTP 409 on image conflict which breaks compatibility with Docker API clients.

## GitHub Issue URL
https://github.com/containers/podman/issues/14208

## Triggering Endpoint(s)
- `/images/{name}`

## Triggering Behavior
**Step 1.** Pull an image
```
curl -X POST "http://127.0.0.1:8082/v1.40/images/create?fromImage=alpine"
```
**Response:** HTTP 200
```
{"status":"Already exists","progressDetail":{},"id":"1074353eec0d"}
{"status":"Pulling fs layer","progressDetail":{},"id":"e7b39c54cdec"}
{"status":"Download complete","progressDetail":{},"id":"e7b39c54cdec"}
{"status":"Download complete","progressDetail":{},"id":"e7b39c54cdec"}
```

**Step 2.** Create a container
```
curl -X POST     -H "Content-Type: application/json"     --data '{"Image":"alpine","Cmd":["sleep","999999"]}'     "http://127.0.0.1:8082/v1.40/containers/create?name=d4rest_imgtest"
```
**Response:** HTTP 200
```
{"Id":"8811734b7d0a01c7baa6615a979ef047484393f0efaea779cc58ac8f72f21ebc","Warnings":[]}
```

**Step 3.** Start the container
```
curl -v -X POST     "http://127.0.0.1:8082/v1.40/containers/d4rest_imgtest/start"
```
**Response:** HTTP 204

**Step 4.** Retrieve the container's image ID
```
curl -v -s "http://127.0.0.1:8082/v1.40/containers/d4rest_imgtest/json" | jq -r '.Image'
```
**Response:** HTTP 200
```
docker.io/library/alpine:latest
```

**Step 5.** Delete the container's image
```
curl -v -X DELETE     "http://127.0.0.1:8082/v1.40/images/docker.io/library/alpine:latest"
```

## Buggy Response
HTTP 500
```
{"cause":"image is in use by a container","message":"Image used by 4e4e878aa9ec0287509ff3b51a21bf2009cda1393bdfa7d0fd2f762e8189ce4a: image is in use by a container","response":500}
```
## Expected Response
HTTP 409
```
{"cause":"image is in use by a container","message":"image docker.io/library/alpine:latest is in use: Image used by 8811734b7d0a01c7baa6615a979ef047484393f0efaea779cc58ac8f72f21ebc: image is in use by a container","response":409}
```

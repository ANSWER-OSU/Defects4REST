# podman#19368

## Description
API returns incorrect status code (HTTP 500) when attempting to send a kill signal to a stopped container which is a process signal handling issue.

## GitHub Issue URL
https://github.com/containers/podman/issues/19368

## Triggering Endpoint(s)
- `/containers/create`
- `/containers/{container_name}/start`
- `/containers/{container_name}/kill`
- `/containers/{container_name}/stop`

## Triggering Behavior

**Step 1.** Pull the image for the container
```
curl -X POST "http://127.0.0.1:8045/v1.41/images/create?fromImage=nginx"
```
**Response:** HTTP 200.
```
{"status":"Download complete","progressDetail":{},"id":"058f4935d1cb"}
```

**Step 2.** Create a container
```
curl -s -X POST -w "%{http_code}" \
"http://127.0.0.1:8045/v1.41/containers/create?name=d4rest_nginx" \
-H "Content-Type: application/json" \
-d '{"Image":"nginx"}' | jq
```
**Response:** HTTP 201
```
{
  "Id": "be28fff4f471a07469a31e0ba0ba8728371a328707640498e8a305fac5017588",
  "Warnings": []
}
```

**Step 3.** Start the container
```
curl -v -X POST -w \
"http://127.0.0.1:8045/v1.41/containers/d4rest_nginx/start"
```
**Response:** HTTP 204

**Step 4.** Stop the container
```
curl -v -X POST -w \
"http://127.0.0.1:8045/v1.41/containers/d4rest_nginx/stop"
```
**Response:** HTTP 204

**Step 5.** Kill the stopped container
```
curl -v -X POST -w "%{http_code}" \
"http://127.0.0.1:8045/v1.41/containers/d4rest_nginx/kill"
```

## Buggy Response
HTTP 500
```
{
  "cause": "container state improper",
  "message": "can only kill running containers. be28fff4f471a07469a31e0ba0ba8728371a328707640498e8a305fac5017588 is in state exited: container state improper",
  "response": 500
}
```
## Expected Response
HTTP 409
```
{
  "cause": "container state improper",
  "message": "can only kill running containers. e57f776399afc68adc7a73014b9501611deb4aa7c3713da86a105752c8842201 is in state exited: container state improper",
  "response": 409
}
```

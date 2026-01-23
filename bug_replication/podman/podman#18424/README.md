# podman#18424

## Description
ExecIDs incorrectly report as running long after the process has exited indicating a failure in tracking or updating process state within the container. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/18424

## Triggering Endpoint(s)
- `/containers/create`
- `/containers/{container_id}/start`
- `/containers/{container_id}/exec`
- `/exec/{exec_id}/start`
- `/exec/{exec_id}/json`

## Triggering Behavior
**Step 1.** Create a container that runs for 300 seconds.
```
curl -s -X POST \
"http://127.0.0.1:18424/v1.41/containers/create?name=d4rest_mycontainer" \
-H "Content-Type: application/json" \
-d '{
  "Image":"alpine:3.20",
  "Cmd":["sh","-c","sleep 300"],
  "Tty": false
}' | jq
```
**Response:** HTTP 200.
```
{
  "Id": "35a98763ea5744664f3c8d51d34a127ad1a81c8fd62aaec8861180b6ae9000fe",
  "Warnings": []
}
```

**Step 2.** Start the container using container ID
```
curl -s -X POST \
"http://127.0.0.1:18424/v1.41/containers/35a98763ea5744664f3c8d51d34a127ad1a81c8fd62aaec8861180b6ae9000fe/start"
```
**Response:** HTTP 200.

**Step 3.** Create an executable session that runs for 5 seconds
```
curl -s -X POST \
"http://127.0.0.1:18424/v1.41/containers/35a98763ea5744664f3c8d51d34a127ad1a81c8fd62aaec8861180b6ae9000fe/exec" \
-H "Content-Type: application/json" \
-d '{
  "AttachStdout": false,
  "AttachStderr": false,
  "Tty": false,
  "Cmd": ["sh","-c","sleep 5"]
}' | jq
```
**Response:** HTTP 200.
```
{
  "Id": "d5801dadb1457e1a2a719e64496716d108db1d555e24a167ae7a4bd796fee521"
}
```

**Step 4.** Start the execution(?)
```
curl -s -X POST \
"http://127.0.0.1:18424/v1.41/exec/d5801dadb1457e1a2a719e64496716d108db1d555e24a167ae7a4bd796fee521/start" \
-H "Content-Type: application/json" \
-d '{"Detach": true, "Tty": false}' | jq
```
**Response:** HTTP 200.

**Step 5.** Poll the exec status every second
```
for i in {1..30}; do
  curl -s \
  "http://127.0.0.1:18424/v1.41/exec/d5801dadb1457e1a2a719e64496716d108db1d555e24a167ae7a4bd796fee521/json" \
  | jq '{Running, ExitCode}'
  sleep 1
done
```

## Buggy Response
HTTP 200. `"Running": true` for 5 minutes
```
{
  "Running": true,
  "ExitCode": 0
}
{
  "Running": true,
  "ExitCode": 0
}
{
  "Running": true,
  "ExitCode": 0
}
```
## Expected Response
HTTP 200. `"Running": false` immediately after few seconds

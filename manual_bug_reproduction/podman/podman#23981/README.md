# podman#23981

## Description
The issue reports that the API returns a list of strings instead of the expected list of lists of strings which is a payload structure mismatch. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/23981

## Triggering Endpoint(s)
- `/containers/create`
- `/containers/{container_name}/start`
- `/containers/{container_name}/top`

## Triggering Behavior
**Step 1.** Create a container
```
curl -s -X POST -H "Content-Type: application/json" --data '{
  "Image":"alpine:3.20",
  "Cmd":["sh","-c","sleep 1d"]
}' http://127.0.0.1:12345/v1.41/containers/create?name=d4rest_topdemo | jq .
```
**Response:** HTTP 200.
```
{
  "Id": "74512cbcc0a37810a24edf5ba6829ff9c271b575c7b87a0b61e4c84275abf61d",
  "Warnings": []
}
```

**Step 2.** Start the container
```
curl -s -X POST \
http://127.0.0.1:12345/v1.41/containers/d4rest_topdemo/start
```
**Response:** HTTP 204.

**Step 3.** Get stats
```
curl -s http://127.0.0.1:12345/v1.41/containers/d4rest_topdemo/top?ps_args=aux | jq .
```
## Buggy Response
HTTP 200.
```
$ curl -s \
http://127.0.0.1:12345/v1.41/containers/d4rest_topdemo/top?ps_args=aux \
| jq .
{
  "Processes": [
    [
      "root           1  0.3  0.0   1612     4 ?        Ss   23:55   0:00 sleep 1d"
    ]
  ],
  ...
}
```
## Expected Response
HTTP 200.
```
{
  "Processes": [
    [
      "root",
      "1",
      "0.0",
      "0.0",
      "1612",
      "4",
      "?",
      "Ss",
      "00:11",
      "0:00",
      "sleep 1d"
    ]
  ...
}
```

# podman#17204

## Description
Test intermittently fails on specific Fedora environment with attach API returning empty content instead of expected output. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/17204

## Triggering Endpoint(s)
- `containers/{id}/attach`

## Triggering Behavior
**Step 1.** Create a container
```
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"Cmd":["sh","-c","echo podman; sleep 100"],"Image":"alpine"}' \
  "http://127.0.0.1:8082/v1.40/containers/create?name=d4rest_topcontainer"
```
**Response:** HTTP 200
```
{"Id":"cdb17a1136720fd55ca0a0d03e31c2f42d1d35c603a43b9207f6308605cd1d3a","Warnings":[]}
```

**Step 2.** Start the container
```
curl -s -X POST \
  "http://127.0.0.1:8082/v1.40/containers/cdb17a1136720fd55ca0a0d03e31c2f42d1d35c603a43b9207f6308605cd1d3a/start"
```
**Response:** HTTP 204

**Step 3.** Attach container output (`logs=true, stream=false`)
```
curl -v -s -X POST   "http://127.0.0.1:8082/v1.40/containers/cdb17a1136720fd55ca0a0d03e31c2f42d1d35c603a43b9207f6308605cd1d3a/attach?logs=true&stream=false"   | hexdump -C
```

## Buggy Response
HTTP 200
```
00000000  01 00 00 00 00 00 00 07  70 6f 64 6d 61 6e 0a     |........podman.|
0000000f
```

## Expected Response
HTTP 200 - No payload

# podman#15720

## Description
RefCount for volumes in the REST API always returns 1 regardless of actual usage indicating incorrect volume usage
tracking.

## GitHub Issue URL
https://github.com/containers/podman/issues/15720

## Triggering Endpoint(s)
- `/libpod/volumes/create`
- `/libpod/system/df`

## Triggering Behavior
**Step 1.** Create a dummy volume named "d4rest_bugvol"
```
curl -s -X POST \
  http://127.0.0.1:8080/v1.41/libpod/volumes/create \
  -H "Content-Type: application/json" \
  -d '{"Name": "d4rest_bugvol"}'
```
**Response:** HTTP 200.
```
{
  "Name": "d4rest_bugvol",
  "Driver": "local",
  "Mountpoint": "/var/lib/containers/storage/volumes/d4rest_bugvol/_data",
  "CreatedAt": "2026-01-02T17:15:21.739171416+07:00",
  "Labels": {},
  "Scope": "local",
  "Options": {},
  "MountCount": 0,
  "NeedsCopyUp": true,
  "NeedsChown": true
}
```
**Step 2.** Use /libpod/system/df to see RefCount
```
curl -s \
  "http://127.0.0.1:8080/v1.41/system/df?verbose=true" \
| jq '.Volumes[] | select(.Name=="d4rest_bugvol")'
```
## Buggy Response:
Even though the volume is unused, RefCount = 1. (HTTP 200)
```
{
  ...
  "UsageData": {
    "RefCount": 1,
    "Size": 0
  }
}
```
## Expected Response
RefCount=0. (HTTP 200)
```
{
  ...
  "UsageData": {
    "RefCount": 0,
    "Size": 0
  }
}
```

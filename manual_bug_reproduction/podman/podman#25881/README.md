# podman#25881

## Description
In rootless mode the REST API fails to enforce ulimit settings for containers even though the CLI applies them correctly (HTTP 200).

## GitHub Issue URL
https://github.com/containers/podman/issues/25881

## Triggering Endpoint(s)
- `/containers/create?name={name}`

## Triggering Behavior
**Step 1.** Pull an image
```
curl -X POST "http://127.0.0.1:8082/images/create?fromImage=alpine"
```
**Response:** HTTP 200.
```
{"status":"Download complete","progressDetail":{},"id":"..."}
```

**Step 2.** Create a container
```
curl -X POST "http://127.0.0.1:8082/containers/create?name=d4rest_test" \
  -H "Content-Type: application/json" \
  -d '{
    "Image": "alpine",
    "Cmd": ["sh", "-c", "ulimit -Ht"],
    "HostConfig": {
      "Ulimits": [
        { "Name": "cpu", "Soft": 1, "Hard": 2 }
      ]
    }
  }'
```
**Response:** HTTP 200.
```
{
  "Id": "827aead6e50b68b63fee7abb443470af6f1b16d2c6ab510324d94be5b7c5c3e9",
  "Warnings": []
}
```

**Step 3.** Inspect the container
```
curl -s "http://127.0.0.1:8082/containers/d4rest_test/json" | jq '.HostConfig.Ulimits'
```

## Buggy Response:
HTTP 200.
```
[]
```

## Expected Response:
HTTP 200.
```
[
  {
    "Name": "RLIMIT_CPU",
    "Hard": 2,
    "Soft": 1
  }
]
```

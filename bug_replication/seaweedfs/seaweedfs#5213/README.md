## SeaweedFS#5213

## Description

Timeouts occur during `/dir/assign` requests specifically when the master initiates volume growth, indicating issues with cluster coordination during dynamic volume assignment.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/5213](https://github.com/seaweedfs/seaweedfs/issues/5213)

## Triggering Endpoints:

* `/dir/assign`

## Triggering Behavior:

**Step 1.** Quick single assign:

```bash
curl -s "http://127.0.0.1:9333/dir/assign?collection=nntp&count=1&replication=001"
```

**Step 2.** Loop to hammer `/dir/assign` to trigger volume growth:

```bash
while true; do
  curl --max-time 3 -s \
    "http://127.0.0.1:9333/dir/assign?collection=nntp&count=10000&replication=001" \
    || echo "timeout"
done
```

## Buggy Response

* Requests time out and docker logs show:

```text
master_server_handlers.go:125 dirAssign volume growth {"collection":"nntp","replication":{"node":1},"ttl":{"Count":0,"Unit":0}}
```

## Expected Response

* No timeouts and no failed assignment requests.

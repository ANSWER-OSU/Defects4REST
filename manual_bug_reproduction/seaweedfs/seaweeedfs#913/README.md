## SeaweedFS#913

## Description

The API fails to allocate all requested volumes and reports inconsistent free volume counts, indicating issues with resource quota enforcement.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/913](https://github.com/seaweedfs/seaweedfs/issues/913)

## Triggering Endpoints:

* `/vol/grow`

## Triggering Behavior:

**Step 1.** First allocation attempt:

```bash
curl "http://seaweed-master:9333/vol/grow?collection=test&count=6400&replication=000"
```

**Response:** HTTP 406

```json
{"error":"Failed to assign 6625: rpc error: code = Unknown desc = No more free space left"}
```

**Step 2.** Second allocation attempt, reports only 42 volumes left:

```bash
curl "http://seaweed-master:9333/vol/grow?collection=test&count=6400&replication=000"
```

**Response:** HTTP 406

```json
{"error":"Only 42 volumes left! Not enough for 6400"}
```

**Step 3.** Allocate the remaining 42 volumes:

```bash
curl "http://seaweed-master:9333/vol/grow?collection=test&count=42&replication=000"
```

**Response:** HTTP 200

```json
{"count":42}
```

## Buggy Response

* First large allocation stops early with `"No more free space left."`
* Retrying reports `"Only 42 volumes left."`
* Small request for 42 volumes succeeds.

## Expected Response

* HTTP 200 with consistent and accurate volume allocation response.

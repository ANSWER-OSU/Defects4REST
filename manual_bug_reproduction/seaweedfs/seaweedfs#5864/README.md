## SeaweedFS#5864

## Description

When the WebDAV service stops, a 404 error is returned for an existing file, indicating a file access issue rather than a true file absence.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/5864](https://github.com/seaweedfs/seaweedfs/issues/5864)

## Triggering Endpoints:

* `/{filePath+}`
* `/buckets/{bucket}/{objectPath}`

## Triggering Behavior:

**Step 1.** Create a bucket (top-level directory):

```bash
curl -X PUT "http://127.0.0.1:7333/warp-benchmark-bucket/" \
  -H "Content-Type: application/x-directory"
```

**Step 2.** Create nested directories inside the bucket:

```bash
curl -X PUT "http://127.0.0.1:7333/warp-benchmark-bucket/data/" \
  -H "Content-Type: application/x-directory"

curl -X PUT "http://127.0.0.1:7333/warp-benchmark-bucket/data/2025/" \
  -H "Content-Type: application/x-directory"

curl -X PUT "http://127.0.0.1:7333/warp-benchmark-bucket/data/2025/11/" \
  -H "Content-Type: application/x-directory"

curl -X PUT "http://127.0.0.1:7333/warp-benchmark-bucket/data/2025/11/10/" \
  -H "Content-Type: application/x-directory"
```

**Step 3.** Upload the object:

```bash
echo "hello" > test.txt
curl -s -X PUT "http://127.0.0.1:7333/warp-benchmark-bucket/data/2025/11/10/obj_1q9XpS7aA4FbYzL3(7Kd).rnd" \
  --data-binary @test.txt \
  -H "Content-Type: text/plain"
```

**Step 4.** Continuously poll the object using HEAD:

```bash
while true; do
  curl -sI \
    "http://127.0.0.1:7333/warp-benchmark-bucket/data/2025/11/10/obj_1q9XpS7aA4FbYzL3(7Kd).rnd" \
    | grep HTTP
done
```

**Buggy Response:** 404 Not Found after WebDAV process is killed

**Expected Response:** 202 Request accepted but resource state unknown as the WebDAV Filer is stopped, or 500 error

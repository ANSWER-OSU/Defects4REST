## **SeaweedFS#4088**

## Description

The volume server returns **404 Not Found** when accessing files stored on a volume that has been marked as read-only. Files on read-only volumes should remain readable, but the system fails to serve them.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/4088](https://github.com/seaweedfs/seaweedfs/issues/4088)

## Triggering Endpoints:

* `/filer/<bucket>/<object>`
* `/<volumeId>,<fileKey>`



## Triggering Behavior:

**Step 1.** Upload a file via the Filer:

```bash
echo "hello read-only test" > test2.txt
curl -v -F file=@test2.txt "http://localhost:8888/readonlytest/testfile2"
```

**Response:**

```text
* Host localhost:8888 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8888...
* Connected to localhost (::1) port 8888
> POST /readonlytest/testfile2 HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/8.5.0
> Accept: */*
> Content-Length: 220
> Content-Type: multipart/form-data; boundary=------------------------fk7UELBw4Dn1maHxrkISX9
> 
* We are completely uploaded and fine
< HTTP/1.1 201 Created
< Content-Md5: /cAw/qsXKPVupLL7Qab91Q==
< Content-Type: application/json
< Server: SeaweedFS Filer 30GB 3.43
< Date: Thu, 18 Dec 2025 07:42:02 GMT
< Content-Length: 30
< 
{"fid":"8,066c762b67","url":"volume:8080","publicUrl":"volume:8080","count":1}
* Connection #0 to host localhost left intact
```

**Step 2.** Mark the volume as read-only (using the volume ID from the `fid`):

```bash
weed volume.marknode localhost:8080 -volumeId 8 -readonly
```

**Step 3.** Attempt to fetch the file directly from the volume:

```bash
curl -v http://localhost:8080/8,066c762b67
```

**Buggy Response:** HTTP 404 Not Found when fetching a file from a read-only volume

```text
* Host localhost:8080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8080...
* Connected to localhost (::1) port 8080
> GET /8,066c762b67 HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 404 Not Found
< Server: SeaweedFS Volume 30GB 3.43
< X-Amz-Request-Id: e6a9aec9-f125-4993-939f-154ccc35102e
< Date: Thu, 18 Dec 2025 07:45:40 GMT
< Content-Length: 0
< 
* Connection #0 to host localhost left intact
```

**Expected Response:** HTTP 200 OK with the file content returned from the read-only volume

```text
* Host localhost:8080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8080...
* Connected to localhost (::1) port 8080
> GET /8,066c762b67 HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.5.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: SeaweedFS Volume 30GB 3.43
< X-Amz-Request-Id: f4b7c9e2-12ab-4c91-9d45-8a9d0c2f1e33
< Date: Thu, 18 Dec 2025 07:46:10 GMT
< Content-Type: application/octet-stream
< Content-Length: 18
< 
hello read-only test
* Connection #0 to host localhost left intact
```
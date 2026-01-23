## Seaweedfs#4270

## Description

API returns 500 Internal Server Error instead of 409 Conflict when attempting to create a directory that already exists.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/4270](https://github.com/seaweedfs/seaweedfs/issues/4270)

## Triggering Endpoints

* `/{dirPath+}`

## Triggering Behavior

**Step 1.** Attempt to create the same directory twice using direct `POST` requests:

```bash
curl -vvv -X POST "http://localhost:8888/too/"

curl -vvv -X POST "http://localhost:8888/too/"
```

**Buggy Response:** First directory was created with response 201 but second directory returned HTTP 500 Internal Server Error

```text
Host localhost:8888 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8888...
* Connected to localhost (::1) port 8888
> POST /too/ HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/8.5.0
> Accept: */*
< HTTP/1.1 201 Created
< Content-Type: application/json
< Server: SeaweedFS Filer 30GB 3.43
< Date: Thu, 18 Dec 2025 06:28:38 GMT
< Content-Length: 14
{"name":"too"}
* Host localhost:8888 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8888...
* Connected to localhost (::1) port 8888
> POST /too/ HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/8.5.0
> Accept: */*
< HTTP/1.1 500 Internal Server Error
< Content-Type: application/json
< Server: SeaweedFS Filer 30GB 3.43
< Date: Thu, 18 Dec 2025 06:28:38 GMT
< Content-Length: 35
{"error":"dir /too already exists"}
```

**Expected Response:** First directory created with HTTP 201 but second directory should return proper HTTP 409 Conflict

```text
Host localhost:8888 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8888...
* Connected to localhost (::1) port 8888
> POST /hoo/ HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/8.5.0
> Accept: */*
< HTTP/1.1 201 Created
< Content-Type: application/json
< Server: SeaweedFS Filer 30GB 3.43
< Date: Thu, 18 Dec 2025 06:47:28 GMT
< Content-Length: 14
{"name":"hoo"}
* Host localhost:8888 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8888...
* Connected to localhost (::1) port 8888
> POST /hoo/ HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/8.5.0
> Accept: */*
< HTTP/1.1 409 Conflict
< Content-Type: application/json
< Server: SeaweedFS Filer 30GB 3.43
< Date: Thu, 18 Dec 2025 06:47:59 GMT
< Content-Length: 35
{"error":"dir /hoo already exists"}
```

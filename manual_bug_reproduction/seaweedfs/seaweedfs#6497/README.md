## SeaweedFS#6497

## Description

Using `PUT` to upload an object to a bucket with an invalid name leads to the creation of a bucket that cannot be removed. This indicates improper validation of bucket names and can leave unremovable or invalid buckets in the system.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/6497](https://github.com/seaweedfs/seaweedfs/issues/6497)

## Triggering Endpoints

* `/bucket/<bucket_name>/<object_name>` (PUT object)
* `/bucket/<bucket_name>` (DELETE bucket)

## Triggering Behavior

**Step 1.** Create a test file:

```bash
echo "test content" > ab
```

**Step 2.** Attempt to upload the object to a bucket with an invalid name `aa`:

```bash
curl -v -X PUT --data-binary @ab http://localhost:8333/aa/a
```

**Response:**

```text
* Host localhost:8333 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8333...
* Connected to localhost (::1) port 8333
> PUT /aa/a HTTP/1.1
> Host: localhost:8333
> User-Agent: curl/8.5.0
> Accept: */*
> Content-Length: 13
> Content-Type: application/x-www-form-urlencoded
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Content-Length: 0
< ETag: "d6eb32081c822ed572b70567826d9d9d"
< Server: SeaweedFS 30GB 3.82
< X-Amz-Request-Id: 1766108011731037521
< Date: Fri, 19 Dec 2025 01:33:31 GMT
* Connection #0 to host localhost left intact
```

**Step 3.** Delete the object:

```bash
curl -v -X DELETE http://localhost:8333/aa/a
```

**Response:** HTTP 204 No Content (object deleted), but the bucket remains in an invalid state.

```text
* Host localhost:8333 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8333...
* Connected to localhost (::1) port 8333
> DELETE /aa/a HTTP/1.1
> Host: localhost:8333
> User-Agent: curl/8.5.0
> Accept: */*
< HTTP/1.1 204 No Content
< Server: SeaweedFS 30GB 3.82
< Date: Fri, 19 Dec 2025 01:35:58 GMT
* Connection #0 to host localhost left intact
```

**Step 4.** Attempt to delete the bucket:

```bash
curl -v -X DELETE http://localhost:8333/aa
```

**Response:** HTTP 204 No Content, but due to the invalid bucket name, the bucket may remain or cause inconsistencies.

```text
* Host localhost:8333 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8333...
* Connected to localhost (::1) port 8333
> DELETE /aa HTTP/1.1
> Host: localhost:8333
> User-Agent: curl/8.5.0
> Accept: */*
< HTTP/1.1 204 No Content
< Accept-Ranges: bytes
< Server: SeaweedFS 30GB 3.82
< X-Amz-Request-Id: 1766108188232090721
< Date: Fri, 19 Dec 2025 01:36:28 GMT
* Connection #0 to host localhost left intact
```

**Step 5.** GET bucket to check its state:

```bash
curl -v http://localhost:8333/aa
```

**Buggy Response:** HTTP 404 `NoSuchBucket`, indicating that the system has inconsistencies after creating a bucket with an invalid name.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error>
    <Code>NoSuchBucket</Code>
    <Message>The specified bucket does not exist</Message>
    <Resource>/aa</Resource>
    <RequestId>1766108212497774004</RequestId>
    <BucketName>aa</BucketName>
</Error>
```

## Expected Response

* PUT requests to invalid bucket names should **fail immediately** with HTTP 400 Bad Request.
PUT to invalid bucket name aa:

```
filer-1   | I1219 01:57:41.657042 common.go:120 error JSON response status 500: invalid bucket name aa: bucket name must between [3, 63] characters
filer-1   | I1219 01:57:41.657074 common.go:77 response method:PUT URL:/buckets/aa/a with httpStatus:500 and JSON:{"error":"invalid bucket name aa: bucket name must between [3, 63] characters"}
s3-1      | E1219 01:57:41.657474 s3api_object_handlers_put.go:164 upload to filer error: invalid bucket name aa: bucket name must between [3, 63] characters
```

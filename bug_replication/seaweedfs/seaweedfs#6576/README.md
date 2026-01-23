
## SeaweedFS#6576

## Description

SeaweedFS does not correctly handle the `x-id` query parameter emitted by AWS SDKs, causing presigned S3 GET requests to fail.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/6576](https://github.com/seaweedfs/seaweedfs/issues/6576)

## Triggering Endpoints:

* `/{bucket}/{object}`

## Prerequisite:

1. Run the Defects4REST command to generate a presigned URL that includes `x-id=GetObject`.
2. After the container starts, the prerequisite function runs automatically:
   - Creates bucket: `bug-demo-bucket`
   - Uploads file: `hello.txt`
   - Generates a presigned URL

**Example output:**

```text
Pre-requisites completed. Presigned URL:
http://127.0.0.1:8333/bug-demo-bucket/hello.txt?AWSAccessKeyId=power_user_key&Signature=F4holVcdzVNgOfGDJUy1%2Bxyi9J4%3D&Expires=1767389662&x-id=GetObject
````

Copy this presigned URL for the triggering behavior.

## Triggering Behavior:

**Step 1.** Trigger the defect using the presigned URL with `x-id=GetObject`:

```bash
curl "http://127.0.0.1:8333/bug-demo-bucket/hello.txt?AWSAccessKeyId=power_user_key&Signature=F4holVcdzVNgOfGDJUy1%2Bxyi9J4%3D&Expires=1767389662&x-id=GetObject"
```

**Buggy Response:** HTTP 500 — the S3 object exists, but the server fails to return it.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>InternalError</Code>
  <Message>We encountered an internal error, please try again.</Message>
  <Resource>/bug-demo-bucket/hello.txt</Resource>
  <RequestId>1767389875375643035</RequestId>
  <Key>hello.txt</Key>
  <BucketName>bug-demo-bucket</BucketName>
</Error>
```

**Expected Response:** HTTP 200 — the presigned URL works correctly, and the object is successfully retrieved even with `x-id=GetObject` included.

```text
Hello SeaweedFS
```

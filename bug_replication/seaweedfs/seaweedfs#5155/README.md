## SeaweedFS#5155

## Description

The API response is malformed and missing the required `VersionConfiguration` node, causing clients (e.g., AWS CLI) to fail parsing the response.

## GitHub Issue URL

[https://github.com/seaweedfs/seaweedfs/issues/5155](https://github.com/seaweedfs/seaweedfs/issues/5155)

## Triggering Endpoints:

* `/{bucket}`

## Triggering Behavior:

**Step 1.** Create a bucket and query its versioning:

```bash
curl -s -X PUT http://localhost:8333/mybucketexample && \
curl http://localhost:8333/mybucketexample?versioning
```

**Buggy Response:** HTTP 200 with `VersioningConfiguration` missing

```xml
<Status>
    Suspended
</Status>
```

**Expected Response:** HTTP 200 with `VersioningConfiguration` included

```xml
<VersioningConfiguration>
    <Status>Suspended</Status>
</VersioningConfiguration>
```


# podman#18092

## Description
The API fails to return expected images when filtering by label using a specific filter format indicating incorrect handling of query filter parameters. (HTTP 200)

## GitHub Issue URL
https://github.com/containers/podman/issues/18092

## Triggering Endpoint(s)
- `/images/create`
- `/images/json`

## Triggering Behavior
**Step 1.** Pull an image
```
curl -X POST "http://127.0.0.1:8082/images/create?fromImage=docker.io/library/ubuntu&tag=22.04"
```
**Response:** HTTP 200
```
{"status":"Download complete","progressDetail":{},"id":"7e49dc6156b0"}
{"status":"Pulling fs layer","progressDetail":{},"id":"9fa3e2b5204f"}
{"status":"Download complete","progressDetail":{},"id":"9fa3e2b5204f"}
{"status":"Download complete","progressDetail":{},"id":"9fa3e2b5204f"}
```
**Step 2.** Filter images by label (new-style filters)
```
curl --get "http://127.0.0.1:8082/images/json"   --data-urlencode 'filters={"label": ["org.opencontainers.image.ref.name=ubuntu", "org.opencontainers.image.version=22.04"]}'
```
## Buggy Response
HTTP 200.
```
[]
```

## Expected Response
HTTP 200.
```
[{"Id":"sha256:9fa3e2b5204f4fd5ae0d53dee5c367ac686a8a39685d9261b9d3d3c8a9cc8917","ParentId":"","RepoTags":["docker.io/library/ubuntu:22.04"],"RepoDigests":["docker.io/library/ubuntu@sha256:104ae83764a5119017b8e8d6218fa0832b09df65aae7d5a6de29a85d813da2fb","docker.io/library/ubuntu@sha256:1c4cc37c10c4678fd5369d172a4e079af8a28a6e6f724647ccaa311b4801c3c9"],"Created":1760376200,"Size":80430184,"SharedSize":0,"VirtualSize":80430184,"Labels":{"org.opencontainers.image.ref.name":"ubuntu","org.opencontainers.image.version":"22.04"},"Containers":0,"Names":["docker.io/library/ubuntu:22.04"],"Digest":"sha256:104ae83764a5119017b8e8d6218fa0832b09df65aae7d5a6de29a85d813da2fb","History":["docker.io/library/ubuntu:22.04"]}]
```

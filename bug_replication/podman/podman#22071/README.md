# podman#22071

## Description
The API rejects the 'platform' query parameter due to invalid multi-arch syntax parsing in the request URL. (HTTP 400)

## GitHub Issue URL
https://github.com/containers/podman/issues/22071

## Triggering Endpoint(s)
- `/libpod/build`

## Triggering Behavior
**Step 1.** POST build context (tar.gz) to `/libpod/build`
```
curl -X POST -H "Content-Type: application/tar" -H "Content-Encoding: gzip"  --data-binary "@context.tar.gz"   "http://127.0.0.1:8082/v4.0.0/libpod/build?platform=linux/arm64,linux/amd64" | jq
```
## Buggy Response
HTTP 400
```
{
  "cause": "invalid argument",
  "message": "failed to parse query parameter 'platform': \"linux/arm64,linux/amd64\": invalid platform syntax for --platform=\"linux/arm64,linux/amd64\": \"arm64,linux\" is an invalid component of \"linux/arm64,linux/amd64\": platform specifier component must match \"^[A-Za-z0-9_-]+$\": invalid argument",
  "response": 400
}
```
## Expected Response
HTTP 200
```
{"stream":"[linux/amd64] STEP 1/1: FROM scratch\n"}
{"stream":"[linux/amd64] COMMIT\n"}
{"stream":"Getting image source signatures\n"}
{"stream":"Copying config sha256:a8f811488f9d08e4ff455cd3cfe07b563bfdf906c18d71efba77d6566027d19c\n"}
{"stream":"Writing manifest to image destination\n"}
{"stream":"--> a8f811488f9d\n"}
{"stream":"[linux/arm64] STEP 1/1: FROM scratch\n"}
{"stream":"a8f811488f9d08e4ff455cd3cfe07b563bfdf906c18d71efba77d6566027d19c\n"}
{"stream":"[linux/arm64] COMMIT\n"}
{"stream":"Getting image source signatures\n"}
{"stream":"Copying config sha256:310402fc2bc8ccab043153fa74c3ddf2ab4e120b3641f5bd29cd06a8336e93e4\n"}
{"stream":"Writing manifest to image destination\n"}
{"stream":"--> 310402fc2bc8\n"}
{"stream":"310402fc2bc8ccab043153fa74c3ddf2ab4e120b3641f5bd29cd06a8336e93e4\n"}
```

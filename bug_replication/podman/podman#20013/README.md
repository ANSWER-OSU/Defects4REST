# podman#20013

## Description
The API response does not conform to the expected Docker schema as it lacks a "message" key at the root level causing client compatibility issues. (HTTP 401)

## GitHub Issue URL
https://github.com/containers/podman/issues/20013

## Triggering Endpoint(s)
- `/images/create`

## Triggering Behavior
**Step 1.** Pull and create an nonexistent image
```
curl -s -X POST "http://127.0.0.1:8082/v1.24/images/create?fromImage=quay.io/idonotexist/idonotexist:dummy"   | jq .
```

## Buggy Response
HTTP 401.
```
{
  "progressDetail": {},
  "errorDetail": {
    "message": "initializing source docker://quay.io/idonotexist/idonotexist:dummy: reading manifest dummy in quay.io/idonotexist/idonotexist: unauthorized: access to the requested resource is not authorized"
  },
  "error": "initializing source docker://quay.io/idonotexist/idonotexist:dummy: reading manifest dummy in quay.io/idonotexist/idonotexist: unauthorized: access to the requested resource is not authorized"
}
```

## Expected Response
HTTP 401.
```
{
  "message": "unauthorized: access to the requested resource is not authorized"
}
```

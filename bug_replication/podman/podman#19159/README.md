# podman#19159

## Description
The API error message regression occurs after an upgrade to 4.6.0-rc1 indicating a change in behavior tied to a specific version or environment. (HTTP 500)

## GitHub Issue URL
https://github.com/containers/podman/issues/19159

## Triggering Endpoint(s)
- `/libpod/pods/create`
- `/libpod/containers/create`
- `/libpod/containers/{container_id}/start`
- `/libpod/pods/{pod_id}`

## Triggering Behavior
**Step 1.** Create a pod
```
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data '{}' \
  "http://127.0.0.1:8082/v1.12/libpod/pods/create?name=d4rest_testpod"
```
**Response:** HTTP 200
```
  {"Id":"33eda54c906b50c00bb76f15c139856be60328a82dd78107a7d79563b018f847"}
```
**Step 2.** Create a container in the pod
```
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data '{
	"Name": "d4rest_foo_ctr",
    "Image": "alpine",
    "Command": [
        "sleep",
        "300"
    ],
    "Pod": "'"
}' \
  "http://127.0.0.1:8082/v1.12/libpod/containers/create"
```
**Response:** HTTP 200
```
{"Id":"96ade0e4b0b7b3343f81dc364ab58218277392cb3412b440c20db592b8758eb7","Warnings":[]}
```
*Step 3.* Start the container
```
curl -s -X POST "http://127.0.0.1:8082/v1.12/libpod/containers/96ade0e4b0b7b3343f81dc364ab58218277392cb3412b440c20db592b8758eb7/start"
```
**Response:** HTTP 204

**Step 4.** Delete the pod
```
curl -v -s -X DELETE \
  "http://127.0.0.1:8082/v1.12/libpod/pods/33eda54c906b50c00bb76f15c139856be60328a82dd78107a7d79563b018f847"
```

## Buggy Response
```
{
  "cause": "removing pod containers",
  "message": "not all containers could be removed from pod 33eda54c906b50c00bb76f15c139856be60328a82dd78107a7d79563b018f847: removing pod containers",
  "response": 500
}
```
## Expected Response
```
{
  "cause": "removing pod containers",
  "message": "not all containers could be removed from pod f2ae10cbebc881028d35e768ace0e03e57c0aff0276f0d54c99d8589091befa0: removing pod containers. 2 errors occurred:\n\t* cannot remove container e53d46811c91ec176b5ba52fd64d732c7012a01121ed4daf61fc9508e9a3682c as it is running - running or paused containers cannot be removed without force: container state improper\n\t* a container that depends on container 6e7248b76ae3392c2886b38807521674dd0a71421bf9409e1afc1f8ecc377a9c still exists: dependency exists\n\n",
  "response": 500
}
```

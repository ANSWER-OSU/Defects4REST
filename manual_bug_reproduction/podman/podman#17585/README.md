# podman#17585

## Description
Podman REST API returns HTTP 500 instead of Docker's HTTP 409 when creating an existing network causing compatibility issues with tools expecting Docker behavior.

## GitHub Issue URL
https://github.com/containers/podman/issues/17585

## Triggering Endpoint(s)
- `/networks/create`

## Triggering Behavior
**Step 1.** Create a network
```
curl -i -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"Name": "d4rest_supabase_default"}' \
  "http://127.0.0.1:8082/v1.40/networks/create"
```
**Response:** HTTP 201
```
{"Id":"7dde38bbad8d4f0c3be094fcabc22311cca4b6a45c076321381329c219a1b4bf","Warning":""}
```

**Step 2.** Create existing network
```
curl -i -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"Name": "d4rest_supabase_default"}' \
  "http://127.0.0.1:8082/v1.40/networks/create"
```
## Buggy Response
HTTP 500.
```
{"cause":"network already exists","message":"network name d4rest_supabase_default already used: network already exists","response":500}
```

## Expected Response
HTTP 200
```
{"Id":"7dde38bbad8d4f0c3be094fcabc22311cca4b6a45c076321381329c219a1b4bf","Warning":""}
```

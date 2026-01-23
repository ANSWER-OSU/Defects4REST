## signal-cli-rest-api#387

## Description

Group deletion via the REST API in a containerized environment does not remove the group despite a successful response indicating a failure in group handling.

## GitHub Issue URL

[https://github.com/bbernhard/signal-cli-rest-api/issues/387](https://github.com/bbernhard/signal-cli-rest-api/issues/387)

## Triggering Endpoint:

* `/v1/groups/{number}`
* `/v1/groups/{number}/{groupid}`

## **Prerequisites**

-   A registered Signal number inside the container
-   Base URL and number set as env vars:

```jsx
BASE="<http://localhost:8080>"
NUMBER="+1xxxxx" # replace with your registered number

```

All commands below assume those two variables are set in your shell.

## Triggering Behavior:

**Step 1.** Create a group with an empty name and a single member

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"name": "", "members": ["+5412244760"]}' \
  "http://localhost:8080/v1/groups/+5412244760"
```

**Response:** HTTP 200 with groupid = roup.dHlqaE1EWTBOek13TURFeU9EQTRPRGN4TnpNMw=="

**Step 2.** Delete the group
```bash
curl -v -X DELETE -H "Content-Type: application/json" \
"http://localhost:8080/v1/groups/+5412244760/group.dHlqaE1EWTBOek13TURFeU9EQTRPRGN4TnpNMw=="
```

**Buggy Response:** HTTP 500 error

**Expected Response:** group gets deleted

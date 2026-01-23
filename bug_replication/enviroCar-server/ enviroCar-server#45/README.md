## enviroCar-server#45

## Description

The issue concerns the inability to delete user accounts via the API which is a core account lifecycle operation.


## GitHub Issue URL

[http://github.com/enviroCar/enviroCar-server/issues/45](http://github.com/enviroCar/enviroCar-server/issues/45)

## Triggering Endpoints:

* `/users`
* `/users/{username}`

## Triggering Behavior:

**Step 1.** Create user 

```bash
curl -X POST "http://localhost:8080/rest/users" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "bugtest_1",
        "mail": "bugtest_1@example.com",
        "token": "myplaintoken123"
      }'
```
**Step 2.** Verify user exists 

```bash
curl -X GET "http://localhost:8080/rest/users/bugtest_<timestamp>"
```

**Step 3.** Delete user

```bash
curl -X DELETE "http://localhost:8080/rest/users/bugtest_1" \
  -H "X-User: bugtest_1" \
  -H "X-Token: myplaintoken123" \
```
**Buggy Response:** 

Time elapsed: 9s

HTTP Response Code: 500


**Expected Response:** 

Time elapsed < 2s

TTP/1.1 204 No Content


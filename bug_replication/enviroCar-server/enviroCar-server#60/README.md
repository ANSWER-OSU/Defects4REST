# enviroCar-server#60

## Description
HTTP 500 error is caused by a null parameter 'vals' in a query filter method leading to an assertion failure in the Morphia query API.

## GitHub Issue URL
https://github.com/enviroCar/enviroCar-server/issues/60

## Triggering Endpoint(s)
- `/users`
- `/users/{name}/friendActivities`

## Triggering Behavior
**Step 1.** Create a user
```
curl --request POST \
  --url http://localhost:8080/rest/users \
  --header 'content-type: application/json' \
  --data '{
  "name": "testuser",
  "mail": "user@example.com",
  "token": "foo"
}'
```
**Response:** HTTP 201 Created

**Step 2.** Retrieve friend activities of the user
```
curl -u testuser:foo --request GET \
  --url http://localhost:8080/rest/users/testuser/friendActivities
```

## Buggy Response
HTTP 500
```
{
  "servlet": "default",
  "cause0": "com.github.jmkgreen.morphia.utils.Assert$AssertionFailedException: Parameter &apos;vals&apos;  is null.",
  "message": "com.github.jmkgreen.morphia.utils.Assert$AssertionFailedException: Parameter &apos;vals&apos;  is null.",
  "url": "/rest/users/testuser/friendActivities",
  "status": "500"
}
```
## Expected Response
HTTP 200
```
{
  "activities": []
}
```
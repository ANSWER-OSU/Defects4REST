# enviroCar-server#52

## Description
Server returns 500 error instead of 409 when creating a user with an already used email indicating improper validation and error handling in the POST request.

## GitHub Issue URL
https://github.com/enviroCar/enviroCar-server/issues/52

## Triggering Endpoint(s)
- `/users`

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
**Step 2.** Create a new user with existing email
```
curl --request POST \
  --url http://localhost:8080/rest/users \
  --header 'content-type: application/json' \
  --data '{
  "name": "newuser",
  "mail": "user@example.com",
  "token": "foo"
}'
```

## Buggy Response
HTTP 500
```
{
  "servlet": "default",
  "cause0": "com.mongodb.MongoException$DuplicateKey: { &quot;serverUsed&quot; : &quot;mongodb/172.18.0.2:27017&quot; , &quot;connectionId&quot; : 14 , &quot;err&quot; : &quot;E11000 duplicate key error collection: envirocar.users index: mail_1 dup key: { : \\&quot;user@example.com\\&quot; }&quot; , &quot;code&quot; : 11000 , &quot;codeName&quot; : &quot;DuplicateKey&quot; , &quot;n&quot; : 0 , &quot;ok&quot; : 1.0}",
  "message": "com.mongodb.MongoException$DuplicateKey: { &quot;serverUsed&quot; : &quot;mongodb/172.18.0.2:27017&quot; , &quot;connectionId&quot; : 14 , &quot;err&quot; : &quot;E11000 duplicate key error collection: envirocar.users index: mail_1 dup key: { : \\&quot;user@example.com\\&quot; }&quot; , &quot;code&quot; : 11000 , &quot;codeName&quot; : &quot;DuplicateKey&quot; , &quot;n&quot; : 0 , &quot;ok&quot; : 1.0}",
  "url": "/rest/users",
  "status": "500"
}
```

## Expected Response
HTTP 409
```
{
  "servlet": "default",
  "message": "Conflict",
  "url": "/rest/users",
  "status": "409"
}
```
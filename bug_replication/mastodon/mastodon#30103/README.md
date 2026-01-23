## mastodon#30103

## Description
Multiple push notification subscriptions are not properly replacing previous ones as documented leading to duplicate notifications for the same account session.



## GitHub Issue URL

[
https://github.com/mastodon/mastodon/issues/30103
](
https://github.com/mastodon/mastodon/issues/30103
)

## Triggering Endpoints:

* `/v1/push/subscription`
* `/v1/statuses`

## Triggering Behavior:

**Step 1:** Create two users (USER1 and USER2) and get their authentication keys. (Note this is the part of the defect initialization and we expect testing tools to take as input both auth keys and detect this bug) 

**Step 2:** Generate many concurrent subscription requests using USER1's auth key. 


```bash
for i in {1..80}; do
  curl -s -X POST "https://localhost:3000/api/v1/push/subscription" \
    -H "Authorization: Bearer 6xc9v0A9UurrWRcr3MrBvU6M2vPq8LWZvci10ZjZC0xMj " \
    -H "Content-Type: application/json" \
    -d '{
          "subscription": {
            "endpoint": "https://example.com/push/notify/12345",
            "keys": {
              "p256dh": "BOPs8xV5Pvjb3Jp2iVJxFJFGf3xc9v0A9UuNWc3M3BvU6M2vPq8-4mVnC8o1yHIf2S6JZx9o7vNQkB_3bMdX8K8",
              "auth":   "abc123XYZ890="
            }
          },
          "data": { "alerts": { "mention": true } }
        }' &
done
```

**Step 3:** Using USER2' auth key mention USER1:

```bash
curl -X POST "https://localhost:3000/api/v1/statuses" \
  -H "Authorization: Bearer MTA2MzQ0NTYtYWJjZC0xMjM0LWZha2UtYWNjZXNzLXRva2VuLWZvci10ZXN0aW5nLW9ubHk" \
  -H "Content-Type: application/json" \
  -d '{ "status": "@USER1 test notification" }'
```
**Step 4:** Check current subscription of USER1 account

```bash
curl "https://localhost:3000/api/v1/push/subscription" \
  -H "Authorization: Bearer xc9v0A9UurrWRcr3MrBvU6M2vPq8LWZvci10ZjZC0xMj"
```
**Response** HTTP  200  (https://example.com/push/notify/12345)

```bash
{
  "id": "1001",
  "endpoint": "https://example.com/push/notify/12345",
  "alerts": {
    "follow": false,
    "favourite": false,
    "reblog": false,
    "mention": true,
    "poll": false,
    "status": false
  },
  "server_key": "BJJ2pP9f2g_xxYxgkzvF6L5oVfXKXoKX8d-q4x7eWc8H8Xv3mR5hJHnL8l0Vt4dz1kYiD9v3wZb1o2k9Hqf6Qw"
}
```

**Step 5:** Delete current subscription of USER1

```bash
curl -X DELETE "https://localhost:3000/api/v1/push/subscription" \
  -H "Authorization: Bearer xc9v0A9UurrWRcr3MrBvU6M2vPq8LWZvci10ZjZC0xMj "
```

**Step 6:** Verify that current subscription of USER1 is deleted

```bash
curl "https://localhost:3000/api/v1/push/subscription" \
  -H "Authorization: Bearer xc9v0A9UurrWRcr3MrBvU6M2vPq8LWZvci10ZjZC0xMj"
```
**Buggy Response** HTTP 200 with the current subscription https://example.com/push/notify/12345

```bash
{
  "id": "1002",
  "endpoint": "https://example.com/push/notify/12345",
  "alerts": {
    "follow": false,
    "favourite": false,
    "reblog": false,
    "mention": true,
    "poll": false,
    "status": false
  },
  "server_key": "BJJ2pP9f2g_xxYxgkzvF6L5oVfXKXoKX8d-q4x7eWc8H8Xv3mR5hJHnL8l0Vt4dz1kYiD9v3wZb1o2k9Hqf6Qw"
}
```

**Expected Response:**
HTTP 200 with empty JSON body.


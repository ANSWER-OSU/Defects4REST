## signal-cli-rest-api#654

## Description

The `notify_self` query parameter is not handled consistently for direct messages versus group chats resulting in unexpected behavior.

## GitHub Issue URL

[https://github.com/bbernhard/signal-cli-rest-api/issues/654](https://github.com/bbernhard/signal-cli-rest-api/issues/654)

## Triggering Endpoint:

* `/v2/send`

## Triggering Behavior:

**Step 1.** Send message to a direct recipient

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "message": "Hello World!",
    "number": "+15412244750",
    "recipients": ["group.SDh0aW9PbVUzeTL0VqND0="],
    "notify_self": false
  }' \
  'http://127.0.0.1:8999/v2/send'
```

**Buggy Response:** HTTP Status 200 OK but you still receive your own message despite `notify_self` set to false

**Expected Response:** HTTP Status 200 and not receiving your own message

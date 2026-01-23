## mastodon#30039

## Description
Idempotency-Key header is ignored in POST /api/v1/statuses causing duplicate scheduled posts indicating a failure in REST API middleware handling of idempotency.


## GitHub Issue URL

[
https://github.com/mastodon/mastodon/issues/30039
](
https://github.com/mastodon/mastodon/issues/30039
)

## Triggering Endpoints:

* `/statuses`
* `/scheduled_statuses`

## Triggering Behavior:

**Step 1.** Send 3 consecutive POST requests to /api/v1/statuses all with the same Idempotency-Key header. Each request tries to schedule the same post for one hour in the future. 

```bash
TOKEN="79xgaTFLuIOCbm0tialgwdrSyVs9OcJMdhKSynClSh0"
IDEMPOTENCY_KEY="test-key-$(date +%s)"
SCHEDULED_TIME=$(date -u -d '+1 hour' +"%Y-%m-%dT%H:%M:%S.000Z")
for i in 1 2 3; do
  echo "Making request $i..."
  curl -s http://localhost:3000/api/v1/statuses \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "Idempotency-Key: $IDEMPOTENCY_KEY" \
    -d "{\"status\":\"Test post for idempotency bug\",\"visibility\":\"private\",\"scheduled_at\":\"$SCHEDULED_TIME\"}" | head -c 100
  echo ""
  echo "---"
  sleep 1
done
```

**Step 2.** Fetch all scheduled posts and count how many posts were created using the same key

```bash
SCHEDULED=$(curl -s http://localhost:3000/api/v1/scheduled_statuses \
  -H "Authorization: Bearer $TOKEN")
COUNT=$(echo "$SCHEDULED" | grep -o '"id"' | wc -l)
echo "RESULT: Found $COUNT scheduled post(s)"
```

**Buggy Response:** 
```bash
RESULT: Found 3 scheduled post(s)
```

**Expected Response:** 1 (same Idempotency-Key should create only 1 post)

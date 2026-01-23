# kafka-rest#37

## Description
API fails to handle a specific exception from the underlying consumer connector resulting in an incorrect HTTP 500 response.

## GitHub Issue URL
https://github.com/confluentinc/kafka-rest/issues/37

## Triggering Endpoint(s)
- `/consumers/{group_name}`
- `/consumers/{group_name}/instances/{instance_id}`
- `/consumers/{group_name}/instances/{instance_id}/topics/{topic_name}`

## Triggering Behavior
**Step 1.** Create a single consumer instance
```
curl -X POST http://localhost:8082/consumers/mygroup \
  -H "Content-Type: application/vnd.kafka.v1+json" \
  -d '{
    "name": "consumer1",
    "format": "binary",
    "auto.offset.reset": "smallest"
  }'
```
**Response:** HTTP 200.
```
{
    "instance_id": "consumer1",
    "base_uri": "http://localhost:8082/consumers/mygroup/instances/consumer1"
}
```

**Step 2.** First topic read
```
curl -X GET \
  -H "Accept: application/vnd.kafka.binary.v1+json" \
  http://localhost:8082/consumers/mygroup/instances/consumer1/topics/topicA
```
**Response:** HTTP 500

**Step 3.** Second topic read
```
curl -X GET \
  -H "Accept: application/vnd.kafka.binary.v1+json" \
  http://localhost:8082/consumers/mygroup/instances/consumer1/topics/topicA
```

## Buggy response
HTTP 500 Internal Server Error

## Expected response
HTTP 409 Conflict
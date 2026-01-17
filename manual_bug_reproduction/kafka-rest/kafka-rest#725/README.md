# kafka-rest#475

## Description
GET request with offset and count parameters returns incorrect messages (HTTP 200) when topic data is compressed indicating improper handling of query parameters with compressed data.

## GitHub Issue URL
https://github.com/confluentinc/kafka-rest/issues/475

## Triggering Endpoint(s)
- `/topics/{topic_name}/partitions/{partition_id}`

## Triggering Behavior
**Step 1.** Request offsets inside a compressed batch.
```
curl -s \
  "http://localhost:8082/topics/compressed-topic/partitions/0/messages?offset=10&count=1" \
  | jq
```
## Buggy Response:
HTTP 200 - Offset is 0
```
[
  {
    "topic": "compressed-topic",
    "key": null,
    "value": "bXNnLTE=",
    "partition": 0,
    "offset": 0
  }
]
```
## Expected Response: 
HTTP 200 - Return the first offset of the batch
```
[
  {
    "topic": "compressed-topic",
    "key": null,
    "value": "bXNnLTE=",
    "partition": 0,
    "offset": 10
  }
]
```

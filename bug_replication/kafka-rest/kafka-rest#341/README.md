# kafka-rest#341

## Description
Multiple consumer instances in the same group experience long delays in message reads indicating issues with partition assignment or group coordination in the distributed system.

## GitHub Issue URL

## Triggering Endpoint(s)
- `/topics/{topic_name}`
- `/consumers/{group_name}`
- `/consumers/{group_name}/instances/{instance_id}/subscription`
- `/consumers/{group_name}/instances/{instance_id}/records`

## Triggering Behavior
**Step 1.** Produce a few messages to a topic "test1"
```
curl -s -X POST "http://localhost:8082/topics/test1" \
 -H "Content-Type: application/vnd.kafka.json.v2+json" \
 -d '{
	 "records":[
		{"value":{"k":1,"msg":"m1"}},
		{"value":{"k":2,"msg":"m2"}},
		{"value":{"k":3,"msg":"m3"}}
	 ]
}'
```
**Response:** HTTP 200.
```
{
  "offsets": [
    {
      "partition": 0,
      "offset": 0,
      "error_code": null,
      "error": null
    },
    {
      "partition": 0,
      "offset": 1,
      "error_code": null,
      "error": null
    },
    {
      "partition": 0,
      "offset": 2,
      "error_code": null,
      "error": null
    }
  ],
  "key_schema_id": null,
  "value_schema_id": null
}
```

**Step 2.** Create two consumer instances (`my_consumer_instance1` and `my_consumer_instance2`) in the SAME group `my_json_consumer1"`

- `my_consumer_instance1` 
```
curl -s -H "Content-Type: application/vnd.kafka.v2+json" \
 -d '{"name":"my_consumer_instance1","format":"json","auto.offset.reset":"earliest"}' \
 http://localhost:8082/consumers/my_json_consumer1 | jq .
```
**Response:** HTTP 200.
```
{
  "instance_id": "my_consumer_instance1",
  "base_uri": "http://kafka-rest:8082/consumers/my_json_consumer1/instances/my_consumer_instance1"
}
```
- `my_consumer_instance2`
```
curl -s -H "Content-Type: application/vnd.kafka.v2+json" \
 -d '{"name":"my_consumer_instance2","format":"json","auto.offset.reset":"earliest"}' \
 http://localhost:8082/consumers/my_json_consumer1 | jq .
```
**Response:** HTTP 200.
```
{
  "instance_id": "my_consumer_instance2",
  "base_uri": "http://kafka-rest:8082/consumers/my_json_consumer1/instances/my_consumer_instance2"
}
```
**Step 3.** Subscribe BOTH instances to the same topic "test1"

- `my_consumer_instance1`
```
curl -s -H "Content-Type: application/vnd.kafka.v2+json" \
 -d '{"topics":["test1"]}' \
http://localhost:8082/consumers/my_json_consumer1/instances/my_consumer_instance1/subscription
| jq .
```
**Response:** HTTP 204

- `my_consumer_instance2`
```
curl --request POST \
  --url http://localhost:8082/consumers/my_json_consumer1/instances/my_consumer_instance2/subscription \
  --header 'content-type: application/vnd.kafka.v2+json' \
  --data '{
  "topics": [
    "test1"
  ]
}'
```
**Response:** HTTP 204.

**Step 4.** Read the message from `my_consumer_instance1` several times and we will get responses back:
```
curl -s -X GET -H "Accept: application/vnd.kafka.json.v2+json" \
 http://localhost:8082/consumers/my_json_consumer1/instances/my_consumer_instance1/records
 
curl -s -X GET -H "Accept: application/vnd.kafka.json.v2+json" \
 http://localhost:8082/consumers/my_json_consumer1/instances/my_consumer_instance1/records
```
**Response:** HTTP 200.
```
[
  {
    "topic": "test1",
    "key": null,
    "value": {
      "k": 1,
      "msg": "m1"
    },
    "partition": 0,
    "offset": 0
  },
  {
    "topic": "test1",
    "key": null,
    "value": {
      "k": 2,
      "msg": "m2"
    },
    "partition": 0,
    "offset": 1
  },
  {
    "topic": "test1",
    "key": null,
    "value": {
      "k": 3,
      "msg": "m3"
    },
    "partition": 0,
    "offset": 2
  }
]
```
**Step 5.** Read the message from my_consumer_instance2 and the call will hang. It will take around 8 minutes to get a response
```
curl -s -X GET -H "Accept: application/vnd.kafka.json.v2+json" \
 http://localhost:8082/consumers/my_json_consumer1/instances/my_consumer_instance2/records
```
**Response:** HTTP 200.

**Step 6.** Read again from instance1 - now this also “hangs”
```
curl -s -X GET -H "Accept: application/vnd.kafka.json.v2+json" \
 http://localhost:8082/consumers/my_json_consumer1/instances/my_consumer_instance1/records
```
## Buggy Response:
It takes 8 minutes to get HTTP 200 response
## Expected Response:
It should not take more than 2 seconds
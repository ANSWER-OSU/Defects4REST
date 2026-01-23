# **Flowable-engine#3536**

## Descriptions
Retrieving historic variable instances crashes when you prematurely stopping a process instance during a multi-instance execution.

## GitHub Issue URL
https://github.com/flowable/flowable-engine/issues/3536

## Triggering Endpoints
- /service/history/historic-variable-instances?processInstanceId={processInstanceId}

## Triggering Behavior
Step 1. Deploy the example model to flowable engine.
```
curl -u "rest-admin:test" --request POST \
 --url http://localhost:8080/flowable-rest/service/repository/deployments \
 --header 'content-type: multipart/form-data' \
 --form @=@ModelWithSubProcess.bpmn20.xml | jq .
```
**Response: **HTTP 201
```
{
 "id": "afb3784c-d054-11f0-8552-d6b62bc7d11b",
 "name": "ModelWithSubProcess",
 "deploymentTime": "2025-12-03T14:30:59.209Z",
 "category": null,
 "parentDeploymentId": "afb3784c-d054-11f0-8552-d6b62bc7d11b",
 "url": "http://localhost:8080/flowable-rest/service/repository/deployments/afb3784c-d054-11f0-8552-d6b62bc7d11b",
 "tenantId": ""
}
```
**Step 2.** Start the process instance
```
curl -u "rest-admin:test" --request POST \
 --url http://localhost:8080/flowable-rest/service/runtime/process-instances \
 --header 'content-type: application/json' \
 --data '{
 "processDefinitionKey": "ModelWithSubProcess"
}' | jq .
```
**Response:** HTTP 201.
```
{
 "id": "c0aba5b0-d054-11f0-8552-d6b62bc7d11b",
 "url": "http://localhost:8080/flowable-rest/service/runtime/process-instances/c0aba5b0-d054-11f0-8552-d6b62bc7d11b",
 "name": null,
 "businessKey": null,
 "businessStatus": null,
 "suspended": false,
 "ended": false,
 "processDefinitionId": "ModelWithSubProcess:1:afd705df-d054-11f0-8552-d6b62bc7d11b",
 "processDefinitionUrl": "http://localhost:8026/flowable-rest/service/repository/process-definitions/ModelWithSubProcess:1:afd705df-d054-11f0-8552-d6b62bc7d11b",
 "processDefinitionName": "ModelWithSubProcess",
 "processDefinitionDescription": null,
 "activityId": null,
 "startUserId": "rest-admin",
...
...
}
```
**Step 3.** Stop the process instance
```
curl -u "rest-admin:test" --request DELETE \
 --url http://localhost:8080/flowable-rest/service/runtime/process-instances/c0aba5b0-d054-11f0-8552-d6b62bc7d11b \
 --header ''\''accept: application/json'\''' \
 --header ''\''content-type: application/json'\''' \
 --header 'content-type: application/json' | jq .
```
**Response:** HTTP 204

Step 4. Retrieve the historic variables
```
curl -u "rest-admin:test" --request GET \
 --url 'http://localhost:8080/flowable-rest/service/history/historic-variable-instances?processInstanceId=c0aba5b0-d054-11f0-8552-d6b62bc7d11b' | jq .


```



**Buggy Response:** HTTP 500.
```
{
 "message": "Internal server error"
}
```


**Expected Response:** HTTP 200
```
{
 "data": [
   {
     "id": "9ecf193e-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf6760-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf6762-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecd6b7e-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf6764-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf8e78-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf8e7c-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf1939-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecf1937-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   },
   {
     "id": "9ecef225-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceId": "9e24f677-d057-11f0-bfd8-f64e0cff6474",
     "processInstanceUrl": "http://localhost:8080/flowable-rest/service/history/historic-process-instances/9e24f677-d057-11f0-bfd8-f64e0cff6474"
   }
 ],
 "total": 10,
 "start": 0,
 "sort": "variableName",
 "order": "asc",
 "size": 10
}


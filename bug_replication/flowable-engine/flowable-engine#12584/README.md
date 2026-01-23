## Flowable-engine#2584

## Description

The REST API no longer allows execution of 'move' or 'moveToHistoryJob' actions on jobs, which prevents expected workflow operations.

## GitHub Issue URL

[https://github.com/flowable/flowable-engine/issues/2584](https://github.com/flowable/flowable-engine/issues/2584)

## Triggering Endpoints:

* `/service/repository/deployments`
* `/runtime/process-instances`
* `/management/deadletter-jobs/{jobId}`

## Triggering Behavior:

**Step 1.** Deploy & start a failing async process (create and push dead-letter job to DLQ) to get a jobId:

```bash
curl -u rest-admin:test -H 'Content-Type: application/json' -X POST -d '{"processDefinitionKey":"deadletter_demo"}' http://localhost:8080/flowable-rest/service/runtime/process-instances
```

**Step 2.** Attempt `moveToHistoryJob` using the jobId:

```bash
curl -u rest-admin:test -H 'Content-Type: application/json' -X POST -d '{"action":"moveToHistoryJob"}' "http://localhost:8080/flowable-rest/service/management/deadletter-jobs/0ab42b73-ba8d-11f0-a976-0690f07036fc"
```

**Buggy Response:** HTTP 400 with action not allowed

```json
{
  "message":"Bad request",
  "exception":"Invalid action, only 'move' is supported."
}
```

**Expected Response:** HTTP 2XX, action allowed when a valid job id is created

```json
{
  "message":"Not found",
  "exception":"Could not find a job with id '0ab42b73-ba8d-11f0-a976-0690f07036fc'."
}
```




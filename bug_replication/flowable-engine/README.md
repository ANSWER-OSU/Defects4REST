# Flowable-engine Defects

This directory contains **5 replicable REST API bugs** documented from the [Flowable Engine](https://github.com/flowable/flowable-engine) project.

## Overview

Flowable Engine is an open-source workflow and business process management platform that provides REST APIs for managing processes, tasks, jobs, variables, and deployments across BPMN, CMMN, and DMN engines.

## Available Defects

The table below shows the available defects including the defect type, sub defect type, a description of each defect, and a link to the steps for replicating each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [1939](https://github.com/flowable/flowable-engine/issues/1939) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | API rejects the likeIgnoreCase operation for task variable queries indicating unsupported or inconsistent query parameter handling. | [Replication steps](./flowable-engine%231939/README.md) |
| [2584](https://github.com/flowable/flowable-engine/issues/2584) | Configuration and Environment Issues| Job Execution and Workflow Configuration Defects | The REST API no longer allows execution of `move` or `moveToHistoryJob` actions on jobs which prevents expected workflow operations. | [Replication steps](./flowable-engine%232584/README.md) |
| [3003](https://github.com/flowable/flowable-engine/issues/3003) | Data Storage, Access, and Volume Errors | Volume and File Upload/Access Errors | API returns incorrect media type for `.form` files which affects correct file access and handling. | [Replication steps](./flowable-engine%233003/README.md) |
| [3536](https://github.com/flowable/flowable-engine/issues/3536) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Querying historic variables without specifying variableName causes a server error specifically for `nrOfActiveInstances` and `nrOfCompletedInstances` after process termination. | [Replication steps](./flowable-engine%233536/README.md) |
| [3856](https://github.com/flowable/flowable-engine/issues/3856) | Integration, Middleware, and Runtime Environment Failures | Middleware Integration Failures in REST APIs | The REST API fails to serialize UUID variable types due to a missing converter in the backend integration logic resulting in null values in the response. | [Replication steps](./flowable-engine%233856/README.md) |



## Deploying, Managing, and Inspecting a Defect (Flowable-engine #1939)

> **Note:** Replace **1939** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p flowable-engine -i 1939 --buggy --start

# 2. Deploy the patched version of the issue 
defects4rest checkout -p flowable-engine -i 1939 --patched --start

# 3. Stop running containers
defects4rest checkout -p flowable-engine -i 1939 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p flowable-engine -i 1939 --clean

# 5. Get bug information
defects4rest info -p flowable-engine -i 1939

# 6. Check container logs if something goes wrong
docker logs flowable-engine
```

## Accessing Flowable-engine

Once deployed, the Flowable Engine service is accessible at:

* **Base URL:** `http://localhost:8080/flowable-rest`
* **Authentication:** Username = `rest-admin`, Password = `test`

The service requires HTTP Basic Authentication which is provided in the curl request for replication. Credentials are preconfigured, so no additional setup is needed.

## Troubleshooting

If the Flowable Engine service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs flowable-rest
```

Ensure that the required ports are free and that no conflicting services are running.

## References

* [Flowable Engine GitHub Repository](https://github.com/flowable/flowable-engine)
* [Flowable REST API Documentation](https://flowable.com/open-source/docs/bpmn/ch14-REST/)

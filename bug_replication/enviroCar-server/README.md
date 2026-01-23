# EnviroCar-server Defects for Defects4REST

This directory contains **4 replicable REST API bugs** documented from the [EnviroCar-server](https://github.com/enviroCar/enviroCar-server) project.
## Overview

EnviroCar-server is a RESTful API that provides environmental and vehicle data, including trips, sensor readings, and user-generated content.

## Available Defects

The table below shows the available defects including the defect type,sub defect type,  a description of each defect, and a link to the steps for replicating each defect.


| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [45](https://github.com/enviroCar/enviroCar-server/issues/45) | Authentication, Authorization, and Session Management Issues | Session, Token, and Account Lifecycle Management Errors | The issue concerns the inability to delete user accounts via the API, which is a core account lifecycle operation. | [Replication steps](./%20enviroCar-server%2345/README.md) |
| [52](https://github.com/enviroCar/enviroCar-server/issues/52) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The server returns a 500 error instead of 409 when creating a user with an already used email, indicating improper validation and error handling in the POST request. | [Replication steps](./enviroCar-server%2352/README.md) |
| [60](https://github.com/enviroCar/enviroCar-server/issues/60) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | A 500 error is caused by a null parameter (`vals`) in a query filter method, leading to an assertion failure in the Morphia query API. | [Replication steps](./enviroCar-server%2360/README.md) |
| [178](https://github.com/enviroCar/enviroCar-server/issues/178) | Integration, Middleware, and Runtime Environment Failures | Middleware Integration Failures in REST APIs | A redirect loop is caused by the interaction between the content negotiation filter and the schema resource endpoint. | [Replication steps](./enviroCar-server%23178/README.md) |



## Deploying, Managing, and Inspecting a Defect (EnviroCar-server #45)

> **Note:** Replace **45** with the desired **issue ID** if you want to deploy a different iisue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p enviroCar-server -i 45 --buggy --start

# 2. Deploy the patched version of the issue 
defects4rest checkout -p enviroCar-server -i 45 --patched --start

# 3. Stop running containers
defects4rest checkout -p enviroCar-server -i 45 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p enviroCar-server -i 45 --clean

# 5. Get bug information
defects4rest info -p enviroCar-server -i 45

# 6. Check container logs if something goes wrong
docker logs envirocar-server
```

## Accessing EnviroCar-server

Once deployed, the EnviroCar-server service is accessible at:

* **Base URL:** `http://localhost:8080`
* **Authentication:** Username = `dummy` and Password = `dummy` 

Authentication is already configured in the backend setup, so you do not need to provide or create credentials manually.

## Troubleshooting

If the EnviroCar-server service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs envirocar-server
docker logs envirocar-mongodb
```

Ensure that the required ports are free and that no conflicting services are running.

## References

* [EnviroCar-server GitHub Repository](https://github.com/enviroCar/enviroCar-server)


# Signal-CLI REST API Defects

This directory contains **3 replicable REST API bugs** documented from the [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) project.

## Overview

Signal-CLI REST API is a dockerized REST API wrapper around signal-cli, allowing you to send and receive Signal messages via HTTP requests. It provides endpoints for messaging, group management, and account operations.

## Available Defects

The table below shows the available defects including the defect type, sub defect type, description of each defect and a link to the steps for reproducing each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [387](https://github.com/bbernhard/signal-cli-rest-api/issues/387) | Runtime and Exception Handling Errors | Runtime Errors and Exception Handling | Group deletion via the REST API in a containerized environment returns 500 error despite the operation being valid. | [Replication steps](./signal-cli-rest-api%23387/README.md) |
| [654](https://github.com/bbernhard/signal-cli-rest-api/issues/654) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The notify_self query parameter is not handled consistently for direct messages versus group chats resulting in unexpected behavior. | [Replication steps](./signal-cli-rest-api%23654/README.md) |
| [657](https://github.com/bbernhard/signal-cli-rest-api/issues/657) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | Group description is missing from API responses only in the Docker container environment despite being present in the official documentation. | [Replication steps](./signal-cli-rest-api%23657/README.md) |

## Deploying, Managing, and Inspecting a Defect (Signal-CLI REST API #387)

> **Note:** Replace **387** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p signal-cli-rest-api -i 387 --buggy --start

# 2. Deploy the patched version of the issue
defects4rest checkout -p signal-cli-rest-api -i 387 --patched --start

# 3. Stop running containers
defects4rest checkout -p signal-cli-rest-api -i 387 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p signal-cli-rest-api -i 387 --clean

# 5. Get bug information
defects4rest info -p signal-cli-rest-api -i 387

# 6. Check container logs if something goes wrong
docker logs signal-cli-rest-api
```

## Accessing Signal-CLI REST API

Once deployed, the Signal-CLI REST API service is accessible at:

* **Base URL:** `http://localhost:8080`
* **API Docs:** `http://localhost:8080/v1/api-docs`
* **Authentication:** Not required

### Prerequisites

Before testing, you need a registered Signal number inside the container:

```bash
# Set environment variables for convenience
BASE="http://localhost:8080"
NUMBER="+1XXXXXXXXXX"  # Replace with your registered number
```

### Example API Calls

```bash
# List all groups for a number
curl -X GET "http://localhost:8080/v1/groups/<NUMBER>"

# Send a message
curl -X POST -H "Content-Type: application/json" \
  -d '{"message": "Hello", "number": "<NUMBER>", "recipients": ["<RECIPIENT>"]}' \
  "http://localhost:8080/v2/send"
```

## Troubleshooting

If the Signal-CLI REST API service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs signal-cli-rest-api
```

Ensure that the required ports are free and no conflicting services are running.

## References

* [Signal-CLI REST API GitHub Repository](https://github.com/bbernhard/signal-cli-rest-api)
* [Signal-CLI Documentation](https://github.com/AsamK/signal-cli)

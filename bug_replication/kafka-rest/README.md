# Kafka REST Defects for Defects4REST

This directory contains **3 replicable REST API bugs** documented from the [Kafka REST](https://github.com/confluentinc/kafka-rest) project.
## Overview

Kafka REST Proxy is a service that exposes a Kafka cluster through a RESTful HTTP API, allowing applications to produce and consume messages, inspect topics and consumer groups, and perform basic administrative operations without using Kafka’s native protocol or client libraries.

## Available Defects

The table below shows the available defects including the defect type,sub defect type,  a description of each defect, and a link to the steps for replicating each defect.


| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [37](https://github.com/confluentinc/kafka-rest/issues/37) | Integration, Middleware, and Runtime Environment Failures | Middleware Integration Failures in REST APIs | API fails to handle a specific exception from the underlying consumer connector resulting in an incorrect HTTP 500 response. | [Replication steps](./kafka-rest%2337/README.md) |
| [341](https://github.com/confluentinc/kafka-rest/issues/341) | Distributed Systems and Clustering Failures | Index and Cluster Coordination Failures | Multiple consumer instances in the same group experience long delays in message reads indicating issues with partition assignment or group coordination in the distributed system. | [Replication steps](./kafka-rest%23341/README.md) |
| [475](https://github.com/confluentinc/kafka-rest/issues/475) | Distributed Systems and Clustering Failures | Query Filter and Search Parameter Handling Errors | GET request with offset and count parameters returns incorrect messages when topic data is compressed indicating improper handling of query parameters with compressed data. | [Replication steps](./kafka-rest%23725/README.md) |



## Deploying, Managing, and Inspecting a Defect (kafka-rest #475)

> **Note:** Replace **475** with the desired **issue ID** if you want to deploy a different iisue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p kafka-rest -i 475 --buggy --start

# 2. Deploy the patched version of the issue 
defects4rest checkout -p kafka-rest -i 475 --patched --start

# 3. Stop running containers
defects4rest checkout -p kafka-rest -i 475 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p kafka-rest -i 475 --clean

# 5. Get bug information
defects4rest info -p kafka-rest -i 475

# 6. Check container logs if something goes wrong
docker logs kafka-rest

```

## Accessing Kafka REST

Once deployed, the Kafka REST service is accessible at:

* **Base URL:** `http://localhost:8082`

## Troubleshooting

If the Kafka REST service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs kafka-rest
docker logs kafka-broker
docker logs kafka-zookeper
docker logs schema-registry
```

Ensure that the required ports are free and that no conflicting services are running.

## References

* [Kafka REST GitHub Repository](https://github.com/confluentinc/kafka-rest)


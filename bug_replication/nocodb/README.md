# NocoDB Defects for Defects4REST

This directory contains **6 replicable REST API bugs** documented from the [NocoDB](https://github.com/nocodb/nocodb) project.
## Overview

NocoDB is a no-code database platform that allows teams to collaborate and build processes with ease of a familiar and intuitive spreadsheet interface. This allows even non-developers or business users to become software creators.

## Available Defects

The table below shows the available defects including the defect type,sub defect type,  a description of each defect, and a link to the steps for replicating each defect.


| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
[1756](https://github.com/nocodb/nocodb/issues/1756) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Filtering on linked record columns returns incorrect results indicating the filter logic for query parameters is faulty. | [Replication step](./nocodb/nocodb%231756/README.md) |
[1866](https://github.com/nocodb/nocodb/issues/1866) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Using lookup columns in filters or formulas causes errors indicating the API does not handle these query parameters correctly. | [Replication step](./nocodb/nocodb%231866/README.md) |
[1981](https://github.com/nocodb/nocodb/issues/1981) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API does not correctly interpret the '*' wildcard in the nested fields query parameter resulting in incomplete field selection. | [Replication step](./nocodb/nocodb%231981/README.md) |
[2242](https://github.com/nocodb/nocodb/issues/2242) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API response for a field with thousands of linked records is truncated without pagination or a way to retrieve all connections indicating improper handling of large result sets and missing query parameters for pagination. | [Replication step](./nocodb/nocodb%232242/README.md) |
[2776](https://github.com/nocodb/nocodb/issues/2776) | Functional Defect | Runtime and Dependency Errors | The API fails with a TypeError due to attempting to read 'endsWith' on null indicating a runtime code issue in MysqlClient. | [Replication step](./nocodb/nocodb%232776/README.md) |
[7535](https://github.com/nocodb/nocodb/issues/7535) | Data Storage, Access, and Volume Errors | Database/Table User Access Handling Errors | Viewer users receive HTTP 403 errors and cannot access email notification features due to insufficient permissions on the base and plugins. | [Replication step](./nocodb/nocodb%237535/README.md) |




## Deploying, Managing, and Inspecting a Defect (nocodb#1866)

> **Note:** Replace **1866** with the desired **issue ID** if you want to deploy a different iisue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p nocodb -i 1866 --buggy --start

# 2. Deploy the patched version of the issue (optional)
defects4rest checkout -p nocodb -i 1866 --patched --start

# 3. Stop running containers
defects4rest checkout -p nocodb -i 1866 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p nocodb -i 1866 --clean

# 5. Get bug information
defects4rest info -p nocodb -i 1866

# 6. Check container logs if something goes wrong
docker logs nocodb

```

## Accessing NocoDB

Once deployed, the NocoDB service is accessible at:

* **Base URL:** `http://localhost:8080`

Note: Defects4REST uses port 8080 for NocoDB by default, but is flexible if port 8080 is used (e.g. can automatically use 8081, 8082, etc).

## Troubleshooting

If the NocoDB service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs nocodb
```

Ensure that the required ports are free and that no conflicting services are running.

## References

* [NocoDB GitHub Repository](https://github.com/nocodb/nocodb)


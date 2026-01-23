# Podman Defects for Defects4REST

This directory contains **23 replicable REST API bugs** documented from the [Podman](https://github.com/containers/podman) project.

## Overview

Podman (the POD MANager) is a tool for managing containers and images, volumes mounted into those containers, and pods made from groups of containers. Podman runs containers on Linux, but can also be used on Mac and Windows systems using a Podman-managed virtual machine. Podman is based on libpod, a library for container lifecycle management that is also contained in this repository. The libpod library provides APIs for managing containers, pods, container images, and volumes.

## Available Defects

The table below shows the available defects including the defect type,sub defect type,  a description of each defect, and a link to the steps for replicating each defect.


| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
[13831](https://github.com/containers/podman/issues/13831) | Data Storage, Access, and Volume Errors | Volume and File Upload/Access Errors | The API build fails because it cannot find the Dockerfile or Containerfile at the expected file path during the remote build process. | [Replication step](./podman/podman%2313831/README.md) |
[13986](https://github.com/containers/podman/issues/13986) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API rejects valid status filter values like removing and restarting resulting in incorrect query parameter handling. | [Replication step](./podman/podman%2313986/README.md) |
[14208](https://github.com/containers/podman/issues/14208) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | Podman API incorrectly returns HTTP 500 instead of the expected HTTP 409 on image conflict which breaks compatibility with Docker API clients. | [Replication step](./podman/podman%2314208/README.md) |
[14647](https://github.com/containers/podman/issues/14647) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | Content-Type header is incorrectly set to text/plain instead of application/json only when the container list is empty indicating environment-specific response behavior. | [Replication step](./podman/podman%2314647/README.md) |
[15720](https://github.com/containers/podman/issues/15720) | Data Storage, Access, and Volume Errors | Volume and File Upload/Access Errors | RefCount for volumes in the REST API always returns 1 regardless of actual usage indicating incorrect volume usage tracking. | [Replication step](./podman/podman%2315720/README.md) |
[15828](https://github.com/containers/podman/issues/15828) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API does not return the correct 404 status when the fromImage query parameter references a nonexistent image. | [Replication step](./podman/podman%2315828/README.md) |
[17204](https://github.com/containers/podman/issues/17204) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | Test intermittently fails on specific Fedora environment with attach API returning empty content instead of expected output. | [Replication step](./podman/podman%2317204/README.md) |
[17524](https://github.com/containers/podman/issues/17524) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API response for the "Titles" field returns a single string instead of an array only when accessed via the podman socket in a specific environment and version. | [Replication step](./podman/podman%2317524/README.md) |
[17542](https://github.com/containers/podman/issues/17542) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API fails to handle negative timeout query parameters as allowed by the Docker spec resulting in a parameter parsing error. | [Replication step](./podman/podman%2317542/README.md) |
[17585](https://github.com/containers/podman/issues/17585) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | Podman REST API returns HTTP 500 instead of Docker's HTTP 409 when creating an existing network causing compatibility issues with tools expecting Docker behavior. | [Replication step](./podman/podman%2317585/README.md) |
[17763](https://github.com/containers/podman/issues/17763) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | Podman’s REST API omits the image tag in the /history endpoint response while Docker returns it under the same environment and API version. | [Replication step](./podman/podman%2317763/README.md) |
[17778](https://github.com/containers/podman/issues/17778) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Podman rejects POST requests with a string value for the pull field that Docker accepts due to stricter schema validation. | [Replication step](./podman/podman%2317778/README.md) |
[17869](https://github.com/containers/podman/issues/17869) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The API response uses "Id" instead of the expected "id" field causing schema incompatibility with clients expecting the correct field name. | [Replication step](./podman/podman%2317869/README.md) |
[18092](https://github.com/containers/podman/issues/18092) |Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API fails to return expected images when filtering by label using a specific filter format indicating incorrect handling of query filter parameters. | [Replication step](./podman/podman%2318092/README.md) |
[18424](https://github.com/containers/podman/issues/18424) | Integration, Middleware, and Runtime Environment Failures | Process Signal and Grouping Issues in Containerized APIs | ExecIDs incorrectly report as running long after the process has exited indicating a failure in tracking or updating process state within the container. | [Replication step](./podman/podman%2318424/README.md) |
[19159](https://github.com/containers/podman/issues/19159) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs     | The API error message regression occurs after an upgrade to 4.6.0-rc1 indicating a change in behavior tied to a specific version or environment. | [Replication step](./podman/podman%2319159/README.md) |
[19368](https://github.com/containers/podman/issues/19368) | Integration, Middleware, and Runtime Environment Failures | Process Signal and Grouping Issues in Containerized APIs | API returns incorrect status code when attempting to send a kill signal to a stopped container which is a process signal handling issue. | [Replication step](./podman/podman%2319368/README.md) |
[20013](https://github.com/containers/podman/issues/20013) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The API response does not conform to the expected Docker schema as it lacks a "message" key at the root level causing client compatibility issues. | [Replication step](./podman/podman%2320013/README.md) |
[20375](https://github.com/containers/podman/issues/20375) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs     | Podman's REST API returns a different and incorrect "Size" value compared to Docker for the same image history endpoint under the same environment. | [Replication step](./podman/podman%2320375/README.md) |
[22071](https://github.com/containers/podman/issues/22071) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API rejects the 'platform' query parameter due to invalid multi-arch syntax parsing in the request URL. | [Replication step](./podman/podman%2322071/README.md) |
[23981](https://github.com/containers/podman/issues/23981) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The issue reports that the API returns a list of strings instead of the expected list of lists of strings which is a payload structure mismatch. | [Replication step](./podman/podman%2323981/README.md) |
[24886](https://github.com/containers/podman/issues/24886) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API request fails with 500 error because the JSON payload includes -1 for a field defined as uint64 which cannot accept negative values. | [Replication step](./podman/podman%2324886/README.md) |
[25881](https://github.com/containers/podman/issues/25881) | Configuration and Environment Issues |  Container and Resource Quota Handling Errors             | In rootless mode the REST API fails to enforce ulimit settings for containers even though the CLI applies them correctly. | [Replication step](./podman/podman%2325881/README.md) |


## Deploying, Managing, and Inspecting a Defect (podman#25881)

> **Note:** Replace **25881** with the desired **issue ID** if you want to deploy a different issue.

- Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
sudo -E venv/bin/defects4rest checkout -p podman -i 25881 --buggy --start

# 2. Deploy the patched version of the issue (optional)
sudo -E venv/bin/defects4rest checkout -p podman -i 25881 --patched --start

# 3. Stop running containers
sudo -E venv/bin/defects4rest checkout -p podman -i 25881 --stop

# 4. Full cleanup (stop + remove volumes/networks)
sudo -E venv/bin/defects4rest checkout -p podman -i 25881 --clean

# 5. Get bug information
sudo -E venv/bin/defects4rest info -p podman -i 25881

# 6. Verify
podman version

```

## Accessing Podman

Once deployed, the Podman service is accessible at:

* **Base URL:** `http://127.0.0.1:8082`

## Troubleshooting

If the Podman service fails to start or behaves unexpectedly, inspect the terminal output produced by the Defects4REST CLI during deployment. Most setup and runtime errors (e.g., missing dependencies, build failures, permission issues) are reported directly there.

## References

* [Podman GitHub Repository](https://github.com/containers/podman)


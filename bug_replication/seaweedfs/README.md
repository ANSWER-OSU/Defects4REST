# SeaweedFS Defects for Defects4REST

This directory contains **9 replivable REST API bugs** documented from the [SeaweedFS](https://github.com/seaweedfs/seaweedfs) project.

---

### Prerequisites

Install **Go 1.22.x** (required for SeaweedFS):

```bash
cd /tmp
wget https://go.dev/dl/go1.22.6.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.6.linux-amd64.tar.gz
```

Add Go to your PATH for the current shell:

```bash
export PATH=$PATH:/usr/local/go/bin
```

(Optional) persist PATH:

```bash
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
```

Verify installation:

```bash
go version
```



## Overview

SeaweedFS is a **fast, simple, and highly scalable distributed file system** that provides REST APIs for managing files, volumes, buckets, and cluster coordination.
This collection of defects covers volume allocation, file access, payload validation, cluster coordination, and query parameter handling.



## Available Defects

The table below shows the available defects including the defect type, sub defects type, a description of each defect, and a link to the steps for replicating each defect.

|                         Issue ID #                         | Defect Type          | Sub Defect Type                                   | Description                                                                                                                                                                   | Replication                                       |
| :--------------------------------------------------------: | -------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
|  [913](https://github.com/seaweedfs/seaweedfs/issues/913)  | Configuration and Environment Issues  | Container and Resource Quota Handling Errors      | API fails to allocate all requested volumes and reports inconsistent free volume counts indicating issues with resource quota enforcement.                                    | [Replication Steps](./seaweedfs%23913/README.md)  |
| [1776](https://github.com/seaweedfs/seaweedfs/issues/1776) | Data Validation and Query Processing Errors | Volume and File Upload/Access Errors              | DELETE request to a nonexistent file returns 404 instead of the S3-specified 204 causing file operation compatibility issues.                                                 | [Replication Steps](./seaweedfs%231776/README.md) |
| [4088](https://github.com/seaweedfs/seaweedfs/issues/4088) | Data Validation and Query Processing Errors       | Volume and File Upload/Access Errors              | The master server returns 404 Not Found when accessing files on a read-only volume indicating a failure in file access operations after the volume state changes.             | [Replication Steps](./seaweedfs%234088/README.md) |
| [4270](https://github.com/seaweedfs/seaweedfs/issues/4270) | Data Validation and Query Processing Errors        | Volume and File Upload/Access Errors              | API returns 500 Internal Server Error instead of 409 Conflict when attempting to create a directory that already exists.                                                      | [Replication Steps](./seaweedfs%234270/README.md) |
| [5155](https://github.com/seaweedfs/seaweedfs/issues/5155) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The API response is malformed and missing the required VersionConfiguration node causing clients to fail parsing the response.                                                | [Replication Steps](./seaweedfs%235155/README.md) |
| [5213](https://github.com/seaweedfs/seaweedfs/issues/5213) | Distributed Systems and Clustering Failures | Index and Cluster Coordination Failures           | Timeouts occur during /dir/assign requests specifically when the master initiates volume growth indicating issues with cluster coordination during dynamic volume assignment. | [Replication Steps](./seaweedfs%235213/README.md) |
| [5864](https://github.com/seaweedfs/seaweedfs/issues/5864) | Data Storage, Access, and Volume Errors | Volume and File Upload/Access Errors              | When the webdav service stops an existing file returns a 404 error indicating a file access issue rather than a true file absence.                                            | [Replication Steps](./seaweedfs%235864/README.md) |
| [6497](https://github.com/seaweedfs/seaweedfs/issues/6497) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The API allows creation of a bucket with an invalid name which leads to internal errors and an unremovable resource.                                                          | [Replication Steps](./seaweedfs%236497/README.md) |
| [6576](https://github.com/seaweedfs/seaweedfs/issues/6576) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | SeaweedFS does not support the x-id query parameter emitted by AWS SDKs causing issues with presigned requests.                                                               | [Replication Steps](./seaweedfs%236576/README.md) |




## Deploying, Managing, and Inspecting a Defect (SeaweedFS #913)

> **Note:** Replace **913** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p seaweedfs -i 913 --buggy --start

# 2. Deploy the patched version of the issue
defects4rest checkout -p seaweedfs -i 913 --patched --start

# 3. Stop running containers
defects4rest checkout -p seaweedfs -i 913 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p seaweedfs -i 913 --clean

# 5. Get bug information
defects4rest info -p seaweedfs -i 913

# 6. Check container logs if something goes wrong
docker logs seaweedfs
```



## Accessing SeaweedFS

Once deployed, the SeaweedFS service is accessible at:

* **Master URL:** `http://localhost:8333`
* **Volume Server URL:** `http://localhost:8080`
* **Authentication:** No authentication required for default local setup


## Troubleshooting

If the SeaweedFS service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs seaweedfs
```

Ensure that the required ports are free and no conflicting services are running.


## References

* [SeaweedFS GitHub Repository](https://github.com/seaweedfs/seaweedfs)
* [SeaweedFS Documentation](https://seaweedfs.com/)

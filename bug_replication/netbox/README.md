# NetBox Defects

This directory contains **6 replicable REST API bugs** documented from the [NetBox](https://github.com/netbox-community/netbox) project.

## Overview

NetBox is a leading open-source infrastructure resource modeling (IRM) application designed for network automation and infrastructure management. It provides a comprehensive REST API for managing IP addresses, racks, devices, circuits, and more.

## Available Defects

The table below shows the available defects including the defect type, sub defect type, description of each defect and a link to the steps for reproducing each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [18363](https://github.com/netbox-community/netbox/issues/18363) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API POST request to create a MAC address fails with a 400 error indicating a schema validation issue for the assigned_object_id field. | [Replication steps](./netbox%2318363/README.md) |
| [18368](https://github.com/netbox-community/netbox/issues/18368) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The API does not allow creation or retrieval of tags on MAC addresses while the web UI does indicating a mismatch in supported fields or schema between UI and API. | [Replication steps](./netbox%2318368/README.md) |
| [18585](https://github.com/netbox-community/netbox/issues/18585) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Filtering circuits by location_id parameter returns all circuits instead of only the attached ones. | [Replication steps](./netbox%2318585/README.md) |
| [18669](https://github.com/netbox-community/netbox/issues/18669) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | When the custom_fields section is present in a POST request body, default values for unspecified custom fields are ignored, leaving them as null. | [Replication steps](./netBox%2318669/README.md) |
| [18887](https://github.com/netbox-community/netbox/issues/18887) | Runtime and Exception Handling Errors | Runtime Errors and Exception Handling | The API fails with an AttributeError because it receives a VMInterface object instead of the expected data dictionary during validation when saving a custom field via the API. | [Replication steps](./netbox%2318887/README.md) |
| [18991](https://github.com/netbox-community/netbox/issues/18991) | Runtime and Exception Handling Errors | Runtime Errors and Exception Handling | An AttributeError is raised in the REST API when accessing the paths endpoint for ports indicating a runtime issue. | [Replication steps](./netbox%2318991/README.md) |

## Deploying, Managing, and Inspecting a Defect (NetBox #18363)

> **Note:** Replace **18363** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p netbox -i 18363 --buggy --start

# 2. Deploy the patched version of the issue
defects4rest checkout -p netbox -i 18363 --patched --start

# 3. Stop running containers
defects4rest checkout -p netbox -i 18363 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p netbox -i 18363 --clean

# 5. Get bug information
defects4rest info -p netbox -i 18363

# 6. Check container logs if something goes wrong
docker logs netbox
docker logs netbox-postgres
docker logs netbox-redis
```

## Accessing NetBox

Once deployed, the NetBox service is accessible at:

* **Base URL:** `http://localhost:8080`
* **Username:** `admin`
* **Password:** `admin`
* **API Token:** `0123456789abcdef0123456789abcdef01234567`

### API Authentication

Use the pre-configured API token in your requests:

```bash
curl -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
     -H "Content-Type: application/json" \
     http://localhost:8080/api/dcim/devices/
```

## Troubleshooting

If the NetBox service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs netbox
docker logs netbox-postgres
docker logs netbox-redis
```

Ensure that the required ports are free and no conflicting services are running.

## References

* [NetBox GitHub Repository](https://github.com/netbox-community/netbox)
* [NetBox API Documentation](https://demo.netbox.dev/api/docs/)

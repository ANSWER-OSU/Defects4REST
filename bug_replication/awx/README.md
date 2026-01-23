# AWX Defects

This directory contains **5 replicable REST API bugs** documented from the [AWX](https://github.com/ansible/awx) project.

## Overview

AWX is the open-source upstream project for Red Hat Ansible Automation Platform, providing a web-based UI, REST API, and task engine for Ansible automation.

## Available Defects

The table below shows the available defects including the defect type, sub defect type, description of each defect and a link to the steps for reproducing each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [7243](https://github.com/ansible/awx/issues/7243) | Authentication and Authorization Errors | Authentication and Token Management Errors | Unauthenticated GET request returns 500 instead of expected 401 indicating improper authentication error handling. | [Replication steps](./awx%237243/README.md) |
| [8305](https://github.com/ansible/awx/issues/8305) | Job and Workflow Errors | Job Execution and Workflow Configuration Defects | Deleting a workflow approval via the API results in a 500 error due to a backend workflow handling issue after the approval step is completed. | [Replication steps](./awx%238305/README.md) |
| [9222](https://github.com/ansible/awx/issues/9222) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | API returns a 500 error when an unsupported query parameter modifier is used instead of a proper 4xx error. | [Replication steps](./awx%239222/README.md) |
| [9472](https://github.com/ansible/awx/issues/9472) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API returns an incorrectly formatted ansible_version field when ansible-core is installed due to changes in the ansible --version output. | [Replication steps](./awx%239472/README.md) |
| [11130](https://github.com/ansible/awx/issues/11130) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API allows modification of restricted fields in the controlplane group without proper validation resulting in unintended changes. | [Replication steps](./awx%2311130/README.md) |

## Deploying, Managing, and Inspecting a Defect (AWX #7243)

> **Note:** Replace **7243** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p awx -i 7243 --buggy --start

# 2. Deploy the patched version of the issue
defects4rest checkout -p awx -i 7243 --patched --start

# 3. Stop running containers
defects4rest checkout -p awx -i 7243 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p awx -i 7243 --clean

# 5. Get bug information
defects4rest info -p awx -i 7243

# 6. Check container logs if something goes wrong
docker logs awx_web
docker logs awx_task
```

## Accessing AWX

Once deployed, the AWX service is accessible at:

* **Base URL:** `http://localhost:80`
* **Username:** `admin`
* **Password:** `password`

## Troubleshooting

If the AWX service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs awx_web
docker logs awx_task
docker logs awx_postgres
```

Ensure that the required ports are free and no conflicting services are running.

## References

* [AWX GitHub Repository](https://github.com/ansible/awx)
* [AWX Documentation](https://ansible.readthedocs.io/projects/awx/en/latest/)

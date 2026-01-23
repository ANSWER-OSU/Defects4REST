# Dolibarr Defects

This directory contains **24 replicable REST API bugs** documented from the [Dolibarr ERP/CRM](https://github.com/Dolibarr/dolibarr) project.

## Overview

Dolibarr is an open-source ERP and CRM software for small and medium businesses, freelancers, and foundations. It provides modules for sales, invoicing, inventory, accounting, and more, all accessible via a REST API.

## Available Defects

The table below shows the available defects including the defect type, sub defect type, description of each defect and a link to the steps for reproducing each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [23179](https://github.com/Dolibarr/dolibarr/issues/23179) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The /products/{id} REST API does not update the note_public and note_private fields indicating a failure to process or validate the payload for these properties. | [Replication steps](./dolibarr%2323179/README.md) |
| [23345](https://github.com/Dolibarr/dolibarr/issues/23345) | Authentication and Authorization Errors | Authorization and Permission Handling Errors | The API response for shipments contains database information that shouldn't be exposed indicating a security issue. | [Replication steps](./dolibarr%2323345/README.md) |
| [23415](https://github.com/Dolibarr/dolibarr/issues/23415) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | BOM API allows invalid/missing ref values when creating/updating BOMs. | [Replication steps](./dolibarr%2323415/README.md) |
| [24661](https://github.com/Dolibarr/dolibarr/issues/24661) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Contract line start/end dates are set as null in API responses despite having values. | [Replication steps](./dolibarr%2324661/README.md) |
| [26066](https://github.com/Dolibarr/dolibarr/issues/26066) | Authentication and Authorization Errors | Authorization and Permission Handling Errors | Missing permission checks on GET /multicurrencies endpoint allowing unauthorized access. | [Replication steps](./dolibarr%2326066/README.md) |
| [26881](https://github.com/Dolibarr/dolibarr/issues/26881) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | API endpoint setpricelevel returns 404 due to incorrect URL mapping. | [Replication steps](./dolibarr%2326881/README.md) |
| [29115](https://github.com/Dolibarr/dolibarr/issues/29115) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Extra fields behave inconsistently when updated via API - partial updates reset fields to null. | [Replication steps](./dolibarr%2329115/README.md) |
| [29292](https://github.com/Dolibarr/dolibarr/issues/29292) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Colon character in sqlfilters query parameter causes incorrect search results. | [Replication steps](./dolibarr%2329292/README.md) |
| [29372](https://github.com/Dolibarr/dolibarr/issues/29372) | Authentication and Authorization Errors | Authorization and Permission Handling Errors | User can access monthly statement page without proper "read all" permission by accessing URI directly. | [Replication steps](./dolibarr%2329372/README.md) |
| [29421](https://github.com/Dolibarr/dolibarr/issues/29421) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | GET /members/types/{id} endpoint incorrectly returns "Member type deleted" message. | [Replication steps](./dolibarr%2329421/README.md) |
| [29424](https://github.com/Dolibarr/dolibarr/issues/29424) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API doesn't return error for non-existing member ID when getting categories. | [Replication steps](./dolibarr%2329424/README.md) |
| [29439](https://github.com/Dolibarr/dolibarr/issues/29439) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Inconsistent API responses with missing ECM metadata fields in /documents endpoint. | [Replication steps](./dolibarr%2329439/README.md) |
| [30161](https://github.com/Dolibarr/dolibarr/issues/30161) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | Ticket API getByRef and getByTrackID endpoints always return specimen ticket instead of actual data. | [Replication steps](./dolibarr%2330161/README.md) |
| [30432](https://github.com/Dolibarr/dolibarr/issues/30432) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API doesn't update client_code and code_compta fields via thirdparties endpoint. | [Replication steps](./dolibarr%2330432/README.md) |
| [30950](https://github.com/Dolibarr/dolibarr/issues/30950) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Supplier invoice ref gets _1 suffix appended when created from template. | [Replication steps](./dolibarr%2330950/README.md) |
| [31015](https://github.com/Dolibarr/dolibarr/issues/31015) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API rejects payment request with datetime value error since upgrade to 20.0. | [Replication steps](./dolibarr%2331015/README.md) |
| [31369](https://github.com/Dolibarr/dolibarr/issues/31369) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API ignores provided date_solde field and sets current time instead when creating bank account. | [Replication steps](./dolibarr%2331369/README.md) |
| [31677](https://github.com/Dolibarr/dolibarr/issues/31677) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | DefaultWorkstationId field not handled in BOM line API. | [Replication steps](./dolibarr%2331677/README.md) |
| [32072](https://github.com/Dolibarr/dolibarr/issues/32072) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Extra fields in array_options don't update via PUT endpoint for shipments. | [Replication steps](./dolibarr%2332072/README.md) |
| [32096](https://github.com/Dolibarr/dolibarr/issues/32096) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | linkedObjectsIds field is null in search results but populated when fetching by ID. | [Replication steps](./dolibarr%2332096/README.md) |
| [32111](https://github.com/Dolibarr/dolibarr/issues/32111) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API expects timestamp but rejects valid date string format for payment date. | [Replication steps](./dolibarr%2332111/README.md) |
| [32145](https://github.com/Dolibarr/dolibarr/issues/32145) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Incorrect evaluation of private_message parameter causes unintended status changes in tickets. | [Replication steps](./dolibarr%2332145/README.md) |
| [33689](https://github.com/Dolibarr/dolibarr/issues/33689) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Validation logic for POST requests breaks ability to import order lines in supplier orders. | [Replication steps](./dolibarr%2333689/README.md) |
| [33949](https://github.com/Dolibarr/dolibarr/issues/33949) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | API accepts PUT request but fails to persist updated extrafield default value. | [Replication steps](./dolibarr%2333949/README.md) |

## Deploying, Managing, and Inspecting a Defect (Dolibarr #23179)

> **Note:** Replace **23179** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p dolibarr -i 23179 --buggy --start

# 2. Deploy the patched version of the issue
defects4rest checkout -p dolibarr -i 23179 --patched --start

# 3. Stop running containers
defects4rest checkout -p dolibarr -i 23179 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p dolibarr -i 23179 --clean

# 5. Get bug information
defects4rest info -p dolibarr -i 23179

# 6. Check container logs if something goes wrong
docker logs dolibarr-dolibarr-1
docker logs dolibarr-db-1
```

## Accessing Dolibarr

Once deployed, the Dolibarr service is accessible at:

* **Base URL:** `http://localhost:8080`
* **Initial Setup:** Complete the installation wizard on first access

### Database Credentials (for setup wizard)

* **Database Server:** `db`
* **Database Name:** `dolibarr`
* **Database User:** `dolibarr`
* **Database Password:** `dolibarr`

### API Authentication

Dolibarr uses API keys for authentication. Include the key in your requests:

```bash
curl -H "DOLAPIKEY: <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     http://localhost:8080/api/index.php/products
```

## Troubleshooting

If the Dolibarr service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs dolibarr-dolibarr-1
docker logs dolibarr-db-1
```

To access the database directly:
```bash
docker exec -it dolibarr-db-1 mysql -u dolibarr -pdolibarr dolibarr
```

Ensure that the required ports are free and no conflicting services are running.

## References

* [Dolibarr GitHub Repository](https://github.com/Dolibarr/dolibarr)
* [Dolibarr Documentation](https://wiki.dolibarr.org/)
* [Dolibarr REST API Documentation](https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST_(developer))

# Mastodon Defects

This directory contains **5 replicable REST API bugs** documented from the [Mastodon](https://github.com/mastodon/mastodon) project.

## Overview

Mastodon is a free, open-source decentralized social networking platform. It provides ActivityPub-compatible APIs for federation and a comprehensive REST API for client applications.

## Available Defects

The table below shows the available defects including the defect type, sub defect type, description of each defect and a link to the steps for reproducing each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [28381](https://github.com/mastodon/mastodon/issues/28381) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns a 500 error due to an ambiguous column in the SQL ORDER BY clause triggered by specific query parameters. | [Replication steps](./mastodon%2328381/README.md) |
| [29071](https://github.com/mastodon/mastodon/issues/29071) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | The API returns Suggestion.source as an array of strings instead of the documented string type causing schema decoding failures for clients. | [Replication steps](./mastodom%2329071/README.md) |
| [30039](https://github.com/mastodon/mastodon/issues/30039) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The Idempotency-Key header is ignored when scheduling posts, allowing duplicate scheduled posts to be created. | [Replication steps](./mastodon%2330039/README.md) |
| [30103](https://github.com/mastodon/mastodon/issues/30103) | Data Validation and Query Processing Errors | Schema and Payload Validation Errors in POST APIs | Creating a new push subscription doesn't properly delete the previous subscription, leading to multiple active subscriptions. | [Replication steps](./mastodon%2330103/README.md) |
| [33357](https://github.com/mastodon/mastodon/issues/33357) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API returns incorrect last usage dates for featured hashtags only when querying remote users, indicating the defect is specific to federated environment behavior. | [Replication steps](./mastodom%2333357/README.md) |

## Deploying, Managing, and Inspecting a Defect (Mastodon #28381)

> **Note:** Replace **28381** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p mastodon -i 28381 --buggy --start

# 2. Deploy the patched version of the issue 
defects4rest checkout -p mastodon -i 28381 --patched --start

# 3. Stop running containers
defects4rest checkout -p mastodon -i 28381 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p mastodon -i 28381 --clean

# 5. Get bug information
defects4rest info -p mastodon -i 28381

# 6. Check container logs if something goes wrong
docker-compose logs web
docker-compose logs sidekiq
```

## Accessing Mastodon

Once deployed, the Mastodon service is accessible at:

* **Base URL:** `http://localhost:3000`
* **Admin Email:** `admin@localhost`
* **Username:** `testadmin`
* **Password:** *(generated during deployment - check console output)*

### API Authentication

Mastodon uses OAuth Bearer tokens. Include the token in your requests:

```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://localhost:3000/api/v1/accounts/verify_credentials
```

## Troubleshooting

If the Mastodon service fails to start or behaves unexpectedly, check the container logs:

```bash
docker-compose logs web
docker-compose logs sidekiq
docker-compose logs db
```

To reset the admin password:
```bash
docker-compose run --rm web bin/tootctl accounts modify testadmin --reset-password
```

Ensure that the required ports are free and no conflicting services are running.

## References

* [Mastodon GitHub Repository](https://github.com/mastodon/mastodon)
* [Mastodon API Documentation](https://docs.joinmastodon.org/api/)

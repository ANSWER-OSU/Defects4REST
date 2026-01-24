# Checkout Command

Deploy, manage, and clean up bug environments.

## Usage

```bash
defects4rest checkout -p <project> -i <issue_id> [OPTIONS]
```

## Arguments

| Argument | Required | Description |
|----------|:--------:|-------------|
| `-p`| Yes | Project name (one of `awx`, `dolibarr` , `enviroCar-server` , `flowable-engine` , `kafka-rest`, `mastodon` , `netbox` , `nocodb` , `podman` , `restcountries`, `seaweedfs`, `signal-cli-rest-api`) |
| `-i` | Yes | GitHub issue number (Issue ID listed [here](../../bug_replication/README.md)) |

## Options

| Option | Description |
|--------|-------------|
| `--buggy` | Deploy the buggy version |
| `--patched` | Deploy the patched version |
| `--start` | Start deployment (implied with `--buggy` or `--patched`) |
| `--stop` | Stop running containers |
| `--clean` | Stop and remove all containers, volumes, networks |

## Actions

### Deploy Buggy version and start the service from the URL displayed on the terminal. NOTE: this will stop already running services. 

```bash
defects4rest checkout -p netbox -i 18363 --buggy
```

### Deploy Patched version and start the service from the URL displayed on the terminal. NOTE: this will stop already running services. 

```bash
# First patch (default)
defects4rest checkout -p netbox -i 18363 --patched
```

### Stop Docker container of a buggy or patched version of a service 

```bash
defects4rest checkout -p netbox -i 18363 --stop
```

### Delete all Docker Containers of a service 

```bash
defects4rest checkout -p netbox -i 18363 --clean
```

## Example Usage

```bash
# 1. Deploy buggy version of netbox project corresponding to issue# 18363 using the following command. The service will be accessible at http://
defects4rest checkout -p netbox -i 18363 --buggy --start

# 2. Execute the bug replication steps (see  )
curl -X POST "http://localhost:8080/api/dcim/mac-addresses/" ...

# 3. Stop the buggy version
defects4rest checkout -p netbox -i 18363 --stop

# 4. Deploy patched version of netbox project corresponding to issue# 18363 using the following command. The service will be accessible at http://
defects4rest checkout -p netbox -i 18363 --patched --start

# 5. Verify fix by re-executing the bug replication steps. 
curl -X POST "http://localhost:8080/api/dcim/mac-addresses/" ...

# 6. Stop the service if you want to rerun it using the following command. To restart the buggy or patched version of the service, rerun step 1 or step 4, respectively. 
defects4rest checkout -p netbox -i 18363 --stop

# 7. Delete the Docker container created for a API using the command:
defects4rest checkout -p netbox -i 18363 --stop
```

## Troubleshooting

### Check Container Logs

```bash
docker logs <container_name>
```

### Port Conflict

```bash
# Find conflicting container
docker ps

# Stop it
docker stop <container_name>
```

### Fresh Start

```bash
defects4rest checkout -p <project> -i <issue> --clean
```

## See Also

- [Info Command](./info.md)
- [Main README](../../README.md)

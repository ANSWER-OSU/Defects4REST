# Checkout Command

Deploy, manage, and clean up bug environments.

## Usage

```bash
defects4rest checkout -p <project> -i <issue_id> [OPTIONS]
```

## Arguments

| Argument | Required | Description |
|----------|:--------:|-------------|
| `-p, --project` | Yes | Project name |
| `-i, --issue_id` | Yes | GitHub issue number |

## Options

| Option | Description |
|--------|-------------|
| `--buggy` | Deploy the buggy version |
| `--patched [N]` | Deploy the Nth patched version (default: 1) |
| `--start` | Start deployment (implied with `--buggy` or `--patched`) |
| `--stop` | Stop running containers |
| `--clean` | Stop and remove all containers, volumes, networks |

## Actions

### Deploy Buggy Version

```bash
defects4rest checkout -p netbox -i 18363 --buggy --start
```

### Deploy Patched Version

```bash
# First patch (default)
defects4rest checkout -p netbox -i 18363 --patched --start

# Specific patch number
defects4rest checkout -p netbox -i 18363 --patched 2 --start
```

### Stop Containers

```bash
defects4rest checkout -p netbox -i 18363 --stop
```

### Full Cleanup

```bash
defects4rest checkout -p netbox -i 18363 --clean
```

## Workflow Example

```bash
# 1. Deploy buggy version
defects4rest checkout -p netbox -i 18363 --buggy --start

# 2. Reproduce bug (see project README for curl commands)
curl -X POST "http://localhost:8080/api/dcim/mac-addresses/" ...

# 3. Stop buggy version
defects4rest checkout -p netbox -i 18363 --stop

# 4. Deploy patched version
defects4rest checkout -p netbox -i 18363 --patched --start

# 5. Verify fix
curl -X POST "http://localhost:8080/api/dcim/mac-addresses/" ...

# 6. Cleanup
defects4rest checkout -p netbox -i 18363 --clean
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

# Info Command

Display detailed information about a specific bug.

## Usage

```bash
defects4rest info -p <project> -i <issue_id>
```

## Arguments

| Argument | Required | Description |
|----------|:--------:|-------------|
| `-p, --project` | Yes | Project name (See below for list of available projects) |
| `-i, --issue_id` | Yes | GitHub issue number (Issue ID listed [here](../../bug_replication/README.md)) |

### Available projects
| Project name | Bugs |
|---------|:----:|
| [awx](../../bug_replication/awx/) | 5 |
| [dolibarr](../../bug_replication/dolibarr/) | 25 |
| [enviroCar-server](../../bug_replication/envirocar-server/) | 4 |
| [flowable-engine](../../bug_replication/flowable-engine/) | 5 |
| [kafka-rest](../../bug_replication/kafka-rest/) | 3 |
| [mastodon](../../bug_replication/mastodon/) | 5 |
| [netbox](../../bug_replication/netbox/) | 6 |
| [nocodb](../../bug_replication/nocodb/) | 6 |
| [podman](../../bug_replication/podman/) | 23 |
| [restcountries](../../bug_replication/restcountries/) | 16 |
| [seaweedfs](../../bug_replication/seaweedfs/) | 9 |
| [signal-cli-rest-api](../../bug_replication/signal-cli-rest-api/) | 3 |

## Example Usage

```bash
defects4rest info -p netbox -i 18363
```

## Output

```
════════════════════════════════════════════════════════════════════════════════
                              Netbox (Issue #18363)
════════════════════════════════════════════════════════════════════════════════

Project Metadata
Project       : netbox
Bug ID        : 18363
Issue Number  : 18363
Issue URL     : https://github.com/netbox-community/netbox/issues/18363
Title         : cant create vm mac-address via api
Days to Fix   : 3

Patched Files
- netbox/dcim/api/serializers.py
- netbox/dcim/tests/test_api.py

Patched File Types
- source-file
- test-file

SHAs
Buggy SHA     : 9a1d9365cd7c703413ca8d15c0b8b737067c275e
Patch SHA(s)  : 636148f9654b82f7e664645f3e781a4591a22132
```

## Output Fields

| Field | Description |
|-------|-------------|
| **Project** | Project name |
| **Bug ID** | Issue identifier |
| **Issue URL** | Link to GitHub issue |
| **Title** | Issue title |
| **Days to Fix** | Time between issue report and fix |
| **Patched Files** | Files modified to fix the bug |
| **Patched File Types** | Categories: `source-file`, `test-file`, `config-file`, `doc-file` |
| **Buggy SHA** | Git commit hash before the fix |
| **Patch SHA(s)** | Git commit hash(es) of the fix |

## See Also

- [Checkout Command](./checkout.md)
- [Main README](../../README.md)

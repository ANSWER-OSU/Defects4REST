# Defects4REST Version 1.0

A comprehensive benchmark framework for systematically deploying, testing, and analyzing reproducible real-world bugs in REST API applications.The framework includes 110 defects across 12 real-world open-source projects, complete with deployment scripts, replication steps, and detailed metadata.

## Features

- **Single Command Deployment** — Deploy buggy or patched versions instantly
- **Pre-configured Environments** — Admin accounts, API tokens, and test data included where applicable
- **Step-by-Step Guides** — Detailed replication steps provided for all 110 bugs

## Supported Projects

| Project | Bugs |
|---------|:----:|
| [awx](./bug_replication/awx/) | 5 |
| [dolibarr](./bug_replication/dolibarr/) | 25 |
| [enviroCar-server](./bug_replication/envirocar-server/) | 4 |
| [flowable-engine](./bug_replication/flowable-engine/) | 5 |
| [kafka-rest](./bug_replication/kafka-rest/) | 3 |
| [mastodon](./bug_replication/mastodon/) | 5 |
| [netbox](./bug_replication/netbox/) | 6 |
| [nocodb](./bug_replication/nocodb/) | 6 |
| [podman](./bug_replication/podman/) | 23 |
| [restcountries](./bug_replication/restcountries/) | 16 |
| [seaweedfs](./bug_replication/seaweedfs/) | 9 |
| [signal-cli-rest-api](./bug_replication/signal-cli-rest-api/) | 3 |

See the complete list of all bugs [here](./bug_replication/README.md) 

## Installation

### Prerequisites

#### Linux / macOS:
- Python 3.9+
- Docker and Docker Compose
- Git
- Go 1.16+

#### Windows
- Python 3.9+
- Docker and Docker Compose
- Git
- Go 1.16+
- WSL2 installed with Ubuntu
- Docker Desktop with WSL integration enabled

#### Project-Specific System Requirements (Podman)
> **Note:** The following requirements apply only when replicating defects from
> the **Podman** subject.
- Linux environment:
  - Native Linux
  - Windows Subsystem for Linux (WSL)
  - Linux virtual machine on macOS (e.g., Podman machine)
- `sudo` privileges
- System packages:
```bash
sudo apt-get update

sudo apt-get install -y conmon btrfs-progs gcc git golang-go go-md2man iptables libassuan-dev libbtrfs-dev libc6-dev libdevmapper-dev libglib2.0-dev libgpgme-dev libgpg-error-dev libprotobuf-dev libprotobuf-c-dev libseccomp-dev libselinux1-dev libsystemd-dev make netavark passt pkg-config runc uidmap
````

### Install from Source

```bash
# Clone the repository
git clone https://github.com/ANSWER-OSU/Defects4REST.git
cd Defects4REST

# Install in development mode
pip install -e .

# Verify installation
defects4rest --help
```

## Usage

The CLI provides two commands: `info` to view bug details and `checkout` to deploy environments.

```bash
# View bug details
defects4rest info -p <project> -i <issue>

# Deploy buggy version
defects4rest checkout -p <project> -i <issue> --buggy --start

# Deploy patched version
defects4rest checkout -p <project> -i <issue> --patched --start

# Cleanup
defects4rest checkout -p <project> -i <issue> --clean
```

See detailed documentation: [info](./docs/commands/info.md) | [checkout](./docs/commands/checkout.md)

## OpenAPI Specifications

For REST API testing tools, OpenAPI specifications are available for each bug at:

```
bug_replication/<project>/<project>#<issue>/<project>#<issue>_spec.json/yaml
```

## Defect Categories

| Defect Type | Sub Defect Type |
|-------------|-----------------|
| **Configuration and Environment Issues (T1)** | Container and Resource Quota Handling Errors (ST1) |
| | Job Execution and Workflow Configuration Defects (ST2) |
| | Environment-Specific Behavior and Configuration Bugs (ST3) |
| **Data Validation and Query Processing Errors (T2)** | Schema and Payload Validation Errors in POST APIs (ST4) |
| | Query Filter and Search Parameter Handling Errors (ST5) |
| **Authentication, Authorization, and Session Management Issues (T3)** | Authentication and Token Management Errors (ST6) |
| | Session, Token, and Account Lifecycle Management Errors (ST7) |
| **Integration, Middleware, and Runtime Environment Failures (T4)** | Middleware Integration Failures in REST APIs (ST8) |
| | Process Signal and Grouping Issues in Containerized APIs (ST9) |
| | Runtime and Dependency Errors (ST10) |
| **Data Storage, Access, and Volume Errors (T5)** | Volume and File Upload/Access Errors (ST11) |
| | Database/Table User Access Handling Errors (ST12) |
| **Distributed Systems and Cluster Failures (T6)** | Index and Cluster Coordination Failures (ST13) |

## Contributing

We welcome contributions! See our guides:

- [Adding New Bugs](./docs/ADDING_BUGS.md) — Step-by-step guide to add new defects


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

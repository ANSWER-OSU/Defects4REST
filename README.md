# Defects4REST version 1.0

A comprehensive defect benchmark and framework for systematically deploying, testing, and analyzing reproducible real-world bugs in REST API applications.

## Features

**Reproducible Bug Deployment for Real-World APIs** — Deploy buggy or patched versions of 12 real-world, open-source REST APIs to replicate 110 defects across these APIs.

**Detailed Fault Information** — Easily access bug report information, developer-modified files used to repair the bug, types of modified files categorized into eight categories, the time developers took to fix the bug, and commit messages.

**Bug Mining Framework** — Reuse the bug mining framework to automatically add more defects from existing or new REST API projects.

## Supported Projects and Defects

| Project        | Number of defects | 
|-------------------------------------------------------------------------|------------|
| [AWX](https://github.com/ansible/awx)                                   |          5 |
| [Dolibarr](https://github.com/Dolibarr/dolibarr)                        |         25 |
| [EnviroCar Server](https://github.com/enviroCar/enviroCar-server)       |          4 |
| [Flowable Engine](https://github.com/flowable/flowable-engine)          |          5 |
| [Kafka REST](https://github.com/confluentinc/kafka-rest)                |          3 |
| [Mastodon](https://github.com/mastodon/mastodon)                        |          5 |
| [NetBox](https://github.com/netbox-community/netbox)                    |          6 |
| [NocoDB](https://github.com/nocodb/nocodb)                              |          6 |
| [Podman](https://github.com/containers/podman)                          |         23 |
| [REST Countries](https://github.com/apilayer/restcountries)             |         16 |
| [SeaweedFS](https://github.com/seaweedfs/seaweedfs)                     |          9 |
| [Signal CLI REST API](https://github.com/bbernhard/signal-cli-rest-api) |          3 |

---

## Installation

### Prerequisites

- **Python 3.9+**
- **Docker** and **Docker Compose**
- **Git**
- **Make** (for AWX)
- **Maven** (for REST Countries)

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


---

## Quick Start

```bash
# View information about a specific bug
defects4rest info -p netbox -i 18991

# Deploy the buggy version of issue #18991 for NetBox
defects4rest checkout -p netbox -i 18991 --buggy --start

# Deploy the patched version
defects4rest checkout -p netbox -i 18991 --patched --start

# Stop the running containers
defects4rest checkout -p netbox -i 18991 --stop

# Clean up all resources
defects4rest checkout -p netbox -i 18991 --clean
```

---

## Usage

### Info Command

Display detailed information about a specific bug in a project.

```bash
defects4rest info -p <project_name> -i <issue_id>
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `-p, --project` | Project name (e.g., `awx`, `netbox`, `mastodon`) |
| `-i, --issue` | Issue/bug identifier number |

**Example:**

```bash
defects4rest info -p netbox -i 18991
```

**Example Output:**


    ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                     Netbox (Issue #18991)                                                  
    ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
   
    
    Project Metadata
    Project       : netbox
    Bug ID        : 18991
    Issue Number  : 18991
    Issue URL     : https://github.com/netbox-community/netbox/issues/18991
    Title         : Path tracing broken for front/rear ports in REST API
    Days to Fix   : 2
    
    Patched Files
    - netbox/dcim/tests/test_api.py
    - netbox/utilities/fields.py
    
    Patched File Types
    - source-file
    - test-file
    
    SHAs
    Buggy SHA     : 9a1d9365cd7c703413ca8d15c0b8b737067c275e
    Patch SHA(s)  : 636148f9654b82f7e664645f3e781a4591a22132
                    fd2bcda8b8777b955222644a5ff94417ba510cb2
   


### Checkout Command

Deploy, manage, and clean up project instances at specific versions.

```bash
defects4rest checkout -p <project> -i <issue> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `-p` | Project name |
| `-i` | Issue/bug identifier |
| `--buggy` | Deploy the buggy version |
| `--patched N` | Deploy the Nth patched version (1-indexed) |
| `--start` | Start the deployment |
| `--stop` | Stop running containers (preserves data) |
| `--clean` | Remove all containers, volumes, and networks |

**Examples:**

```bash

# Deploy buggy version
defects4rest checkout -p kafka-rest -i 475 --buggy --start

# Deploy first patch
defects4rest checkout -p kafka-rest -i 475 --patched 1 --start

# Deploy second patch (if multiple patches exist)
defects4rest checkout -p kafka-rest -i 475 --patched 2 --start

# Stop containers
defects4rest checkout -p kafka-rest -i 475 --stop

# Full cleanup
defects4rest checkout -p kafka-rest -i 475 --clean
```

---
## Adding new projects
Instructions for adding new projects can be found in our [CONTRIBUTING.md](CONTRIBUTING.md)

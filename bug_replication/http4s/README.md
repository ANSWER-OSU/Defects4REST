## Triggering Behavior

### Reproducibility Approach

Bug #5069 was fixed in PR #5070 and released in http4s **0.22.3** and **0.23.x**. The exact historical git SHAs in the CSV (`buggy_sha = 82f8c4b9…`, `patch_sha = 3a617522…`) are checked out into the project directory for **code inspection**. The running reproduction server, however, is compiled against **published Maven Central artifacts** rather than from the historical source tree, because building old http4s commits requires a matching historical JDK and sbt toolchain that is impractical to require from every reviewer.

This approach is consistent with how Defects4REST handles projects that publish Docker images to Docker Hub (`buggy_docker_version` / `patched_docker_version` columns in the CSV schema): the historical commit provides metadata and source provenance, while a published artifact provides the running binary.

The two artifact versions used here are:

| Variant | http4s artifact | Maven Central coordinates | Contains fix? |
|---------|-----------------|--------------------------|---------------|
| `buggy`   | `0.22.2`  | `org.http4s::http4s-ember-server::0.22.2`  | No — last release containing the bug |
| `patched` | `0.23.38` | `org.http4s::http4s-ember-server::0.23.38` | Yes — includes PR #5070 |

To switch between buggy and patched behavior, change the `//> using lib` directives at the top of `ReproServer.scala` (or pass `--buggy` / `--patched` to the deploy script).

### Prerequisites
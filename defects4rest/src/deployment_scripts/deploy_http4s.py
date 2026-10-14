#-------------------------------------------------------------------------------
# Copyright (c) 2026 NancyD2017
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""
http4s Deployment Script

This script deploys a minimal Ember-based http4s server for the purpose of
reproducing REST API bugs from the http4s project (https://github.com/http4s/http4s).

Because http4s is a Scala library (not a deployable application), the script
builds and runs a single-file Ember server that depends on the locally checked-out
http4s sources. The server is launched via `scala-cli`, which is the simplest way
to compile and run a single Scala file against a local sbt project.

Prerequisites:
    - git
    - java (JDK 11+)
    - scala-cli (https://scala-cli.virtuslab.org/)
    - curl (for readiness check)

The reproduction server exposes a single `GET /` route that explicitly parses
the `Accept-Language` request header. This is the entry point used by bug #5069.
"""
import subprocess
import shutil
import os
import sys
import time
import socket
import argparse

# Make the project root importable so the script can be run directly via
#   python defects4rest/src/deployment_scripts/deploy_http4s.py
# without first installing the package with `pip install -e .`.
# When executed as `python <script>`, Python only adds the script's own
# directory to sys.path — we walk up three levels to reach the project root.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from defects4rest.src.utils.shell import run, pretty_step, pretty_section, pretty_subsection
from defects4rest.src.utils.resources import ensure_temp_project_dir, check_prereq, data_csv

REPO_URL = "https://github.com/http4s/http4s.git"

PROJECT_NAME = 'http4s'
PROJECT_DIR = str(ensure_temp_project_dir(PROJECT_NAME))

DEFAULT_PORT = 8080
REPRO_FILE = "ReproServer.scala"

# The reproduction server is a single Scala file that depends on a
# published http4s artifact. Because the bug being reproduced (#5069) was
# fixed in PR #5070 and released in http4s 0.22.3, we use TWO different
# published versions from the SAME 0.22.x line to demonstrate buggy vs
# patched behavior:
#
#   buggy   → http4s 0.22.2  (last release containing the bug)
#   patched → http4s 0.22.3 (first release containing the fix, PR #5070)
#
# Using two versions from the same 0.22.x line (instead of jumping to
# 0.23.x for the patched build) keeps the EmberServerBuilder API
# identical between the two variants. The only difference between 0.22.2
# and 0.22.3 is the parser grammar fix in `Accept-Language.scala` /
# `Content-Language.scala`, which is exactly the bug being reproduced.
# This means the ReproServer.scala source compiles unchanged against
# both artifact versions.
#
# The exact historical git SHAs (buggy_sha / patch_sha from the CSV) are
# still checked out into the project directory for code inspection, but
# the running reproduction server uses the published artifacts above so
# that no historical JDK/sbt toolchain is required.

# API in 0.22.x is simpler than in 0.23.x:
#   - 0.22.x: withHost(String), withPort(Int)
#   - 0.23.x: withHost(Host),     withPort(Port)
# Using 0.22.x for both buggy and patched keeps the source simple — just
# plain String/Int, no ip4s imports needed.

# Template for the reproduction Scala source. {HTTP4S_VERSION} is filled in
# at deploy time based on the --buggy / --patched flag.
REPRO_SOURCE_TEMPLATE = '''//> using scala 2.13.12
//> using lib org.http4s::http4s-ember-server::{HTTP4S_VERSION}
//> using lib org.http4s::http4s-dsl::{HTTP4S_VERSION}

import cats.effect._
import org.http4s._
import org.http4s.dsl.io._
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.headers.`Accept-Language`
import org.http4s.implicits._

object ReproServer extends IOApp.Simple {
  // The Accept-Language header name as registered in http4s.
  private val acceptLanguageName = Header[`Accept-Language`].name

  val routes = HttpRoutes.of[IO] {
    case req @ GET -> Root =>
      // Look up the raw Accept-Language header value(s) sent by the client.
      val rawValues =
        req.headers.headers
          .filter(_.name == acceptLanguageName)
          .map(_.value)

      rawValues match {
        case Nil =>
          Ok("No Accept-Language header sent.")
        case value :: _ =>
          // Explicitly invoke the parser.
          //   buggy build   (0.22.2)  → Left(ParseFailure(...)) on wildcard `*`
          //   patched build (0.22.3)  → Right(Accept-Language(...))
          `Accept-Language`.parse(value) match {
            case Right(acceptLang) =>
              Ok(s"Parsed Accept-Language successfully: ${acceptLang.value}")
            case Left(err) =>
              InternalServerError(s"Accept-Language parse failure: ${err.message}")
          }
      }
  }.orNotFound

  def run: IO[Unit] =
    EmberServerBuilder
      .default[IO]
      .withHost("0.0.0.0")
      .withPort(8080)
      .withHttpApp(routes)
      .build
      .use(_ => IO.never)
}
'''

# The same source works in both 0.22.2 (buggy) and 0.22.3 (patched) because
# the EmberServerBuilder API is identical between these two patch releases —
# the only difference is the parser grammar fix in `Accept-Language.scala`.

# Historical SHAs from the CSV (kept for code inspection; not used to build).
BUGGY_SHA   = "82f8c4b90b08bd6e037b400db52f20b86d666c23"   # buggy commit
PATCHED_SHA = "3a6175224bf96a9e2848cae706295485226590f7"   # fix commit

# Published artifact versions used to actually run the reproduction server.
BUGGY_ARTIFACT   = "0.22.2"   # last release containing the bug
PATCHED_ARTIFACT = "0.22.3"   # first release containing the fix (PR #5070)

def _build_repro_source(http4s_version: str) -> str:
    """Render the ReproServer.scala source for a given http4s version."""
    return REPRO_SOURCE_TEMPLATE.replace("{HTTP4S_VERSION}", http4s_version)

# Container name used when --use-docker is passed. The default code path
# runs scala-cli directly on the host; the Docker path is provided for
# sandboxed reproductions and CI.
CONTAINER_NAME = "http4s-repro-server"

CSV_PATH = data_csv(PROJECT_NAME)


def _wait_for_port(host: str, port: int, timeout: int = 120) -> bool:
    """Poll a TCP port until it accepts a connection or timeout elapses."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except OSError:
            time.sleep(2)
    return False


def write_repro_source(http4s_version: str):
    """Write the reproduction Scala source file into the project directory,
    rendered against the given http4s published artifact version.
    """
    source = _build_repro_source(http4s_version)
    repro_path = os.path.join(PROJECT_DIR, REPRO_FILE)
    with open(repro_path, "w", encoding="utf-8") as f:
        f.write(source)
    print(f"Wrote reproduction source for http4s {http4s_version}: {repro_path}")
    return repro_path


def launch_on_host(repro_path: str, port: int):
    """Launch the reproduction server on the host via scala-cli in the background."""
    pretty_step(f"Launching reproduction server via scala-cli (port {port}) …")
    log_path = os.path.join(PROJECT_DIR, "server.log")
    log = open(log_path, "w", encoding="utf-8")
    # On Windows, scala-cli is installed as `scala-cli.bat`. On Unix, it's
    # `scala-cli`. We resolve the full path via shutil.which so that
    # subprocess.Popen finds it without requiring shell=True.
    scala_cli_cmd = shutil.which("scala-cli")
    if scala_cli_cmd is None and os.name == "nt":
        # Try the .bat variant explicitly on Windows (shutil.which sometimes
        # doesn't pick it up if PATHEXT is misconfigured).
        scala_cli_cmd = shutil.which("scala-cli.bat")
    if scala_cli_cmd is None:
        raise FileNotFoundError(
            "scala-cli was not found on PATH. Install it from "
            "https://scala-cli.virtuslab.org/ and re-run this script."
        )
    print(f"Using scala-cli at: {scala_cli_cmd}")
    proc = subprocess.Popen(
        [scala_cli_cmd, "run", repro_path, "--server=false"],
        cwd=PROJECT_DIR,
        stdout=log,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
    )
    # Persist the PID so stop()/clean() can find and kill it later.
    pid_path = os.path.join(PROJECT_DIR, "server.pid")
    with open(pid_path, "w") as f:
        f.write(str(proc.pid))
    print(f"Server PID {proc.pid} (logs: {log_path})")


def launch_in_docker(repro_path: str, port: int):
    """Launch the reproduction server inside a Docker container.

    Uses the official scala-cli image so that no host-level Scala toolchain is
    required. The project directory is bind-mounted read-only into the container
    so the same checked-out sources are visible inside.
    """
    pretty_step(f"Launching reproduction server in Docker (port {port}) …")

    # Remove any stale container
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True, text=True,
    )
    if CONTAINER_NAME in result.stdout.splitlines():
        print(f"Removing existing container '{CONTAINER_NAME}' …")
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], check=False)

    run([
        "docker", "run", "-d",
        "--name", CONTAINER_NAME,
        "-p", f"{port}:8080",
        "-v", f"{PROJECT_DIR}:/workspace:ro",
        "-w", "/workspace",
        "virtuslab/scala-cli:0.3.x",
        "scala-cli", "run", REPRO_FILE, "--server=false",
    ])


def main(sha=None, issue_id=None, action: str = "deploy", port=DEFAULT_PORT, use_docker: bool = False, variant: str = None):
    """Main deployment function for http4s.

    Conforms to the Defects4REST deploy-script interface:
    `main(sha, issue_id)` — used by `defects4rest checkout -p http4s -i <issue> --buggy|--patched --start`.

    The `sha` parameter (passed by the Defects4REST CLI from the CSV's
    `buggy_sha` / `patch_sha` column) is used to determine which published
    http4s artifact to compile and run the reproduction server against:
        - sha == BUGGY_SHA   → http4s 0.22.2  (last release containing the bug)
        - sha == PATCHED_SHA → http4s 0.22.3 (first release containing the fix)

    The corresponding historical git SHA is also checked out into the project
    directory so that the user can inspect the exact buggy / patched source code.

    Args:
        sha: Git commit SHA to check out (buggy or patched). When passed by
            the Defects4REST CLI, this comes from the CSV's `buggy_sha` or
            `patch_sha` column. If None, `variant` must be set.
        issue_id: GitHub issue number (used for logging and hooks).
        action: One of {"deploy", "clone_only"}. "clone_only" checks out the
            sources without launching the server — useful for offline inspection.
        port: Host port to expose the reproduction server on.
        use_docker: If True, run scala-cli inside a Docker container; otherwise
            run on the host. Docker is recommended for CI; the host path is
            recommended for interactive reproductions.
        variant: Convenience override for CLI use. One of {"buggy", "patched"}.
            If both `sha` and `variant` are set, `sha` takes precedence.
            If only `variant` is set, the corresponding SHA is looked up.
    """
    if sha is not None:
        sha_lower = sha.lower()
        if sha_lower == BUGGY_SHA.lower() or sha_lower == BUGGY_SHA[:8].lower():
            variant = "buggy"
        elif sha_lower == PATCHED_SHA.lower() or sha_lower == PATCHED_SHA[:8].lower():
            variant = "patched"
        else:
            raise ValueError(
                f"Unknown SHA: {sha!r}. Expected one of:\n"
                f"  buggy   (82f8c4b90b08bd6e037b400db52f20b86d666c23)\n"
                f"  patched (3a6175224bf96a9e2848cae706295485226590f7)"
            )
    elif variant is None:
        # Default to buggy when neither sha nor variant is given.
        variant = "buggy"

    if variant not in ("buggy", "patched"):
        raise ValueError(f"variant must be 'buggy' or 'patched', got: {variant!r}")

    sha = BUGGY_SHA if variant == "buggy" else PATCHED_SHA
    artifact_version = BUGGY_ARTIFACT if variant == "buggy" else PATCHED_ARTIFACT

    if action == "deploy":
        pretty_section(
            f"Deploying http4s (issue #{issue_id}) — variant={variant}, "
            f"SHA={sha[:8]}…, artifact=0.{artifact_version}"
        )
    else:
        pretty_section(
            f"Cloning http4s (issue #{issue_id}) — variant={variant}, SHA={sha[:8]}…"
        )

    # Stop any running server from a prior deployment BEFORE removing the
    # project directory. On Windows, files held open by a running scala-cli
    # process cannot be deleted, which would cause `git clone` below to fail
    # with "destination path already exists and is not an empty directory".
    stop(heading=False)

    # Remove existing repo for a clean checkout.
    if os.path.isdir(PROJECT_DIR):
        pretty_step(f"Removing existing repo at {PROJECT_DIR} …")
        # Retry on Windows because file locks may take a moment to release
        # after the process is killed.
        removed = False
        for attempt in range(5):
            try:
                shutil.rmtree(PROJECT_DIR)
                removed = True
                break
            except (PermissionError, OSError) as e:
                if attempt < 4:
                    pretty_step(f"Folder locked, retrying ({attempt + 1}/5) …")
                    time.sleep(2)
                else:
                    # Last-resort on Windows: rename the locked directory aside
                    # and let git clone into a fresh one. The stale directory
                    # will be cleaned up later (e.g. on next reboot or by the
                    # user manually). This avoids blocking the deploy workflow
                    # when the JVM holds file locks that we cannot release.
                    if os.name == "nt":
                        stale_dir = PROJECT_DIR + f".stale.{int(time.time())}"
                        pretty_step(f"Could not remove {PROJECT_DIR}: {e}")
                        pretty_step(f"Renaming stale directory to {stale_dir} …")
                        try:
                            os.rename(PROJECT_DIR, stale_dir)
                            removed = True
                        except OSError as rename_err:
                            pretty_step(f"Rename also failed: {rename_err}")
                    else:
                        pretty_step(f"Could not fully remove {PROJECT_DIR}: {e}")
        if not removed:
            pretty_step("Will attempt clone into the directory as-is.")
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Clone and checkout.
    pretty_step(f"Cloning {REPO_URL} into {PROJECT_DIR} …")
    run(["git", "clone", REPO_URL, PROJECT_DIR])

    pretty_step("Fetching all refs …")
    run(["git", "fetch", "--all", "--tags"], cwd=PROJECT_DIR)

    pretty_step(f"Checking out {sha} ({variant} source for inspection) …")
    run(["git", "checkout", sha], cwd=PROJECT_DIR)

    if action == "clone_only":
        pretty_section(f"http4s repository cloned and checked out at: {PROJECT_DIR}")
        sys.exit(0)

    # Verify prerequisites.
    if use_docker:
        check_prereq("docker")
    else:
        for tool in ("java", "scala-cli"):
            check_prereq(tool)

    # Clean up any prior deployment.
    clean(heading=False)

    # Write the reproduction Scala source against the selected artifact version.
    repro_path = write_repro_source(artifact_version)

    # Launch the reproduction server.
    if use_docker:
        launch_in_docker(repro_path, port)
    else:
        launch_on_host(repro_path, port)

    # Wait for the server to be ready. sbt first-run compilation can take a
    # while, so use a generous timeout.
    pretty_step(f"Waiting for Ember server to accept connections on port {port} …")
    if not _wait_for_port("127.0.0.1", port, timeout=300):
        pretty_section("WARNING: server did not become ready in 5 minutes", color="yellow")
        log_path = os.path.join(PROJECT_DIR, "server.log")
        print(f"  See {log_path} for the full sbt/scala-cli output.")
        return

    pretty_section("http4s reproduction server is ready", color="green")
    print(f"\nServer is live at http://127.0.0.1:{port}/")
    print("Reproduce bug #5069 with:")
    print(f'  curl -v -H "Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5" http://127.0.0.1:{port}/')
    print("  → buggy build:    HTTP/1.1 500 Internal Server Error")
    print("  → patched build:  HTTP/1.1 200 OK")


def stop(heading=True):
    """Stop the running http4s reproduction server without removing sources."""
    if heading:
        pretty_section("Stopping http4s reproduction server …")

    # Host path: kill the scala-cli process by PID file.
    pid_path = os.path.join(PROJECT_DIR, "server.pid")
    if os.path.exists(pid_path):
        with open(pid_path, encoding="utf-8") as f:
            pid = int(f.read().strip())
        try:
            print(f"  Stopping host process {pid} …")
            if os.name == "nt":
                # Windows: kill the entire process tree (scala-cli.bat → JVM).
                # Without /T, taskkill leaves the JVM child alive, which keeps
                # file locks on .git/objects/pack/*.pack and prevents rmtree
                # from removing the project directory on the next deploy.
                subprocess.run(
                    ["taskkill", "/PID", str(pid), "/T", "/F"],
                    check=False,
                    capture_output=True,
                )
            else:
                os.kill(pid, 15)  # SIGTERM
        except ProcessLookupError:
            print(f"  Process {pid} not running.")
        except PermissionError as e:
            print(f"  Could not stop process {pid}: {e}")
        os.remove(pid_path)

    # Docker path: stop the container (do not remove it — clean() does that).
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True, text=True,
    )
    if CONTAINER_NAME in result.stdout.splitlines():
        print(f"  Stopping container {CONTAINER_NAME} …")
        subprocess.run(["docker", "stop", CONTAINER_NAME], check=False)

    print("Done stopping http4s reproduction server.")


def clean(heading=True):
    """Complete cleanup of the http4s deployment: stop server, remove container."""
    if heading:
        pretty_section("Cleaning http4s reproduction server …")

    # Stop everything first.
    stop(heading=False)

    # Remove Docker container if present.
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True, text=True,
    )
    if CONTAINER_NAME in result.stdout.splitlines():
        print(f"  Removing container {CONTAINER_NAME} …")
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], check=False)

    print("Cleanup complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Deploy http4s reproduction server for Defects4REST bug #5069. "
            "The reproduction server uses a published http4s artifact "
            "(buggy=0.22.2, patched=0.22.3). The corresponding historical "
            "git SHA is checked out alongside for code inspection."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # Deploy the buggy version (returns HTTP 500 on the wildcard Accept-Language):\n"
            "  python deploy_http4s.py --buggy\n\n"
            "  # Deploy the patched version (returns HTTP 200):\n"
            "  python deploy_http4s.py --patched\n\n"
            "  # Verify the bug:\n"
            '  curl -v -H "Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5" http://127.0.0.1:8080/'
        ),
    )
    variant_group = parser.add_mutually_exclusive_group()
    variant_group.add_argument(
        "--buggy",
        action="store_const",
        dest="sha",
        const=BUGGY_SHA,
        help=(
            "Deploy the buggy version: http4s 0.22.2 (last release containing "
            "the Accept-Language wildcard parsing bug). Git checkout: 82f8c4b9... "
            "[default]"
        ),
    )
    variant_group.add_argument(
        "--patched",
        action="store_const",
        dest="sha",
        const=PATCHED_SHA,
        help=(
            "Deploy the patched version: http4s 0.22.3 (first release containing "
            "the fix from PR #5070). Git checkout: 3a617522..."
        ),
    )
    parser.add_argument(
        "--sha",
        type=str,
        default=None,
        help=(
            "Explicit git commit SHA to check out (alternative to --buggy/--patched). "
            "Must be one of: 82f8c4b9... (buggy) or 3a617522... (patched)."
        ),
    )
    parser.set_defaults(sha=BUGGY_SHA)
    parser.add_argument(
        "--issue-id",
        type=str,
        default="5069",
        help="GitHub issue number (used for logging and hooks)",
    )
    parser.add_argument(
        "--action",
        type=str,
        default="deploy",
        choices=["deploy", "clone_only"],
        help="deploy = checkout + launch server; clone_only = checkout only",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Host port to expose the reproduction server on (default: 8080)",
    )
    parser.add_argument(
        "--use-docker",
        action="store_true",
        help="Run scala-cli inside a Docker container instead of on the host",
    )
    args = parser.parse_args()

    main(
        sha=args.sha,
        issue_id=args.issue_id,
        action=args.action,
        port=args.port,
        use_docker=args.use_docker,
    )
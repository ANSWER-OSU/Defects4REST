# http4s#5069 — Accept-Language parser fails on wildcard `*` in 0.22

## Description

The `Accept-Language` header parser in http4s 0.22+ rejects the wildcard token `*;q=0.5` even though it is a valid production per [RFC 9110 §12.5.4](https://www.rfc-editor.org/rfc/rfc9110.html#name-accept-language). The example header value `fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5` — taken verbatim from [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language) — parses successfully on http4s 0.21.24 but fails on 0.22.2 and later, returning:

```
Left(org.http4s.ParseFailure: Invalid Accept-Language header:
     Error(0,NonEmptyList(InRange(0,A,Z), InRange(0,a,z))))
```

The parser grammar expects an alphabetic language tag where the wildcard `*` appears, instead of accepting `*` as a valid `language-range` production as required by RFC 9110.

This is a REST API bug for two reasons:

1. **Breaks content negotiation.** Any REST client that sends a valid `Accept-Language` header containing a wildcard catch-all entry (an extremely common pattern recommended by MDN, used by browsers such as Firefox and Safari, and produced by Spring's `LocaleContextResolver`) will be rejected by an http4s server that tries to read the header through `Accept-Language.parse(...)`. The server-side code receives `Left(ParseFailure(...))` instead of `Right(Accept-Language(...))`, which typically surfaces as a `500 Internal Server Error` because the application does not expect the parser to fail on a syntactically valid header.

2. **Silent regression from 0.21.x.** The same header value parsed successfully on http4s 0.21.24, so applications that upgraded from 0.21.x to 0.22.x experienced the regression without any code change on their side. This is the worst class of HTTP bug: a syntactically valid request from a well-behaved client is rejected, and the rejection is reported as a server-side failure rather than a client-side failure.

The fix (PR [#5070](https://github.com/http4s/http4s/pull/5070)) updates the parser grammar to accept `*` as a valid `language-range` production, mirroring RFC 9110 §12.5.4, and adds regression tests to `AcceptLanguageSuite.scala`.

## GitHub Issue URL

https://github.com/http4s/http4s/issues/5069

## Triggering Endpoints

The bug is triggered when an http4s server-side handler explicitly parses the `Accept-Language` request header (for example, to perform content negotiation, locale selection, or localization). The bug therefore affects **every** endpoint that performs such parsing. In the reproduction server used below, only `GET /` is exposed, but any route that calls `Accept-Language.parse(...)` exhibits the same behavior.

| Method | Path | Notes |
|--------|------|-------|
| `GET` | `/` | Used in the reproduction below. Any other route that parses `Accept-Language` exhibits the same behavior. |
| `GET` | `/localized/<resource>` | A typical content-negotiation endpoint that selects a language variant from `Accept-Language`. |
| `POST` | `/anything` | Affects every method, since the failure occurs during header parsing rather than during routing or body decoding. |

## Triggering Behavior

### Reproducibility Approach

Bug #5069 was fixed in PR #5070 and released in http4s **0.22.3**. The exact historical git SHAs in the CSV (`buggy_sha = 82f8c4b9…`, `patch_sha = 3a617522…`) are checked out into the project directory for **code inspection**. The running reproduction server, however, is compiled against **published Maven Central artifacts** rather than from the historical source tree, because building old http4s commits requires a matching historical JDK and sbt toolchain that is impractical to require from every reviewer.

This approach is consistent with how Defects4REST handles projects that publish Docker images to Docker Hub (`buggy_docker_version` / `patched_docker_version` columns in the CSV schema): the historical commit provides metadata and source provenance, while a published artifact provides the running binary.

The two artifact versions used here are both from the **0.22.x line** (rather than jumping to 0.23.x for the patched build). This keeps the `EmberServerBuilder` API identical between the two variants — the only difference between 0.22.2 and 0.22.3 is the parser grammar fix in `Accept-Language.scala` / `Content-Language.scala`, which is exactly the bug being reproduced. This means `ReproServer.scala` compiles unchanged against either artifact version.

| Variant | http4s artifact | Maven Central coordinates | Contains fix? |
|---------|-----------------|--------------------------|---------------|
| `buggy`   | `0.22.2` | `org.http4s::http4s-ember-server::0.22.2` | No — last release containing the bug |
| `patched` | `0.22.3` | `org.http4s::http4s-ember-server::0.22.3` | Yes — first release containing the fix (PR #5070) |

To switch between buggy and patched behavior, change the `//> using lib` directives at the top of `ReproServer.scala` (or pass `--buggy` / `--patched` to the deploy script).

### Prerequisites

1. A JVM with Scala 2.13 and `scala-cli` installed.
2. `git` (the reproduction does not require Docker, since the reproduction server is a single Scala file run via `scala-cli`).
3. A checkout of the http4s repository at the buggy commit (for source inspection):
   ```bash
   git clone https://github.com/http4s/http4s.git
   cd http4s
   git checkout 82f8c4b90b08bd6e037b400db52f20b86d666c23
   ```
   The historical commit is checked out for **code inspection only** — the running reproduction server uses a published http4s artifact (see "Reproducibility Approach" above for why).
4. A minimal Ember-based http4s server that exposes one route which explicitly parses the `Accept-Language` header. Save the following as `ReproServer.scala`:

   ```scala
   //> using scala 2.13.12
   //> using lib org.http4s::http4s-ember-server::0.22.2
   //> using lib org.http4s::http4s-dsl::0.22.2

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
             // Explicitly invoke the parser. On the buggy build (SHA 82f8c4b9…)
             // this returns Left(ParseFailure(...)) when the value contains the
             // wildcard token "*;q=0.5". On the patched build (SHA 3a617522…)
             // this returns Right(Accept-Language(...)).
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
         .withHost("127.0.0.1")
         .withPort(8080)
         .withHttpApp(routes)
         .build
         .use(_ => IO.never)
   }
   ```

   To switch to the patched build, replace `0.22.2` with `0.22.3` in both `//> using lib` directives.

5. Start the server:
   ```bash
   scala-cli run ReproServer.scala
   ```

### Step-by-step reproduction (curl)

The bug can be reproduced with a single `curl` command. The request sends an `Accept-Language` header whose value is the verbatim MDN example, including the wildcard `*;q=0.5` token that the buggy parser rejects:

```bash
# Send an Accept-Language header containing the wildcard token "*;q=0.5".
# On the buggy build (http4s 0.22.2) this triggers a parser failure and the
# server responds with 500.
# On the patched build (http4s 0.22.3) the parser succeeds and the server
# responds with 200, echoing back the parsed value.
curl -v \
  -H "Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5" \
  http://127.0.0.1:8080/
```

The same request can also be issued from Postman by setting the method to `GET`, URL to `http://127.0.0.1:8080/`, and adding a single header:

| Key | Value |
|-----|-------|
| `Accept-Language` | `fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5` |

No authentication, request body, or query parameters are required.

### Equivalent raw socket reproduction

If `curl` is unavailable, the same request can be sent with any netcat:

```bash
{
  printf 'GET / HTTP/1.1\r\n'
  printf 'Host: 127.0.0.1:8080\r\n'
  printf 'Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5\r\n'
  printf 'Connection: close\r\n'
  printf '\r\n'
} | nc 127.0.0.1 8080
```

## Buggy Response

Observed response when running the reproduction server against http4s artifact `0.22.2`:

```
HTTP/1.1 500 Internal Server Error
Content-Type: text/plain; charset=UTF-8
Content-Length: 119
Date: Wed, 14 Oct 2026 19:56:36 GMT

Accept-Language parse failure: Invalid Accept-Language header: Error(37,NonEmptyList(InRange(37,A,Z), InRange(37,a,z)))
```

- **Status code:** `500` (Internal Server Error)
- **Body:** the message of the underlying `ParseFailure`, surfaced to the client because the reproduction server maps `Left(err)` to `InternalServerError`. In a real application, this would typically surface as an unhandled exception and the body would be a generic `500` page.
- **Server logs:** the parse failure is not logged by default because it is returned as a `ParseResult` rather than thrown as an exception. Operators see only the resulting `500` in access logs.
- **Error position `37`:** the byte offset of the `*` character in the `Accept-Language` header value, which is exactly where the buggy parser expected an alphabetic language tag and instead encountered the wildcard.

## Expected Response

Observed response after switching the reproduction server to http4s artifact `0.22.3` (which contains the fix from PR #5070):

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8
Content-Length: 81
Date: Wed, 14 Oct 2026 20:02:50 GMT

Parsed Accept-Language successfully: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5
```

- **Status code:** `200` (OK)
- **Body:** confirmation that the `Accept-Language` header parsed successfully, followed by the canonical rendering of the parsed value (which round-trips through the parser and the renderer).
- **Server logs:** no parse failure is emitted.

## Patched Files

| File | Role |
|------|------|
| `core/src/main/scala/org/http4s/headers/Accept-Language.scala` | Updates the parser grammar to accept `*` as a valid `language-range` production, conforming to RFC 9110 §12.5.4. Specifically, the language-tag parser changes from `string(alpha.rep)` to `(alpha.rep \| charIn('*')).string`. |
| `core/src/main/scala/org/http4s/headers/Content-Language.scala` | Same parser fix applied to the symmetric `Content-Language` response header. |
| `laws/src/main/scala/org/http4s/laws/discipline/ArbitraryInstances.scala` | Adds generator cases for `*` and `*;q=…` so that property-based tests exercise the new grammar. |
| `tests/src/test/scala/org/http4s/headers/AcceptLanguageSuite.scala` | Adds a regression test that parses the MDN example (`fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5`) and asserts a `Right(...)`. |
| `tests/src/test/scala/org/http4s/parser/AcceptLanguageSuite.scala` | Adds a parser-level regression test covering the same input. |

## Verification

The reproduction was verified locally on Windows 11 with `scala-cli 0.3.x` and JDK 11:

| Variant | http4s artifact | HTTP status | Body |
|---------|-----------------|-------------|------|
| `buggy`   | `0.22.2` | `500` | `Accept-Language parse failure: Invalid Accept-Language header: Error(37,NonEmptyList(InRange(37,A,Z), InRange(37,a,z)))` |
| `patched` | `0.22.3` | `200` | `Parsed Accept-Language successfully: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5` |

Both variants are reproducible via the deploy script:

```bash
# Deploy buggy build
python defects4rest/src/deployment_scripts/deploy_http4s.py --buggy
curl -v -H "Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5" http://127.0.0.1:8080/

# Deploy patched build
python defects4rest/src/deployment_scripts/deploy_http4s.py --patched
curl -v -H "Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5" http://127.0.0.1:8080/
```

## References

- Original issue: https://github.com/http4s/http4s/issues/5069
- Fix PR: https://github.com/http4s/http4s/pull/5070
- RFC 9110 §12.5.4 — `Accept-Language`: https://www.rfc-editor.org/rfc/rfc9110.html#name-accept-language
- MDN — `Accept-Language` header reference (example value used in the reproduction): https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language

# enviroCar-server#178

## Description
Track encoding throws an exception due to missing metadata properties in track.json indicating a schema validation issue. (HTTP 307)

## GitHub Issue URL
https://github.com/enviroCar/enviroCar-server/issues/178

## Triggering Endpoint(s)
- `/schema/{schema}`

## Triggering Behavior
**Step 1.** Request a schema
```
curl -I -L http://localhost:8080/schema/sensor.json
```
## Buggy Response
HTTP 307
```
HTTP/1.1 307 Temporary Redirect
Date: Mon, 12 Jan 2026 04:11:04 GMT
Location: http://localhost:8080/schema/sensor.json
Vary: Accept-Encoding
Content-Length: 0
Server: Jetty(9.4.48.v20220622)

HTTP/1.1 307 Temporary Redirect
Date: Mon, 12 Jan 2026 04:11:04 GMT
Location: http://localhost:8080/schema/sensor.json
Vary: Accept-Encoding
Content-Length: 0
Server: Jetty(9.4.48.v20220622)

HTTP/1.1 307 Temporary Redirect
Date: Mon, 12 Jan 2026 04:11:04 GMT
Location: http://localhost:8080/schema/sensor.json
Vary: Accept-Encoding
Content-Length: 0
Server: Jetty(9.4.48.v20220622)

curl: (47) Maximum (50) redirects followed
```

## Expected Response
HTTP 200
```
HTTP/1.1 200 OK
Date: Mon, 12 Jan 2026 04:24:20 GMT
Content-Type: application/json
Vary: Accept-Encoding
Content-Length: 0
Server: Jetty(9.4.48.v20220622)
```
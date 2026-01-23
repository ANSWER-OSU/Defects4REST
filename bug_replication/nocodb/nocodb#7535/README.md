# nocodb#7535

## Description
Viewer users receive HTTP 403 errors and cannot access email notification features due to insufficient permissions on the base and plugins.

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/7535

## Triggering Endpoint(s)
- `/api/v1/db/meta/projects/{projectId}/users/{userId}`
- `/api/v1/db/meta/plugins/{pluginId}/status`

## Prerequisites

**Step 1.** Sign up as CREATOR
```
curl --request POST \
  --url http://localhost:8080/api/v1/auth/user/signup \
  --header 'content-type: application/json' \
  --data '{
  "email": "admin@example.com",
  "password": "admin123"
}'
```
**Response:** HTTP 200.
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWQiOiJ1czI1ampicDJmZGE4NzYyIiwicm9sZXMiOiJvcmctbGV2ZWwtY3JlYXRvcixzdXBlciIsInRva2VuX3ZlcnNpb24iOiJjYjYzOGEzMzY5MDlmNDIwMDNkZGU0YWNiNzhjZDM3Y2JhMTFiZTU4ZjZiMGUyMThkN2Y1MDE2ZWZjNTE4YzY3YWRlM2FiMGExOTc1ZjlkNSIsImlhdCI6MTc2NjQ1OTk1OSwiZXhwIjoxNzY2NDk1OTU5fQ.DLSe9tMRw3LNNxeUXQCCfo2HJ8xzZVHF_HACyJ7BxIE",
  "createdProject": {
    "is_meta": 1,
    "id": "pz42uzjzu92svnw",
    "title": "Getting Started",
    "prefix": "nc_cp84__",
    ...
    ...
    "tables": [
      {
        "id": "md5i75ivra2f6uh",
        "source_id": "bdmp98s23nia76w",
        "base_id": "pz42uzjzu92svnw",
        "table_name": "nc_cp84___Features",
        "title": "Features",
        "type": "table",
       ...
}
```

**Step 2.** Sign up as USER/VIEWER
```
curl --request POST \
  --url http://localhost:8080/api/v1/auth/user/signup \
  --header 'content-type: application/json' \
  --data '{
  "email": "user@example.com",
  "password": "user12345"
}'
```
**Response:** HTTP 200.
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJpZCI6InVzcHZueTkwcmFpaHNub2EiLCJyb2xlcyI6Im9yZy1sZXZlbC12aWV3ZXIiLCJ0b2tlbl92ZXJzaW9uIjoiZmUyNDAzNzBlYTRkYzQzNTBmMDI0YTZkYjYyOTkzZmJkNzM0ZTI0ZTI0ZGIyYzAzOTA0MGEwM2EyMjc3NjM0ZTk5NTNhY2I1NzU1M2NjMWEiLCJpYXQiOjE3NjY0NTk5OTMsImV4cCI6MTc2NjQ5NTk5M30.PEqqJYa6QYXMGPorDRLc6nEbTCf3I6FfTA4Ha4Ur7iU"
}
```

**Step 3.** List plugins
```
curl --request GET \
  --url http://localhost:8080/api/v1/db/meta/plugins \
  --header 'xc-auth: <CREATOR_TOKEN>'
```
**Response:** HTTP 200.
```
...,
{
      "id": "nc9kctewdqaxj9zk",
      "title": "SMTP",
      "description": "SMTP email client",
      "active": 0,
      "rating": null,
      "version": "0.0.2",
      "docs": null,
      "status": "install",
      "status_details": null,
      "logo": null,
      "icon": null,
      "tags": "Email",
      "category": "Email",
	  ...
}
```

**Step 4.** Activate SMTP plugin
```
curl --request PATCH \
  --url http://localhost:8080/api/v1/db/meta/plugins/nc9kctewdqaxj9zk \
  --header 'content-type: application/json' \
  --header 'xc-auth: <CREATOR_TOKEN>' \
  --data '{
  "active": true
}'
```
**Response:** HTTP 200.
```
{
  "id": "nc9kctewdqaxj9zk",
  "title": "SMTP",
  "description": "SMTP email client",
  "active": true,
  "rating": null,
  "version": "0.0.2",
  ...,
}
```

**Step 5.** Create form view
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/meta/tables/md5i75ivra2f6uh/forms \
  --header 'accept: application/json, text/plain, */*' \
  --header 'content-type: application/json' \
  --header 'xc-auth: <CREATOR_TOKEN>' \
  --data '{
  "title": "ExampleForm",
  "type": 1,
  "copy_from_id": null,
  "fk_grp_col_id": null,
  "fk_geo_data_col_id": null
}'
```
**Response:** HTTP 200.
```
{
  "id": "vwrakhl2vdipvztw",
  "source_id": "bdmp98s23nia76w",
  "base_id": "pz42uzjzu92svnw",
  "fk_model_id": "md5i75ivra2f6uh",
  "title": "ExampleForm",
  ...
}
```

**Step 6.** List users
```
curl --request GET \
  --url http://localhost:8080/api/v1/users \
  --header 'xc-auth: <CREATOR_TOKEN>'
```
**Response:** HTTP 200.
```
{
  "list": [
    ...,
    {
      "id": "uspvny90raihsnoa",
      "email": "user@example.com",
      "email_verified": null,
      "invite_token": null,
      "created_at": "2025-12-23 03:19:53+00:00",
      "updated_at": "2025-12-23 03:19:53+00:00",
      "roles": "org-level-viewer",
      "projectsCount": 0
    }
  ],
  ...
}
```

## Triggering Behavior
**Step 1.** Change USER's role to CREATOR
```
curl --request PATCH \
  --url http://localhost:8080/api/v1/db/meta/projects/pz42uzjzu92svnw/users/uspvny90raihsnoa \
  --header 'accept: application/json, text/plain, */*' \
  --header 'content-type: application/json' \
  --header 'xc-auth: <CREATOR_TOKEN>' \
  --data '{
  "email": "user@example.com",
  "roles": "creator"
}'
```
**Response:** HTTP 200.
```
{
  "msg": "The user has been updated successfully"
}
```

**Step 2.** Get SMTP plugin status as USER/VIEWER
```
curl --request GET \
  --url http://localhost:8080/api/v1/db/meta/plugins/SMTP/status \
  --header 'accept: application/json, text/plain, */*' \
  --header 'xc-auth: <USER_TOKEN>'
```
## Buggy Response:
HTTP 403 with the following response
```
{
    "msg": "isPluginActive - : Not allowed"
}
```
## Expected Response:
HTTP 200
```
true
```
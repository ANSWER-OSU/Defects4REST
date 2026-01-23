## nocodb#2776

## Description
The API fails with a Type Error (HTTP 400) due to attempting to read 'endsWith' null indicating a runtime code issue in MysqlClient.

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/2776

## Triggering Endpoints:
- `api/v1/meta/bases/{baseId}/{sourceId}/tables`
- `api/v1/meta/tables/{tableId}`
- `api/v1/meta/columns/{columnId}`

## Prerequisites
**Step 1.** Sign up

```
curl -X POST "http://localhost:8080/api/v1/db/auth/user/signup" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --data-raw '{
    "email": "admin@admin.com",
    "password": "@Admin123",
    "ignore_subscribe": true
  }'
```
**Response:** HTTP 200.
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfampiMjBveTRmaWtyamwiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJ0b2tlbl92ZXJzaW9uIjoiMjY3YzJiNzVjNTZiOTFiYjEwZTg1OGMxZTI4MGM3NTVlNjk0NTIwYTBmYWYyOWZmMDdmMjZkOTAxNmFkZDA4ZGQyMDY2NmIyYzE0NWQwYzkiLCJpYXQiOjE3NjYxOTEzOTIsImV4cCI6MTc2NjIyNzM5Mn0.Q_CR5SVnFuZc1OhKQ-uL1TnqTkS7jxS5Z0Rbf2B4y6Y"
}
```

**Step 2.** Create a project
```
curl -X POST "http://localhost:8080/api/v1/db/meta/projects" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "xc-auth: <XC_TOKEN>" \
  --data-raw '{
    "title": "Buggy2776"
  }'
```
**Response:** HTTP 200.
```
{
    "is_meta": 1,
    "id": "p_k3cbxk50bhsdfa",
    "title": "Buggy2776",
    "prefix": "nc_dagu__",
    "status": null,
    "description": null,
    "meta": null,
    "color": null,
    "uuid": null,
    "password": null,
    "roles": null,
    "deleted": 0,
    "order": null,
    "created_at": "2025-12-20 00:11:16",
    "updated_at": "2025-12-20 00:11:16",
    "bases": [
        {
            "id": "ds_rzw5zlygqoquqq",
            "project_id": "p_k3cbxk50bhsdfa",
            "alias": null,
            "meta": null,
            "is_meta": 1,
            "type": "sqlite3",
            "inflection_column": "camelize",
            "inflection_table": "camelize",
            "created_at": "2025-12-20 00:11:16",
            "updated_at": "2025-12-20 00:11:16"
        }
    ]
}

```

## Triggering Behavior:
**Step 3.** Create table 'Bug2776Table'
```
curl -s -X POST "http://localhost:8080/api/v1/meta/bases/p_k3cbxk50bhsdfa/ds_rzw5zlygqoquqq/tables" -H "xc-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdDd5N29hMGsxM2tqbW0iLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJ0b2tlbl92ZXJzaW9uIjoiODBmNjIwNzcyZmFiOWY5ZDViMDI0ZDFiYTViNzJkYjE5OTM4ZmQ4OWZiZDgxNDExYzhkOGE1ODg1YTJkZDdjZDM3MTEzZjlkMDJjNDFkNWQiLCJpYXQiOjE3NjYxODk0MzQsImV4cCI6MTc2NjIyNTQzNH0.VR02Eu04H7sNx4rUhdbGuHUmWKe1Qbzru-t-zCaahYs" -H "Content-Type: application/json" -d '{"title":"Bug2776Table","table_name":"bug2776_table","columns":[{"title":"Id","column_name":"id","uidt":"ID","dt":"int","ct":"int unsigned","pk":true,"ai":true,"un":true,"rqd":true}]}' | jq
```
**Response:** HTTP 200
```
{
    "id": "tb_jx9p8q7r6s5t4u3v2w1",
    "title": "Bug2776Table",
    "table_name": "bug2776_table"
}
```

**Step 2.** Add a text column called 'status' to the created table
```
curl -s -X POST "http://localhost:8080/api/v1/meta/tables/tb_jx9p8q7r6s5t4u3v2w1/columns" \
 -H "xc-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.YXNkZnM0Nzc2ZXhhbXBsZQ" \
 -H "Content-Type: application/json" \
 -d '{
    "title": "status",
    "column_name": "status",
    "uidt": "Text"
}' | jq .
```
**Response:** HTTP 200
```
{
 "id": "cl_yssmfj5zxz5s8m",
 "title": "status",
 "uidt": "Text"
}
```

**Step 3.** Add data to the created 'status' column with same column id "cl_yssmfj5zxz5s8m"
```
curl -v -s -X PATCH "http://localhost:8080/api/v1/meta/columns/cl_yssmfj5zxz5s8m" \
 -H "xc-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.YXNkZnM0Nzc2ZXhhbXBsZQ" \
-H "Content-Type: application/json" \
-d '{
    "title": "Status",
    "column_name": "status",
    "uidt": "SingleSelect",
    "meta": {
        "options": [
            "Todo",
            "Doing",
            "Done"
        ]
    },
    "ct": null
}'
```
## Buggy Response:
HTTP 400 Bad Request
```
{"message":"Cannot read properties of null (reading 'endsWith')"}
```
## Expected Response:
HTTP 2XX with a JSON body showing the updated column
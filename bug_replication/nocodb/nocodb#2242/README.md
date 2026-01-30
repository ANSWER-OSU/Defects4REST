# nocodb#2242

## Description
The API response for a field with thousands of linked records is truncated without pagination or a way to retrieve all connections (HTTP 200) indicating improper handling of large result sets and missing query parameters for pagination.

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/2242

## Triggering Endpoint
`/api/v1/db/data/noco/{projectName}/{tableName}/{rowId}`

## Triggering Behavior
**Step 1.** Signin as a super user (admin)
```
curl 'http://localhost:8081/api/v1/db/auth/user/signin' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"admin@admin.com","password":"@Admin123"}'
```
**Response:** HTTP 200
```
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfazUxcXE0MnUzaTN1eGgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjUzODA5MjV9.2M6aW09b6PAr8uSA11qDZOYpRMVyR3GtkAsAS9W-OeU"}
```
**Step 2.** Retrieve the data for a table's row with 1000 `hasMany` values
```
curl -X 'GET' \
  'http://localhost:8080/api/v1/db/data/noco/Buggy2242/Country/1' \
  -H 'accept: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfazUxcXE0MnUzaTN1eGgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjUzODA5MjV9.2M6aW09b6PAr8uSA11qDZOYpRMVyR3GtkAsAS9W-OeU'
```
## Buggy Response:
HTTP 200. Data is truncated up to 20 only, even if pagination is not requested.
```
{
  "ID": 1,
  "Title": "b1",
  "nc_hm4g___nc_m2m_31thpd39zpList": [
    {
      "table2_id": 1,
      "table1_id": 1
    },
    {
      "table2_id": 1,
      "table1_id": 2
    },
    {
      "table2_id": 1,
      "table1_id": 3
    },
    {
      "table2_id": 1,
      "table1_id": 4
    },
    ...
    {
      "table2_id": 1,
      "table1_id": 20
    }
  ],
  "cityList": [
    {
      "ID": 1,
      "Title": "city_0"
    },
    {
      "ID": 2,
      "Title": "city_1"
    },
    {
      "ID": 3,
      "Title": "city_2"
    },
    ...
    {
      "ID": 20,
      "Title": "city_19"
    }
  ],
  "CountryMMList": [
    {
      "ID": 1,
      "Title": "city_0"
    },
    {
      "ID": 2,
      "Title": "city_1"
    },
    {
      "ID": 3,
      "Title": "city_2"
    },
    {
      "ID": 4,
      "Title": "city_3"
    },
    ...
    {
      "ID": 20,
      "Title": "city_19"
    }
  ]
}
```
## Expected Response:
HTTP 200. Data is not truncated
# nocodb#2242

## Description
The API response for a field with thousands of linked records is truncated without pagination or a way to retrieve all connections (HTTP 200) indicating improper handling of large result sets and missing query parameters for pagination.

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/2242

## Triggering Endpoint
`/api/v1/db/data/noco/{projectName}/{tableName}/{rowId}`

## Setup
**Step 1.** Create Table A and B

**Step 2.** Populate Table A with 1000 rows

**Step 3.** In Table B, create a `hasMany` column to Table A

**Step 4.** Populate `hasMany` column in Table B with 1000 rows

## Triggering Behavior
**Step 1.** Retrieve the data for a table's row with 1000 `hasMany` values
```
curl -X 'GET' \
  'http://localhost:8080/api/v1/db/data/noco/Buggy2242/Country/1' \
  -H 'accept: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfazUxcXE0MnUzaTN1eGgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjUzODA5MjV9.2M6aW09b6PAr8uSA11qDZOYpRMVyR3GtkAsAS9W-OeU'
```
## Buggy Response:
HTTP 200. Data is truncated
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
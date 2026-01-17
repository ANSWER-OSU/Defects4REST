# **Dolibarr 30161**
 
## Description
The API endpoints ignore provided ref or track_id parameters and always return a specimen ticket due to incorrect conditional logic in parameter handling.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/30161
## Triggering Endpoints
*  /tickets
*  /tickets/ref/{ref}
*  /tickets/track_id/{track_id}

## Triggering Behavior
### Step 1: Create a ticket via API
```
curl -s -X POST "http://localhost:8080/api/index.php/tickets" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Ticket for Bug #30161",
    "message": "This is a test ticket to reproduce the bug",
    "type_code": "OTHER"
  }' | jq
```

**Response:** HTTP 200 with ticket details including `ref` and `track_id`

Example response:
```
{
  "id": 1,
  "ref": "TI2401-0001",
  "track_id": "ABCD1234",
  "subject": "Test Ticket for Bug #30161",
  ...
}
```


### Step 2: Try to fetch the ticket by ref
```
curl -s -X GET "http://localhost:8080/api/index.php/tickets/ref/TI2401-0001" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" | jq
```

## Buggy Response
HTTP 200 with specimen ticket data (not the actual ticket)
```
{
  "id": 0,
  "ref": "(PROV)",
  "track_id": "SPECIMEN",
  "subject": "Specimen ticket subject",
  "message": "Specimen ticket message",
  ...
}
```
## Expected Response:
HTTP 200 with the actual ticket data matching the `ref`
```
{
  "id": 1,
  "ref": "TI2401-0001",
  "track_id": "ABCD1234",
  "subject": "Test Ticket for Bug #30161",
  "message": "This is a test ticket to reproduce the bug",
  ...
}
```

### Step 3: Try to fetch the ticket by track_id
```
curl -s -X GET "http://localhost:8080/api/index.php/tickets/track_id/ABCD1234" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" | jq
```
## Buggy Response
HTTP 200 with specimen ticket data (not the actual ticket)
```
{
  "id": 0,
  "ref": "(PROV)",
  "track_id": "SPECIMEN",
  "subject": "Specimen ticket subject",
  "message": "Specimen ticket message",
  ...
}
```
## Expected Response:
HTTP 200 with the actual ticket data matching the `track_id`
```
{
  "id": 1,
  "ref": "TI2401-0001",
  "track_id": "ABCD1234",
  "subject": "Test Ticket for Bug #30161",
  "message": "This is a test ticket to reproduce the bug",
  ...
}
```

### Step 4: Try with a non-existing ref
```
curl -s -X GET "http://localhost:8080/api/index.php/tickets/ref/NONEXISTENT" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" | jq
```
## Buggy Response
HTTP 200 with specimen ticket data
```
{
  "id": 0,
  "ref": "(PROV)",
  "track_id": "SPECIMEN",
  ...
}
```

## Expected Response:
 HTTP 404 - Ticket not found
```
{
  "error": {
    "code": 404,
    "message": "Ticket not found"
  }
}
```
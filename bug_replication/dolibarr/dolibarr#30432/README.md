# **Dolibarr 30432**
 
## Description
API does not allow updating client_code even when Dolibarr is configured to permit custom codes via the Leopard Module.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/30432
## Triggering Endpoints
*  /thirdparties
*  /thirdparties/{id}

## Triggering Behavior

**Step 1.** Create a Thirdparty (Customer)
```
curl -s -X POST "http://localhost:8080/api/index.php/thirdparties" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Company",
    "client": 1
  }' | jq
```

**Response:** HTTP 200 with e.g. `id = 1`:
```
{
  "id": 1,
  "name": "Test Company",
  "code_client": "CU-000001",
  "code_compta": null
}
```

 **Step 2.** Try to Update client_code with Thirdparty id = 1 
```
curl -s -X PUT "http://localhost:8080/api/index.php/thirdparties/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "code_client": "NEW-CODE-001"
  }' | jq
```

## Buggy Response

HTTP 200 and the JSON still contains the old value:
```
{
  "id": 1,
  "name": "Test Company",
  "code_client": "CU-000001",
  "code_compta": null
}
```

## Expected Response

HTTP 200 with the new value applied:
```
{
  "id": 1,
  "name": "Test Company",
  "code_client": "NEW-CODE-001",
  "code_compta": null
}
```

**Step 3.** Try to Update code_compta with Thirdparty id = 1
```
curl -s -X PUT "http://localhost:8080/api/index.php/thirdparties/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "code_compta": "ACCT-12345"
  }' | jq
```

## Buggy Response:

HTTP 200 and the JSON still contains:
```
{
  "id": 1,
  "name": "Test Company",
  "code_client": "CU-000001",
  "code_compta": null
}
```

## Expected Response:

HTTP 200 with the new value applied:
```
{
  "id": 1,
  "name": "Test Company",
  "code_client": "CU-000001",
  "code_compta": "ACCT-12345"
}
```

**Step 4.** Try to Update Both code_client and code_compta Together
```bash
curl -s -X PUT "http://localhost:8080/api/index.php/thirdparties/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "code_client": "NEW-CODE-002",
    "code_compta": "ACCT-67890"
  }' | jq
```

## Buggy Response:

HTTP 200 and the JSON still contains the original values:
```json
{
  "id": 1,
  "name": "Test Company",
  "code_client": "CU-000001",
  "code_compta": null
}
```

## Expected Response:

HTTP 200 with both new values applied:
```json
{
  "id": 1,
  "name": "Test Company",
  "code_client": "NEW-CODE-002",
  "code_compta": "ACCT-67890"
}
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







# **Dolibarr  32145**
 
## Description
The issue is caused by incorrect evaluation of the "private_message" POST parameter value leading to unintended status changes.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/32145
## Triggering Endpoints

/tickets
/tickets/{id}/messages
/tickets/{id}
## Triggering Behavior

**Step 1:** Create a New Ticket

```
curl -s -X POST "http://localhost:8080/api/index.php/tickets" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "BUG-32145-TEST",
    "message": "Test ticket for bug #32145",
    "type_code": "OTHER"
  }' | jq
```

**Response:** HTTP 200
```
{
  "id": 1,
  "ref": "TICK-XXXX",
  "subject": "BUG-32145-TEST",
  "fk_statut": 0
}
```

**Step 2:** Add a Private Message to the Ticket
```
curl -s -X POST "http://localhost:8080/api/index.php/tickets/1/messages" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "This is a private message",
    "private_message": "1"
  }' | jq
```

**Response:** HTTP 200
```
{
  "success": true,
  "message_id": 1
}
```



**Step 3:** Verify Ticket Status Change (Bug Manifestation)

```
curl -s -X GET "http://localhost:8080/api/index.php/tickets/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq
```

## Buggy Response
HTTP 200  with fk_statut` changed to `3` ("IN PROGRESS"), even though the message was marked as private.
```json
{
  "id": 1,
  "ref": "TICK-XXXX",
  "subject": "BUG-32145-TEST",
  "fk_statut": 3
}
```



## Expected Response:
HTTP 200
```
{
  "id": 1,
  "ref": "TICK-XXXX",
  "subject": "BUG-32145-TEST",
  "fk_statut": 0
}
```
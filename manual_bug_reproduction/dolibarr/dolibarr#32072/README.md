# **Dolibarr  32072**
 
## Description
The PUT /shipments/{id} endpoint does not update extra fields in array_options due to missing handling in the API implementation compared to the products API.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/32072
## Triggering Endpoints

 - /shipments 
 - /shipments/{id}

## Triggering Behavior


**Step 1:** Create a Shipment
```
curl -s -X POST "http://localhost:8080/api/index.php/shipments" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": 1,
    "ref": "SHIP-BUG-32072",
    "array_options": {
      "options_custom_field": "Initial Value"
    }
  }' | jq
```

**Response:** HTTP 200
```
{
  "id": 1,
  "ref": "SHIP-BUG-32072",
  "socid": 1,
  "array_options": {
    "options_custom_field": "Initial Value"
  }
}
```

---

**Step 2:** Attempt to Update Extra Field Using PUT
```
curl -s -X PUT "http://localhost:8080/api/index.php/shipments/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "array_options": {
      "options_custom_field": "Updated Value"
    }
  }' | jq
```
## Buggy Response
 HTTP 200, The `options_custom_field` value remains "Initial Value" instead of changing to "Updated Value".
```
{
  "id": 1,
  "ref": "SHIP-BUG-32072",
  "array_options": {
    "options_custom_field": "Initial Value"
  }
}
```

## Expected Response:

**Expected Response:** HTTP 200
```
{
  "id": 1,
  "ref": "SHIP-BUG-32072",
  "array_options": {
    "options_custom_field": "Updated Value"
  }
}
```





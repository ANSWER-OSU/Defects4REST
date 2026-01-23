# **Dolibarr  32096**
 
## Description
The linkedObjectsIds field is null when using a search query but is populated when fetching by ID indicating inconsistent handling of search parameters in the API.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/32096
## Triggering Endpoints

 - /thirdparties 
 - /shipments 
 - /orders

## Triggering Behavior

 **Step 1:** Create a Third Party (Customer)

```
curl -s -X POST "http://localhost:8080/api/index.php/thirdparties" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Customer for Bug 32096",
    "client": 1
  }' | jq
```

**Response:** HTTP 200 with body customer id = 1

**Step 2:** Create an Order

```
curl -s -X POST "http://localhost:8080/api/index.php/orders" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": 1,
    "date": 1732492800,
    "lines": [
      {
        "subprice": 100,
        "qty": 1,
        "desc": "Test product"
      }
    ]
  }' | jq
```

**Response:** HTTP 200 with order ID = 5

**Step 3:** Create a Shipment Linked to the Order

```
curl -s -X POST "http://localhost:8080/api/index.php/shipments" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": 1,
    "origin_id": 5,
    "origin_type": "order"
  }' | jq
```

**Response:** HTTP 200 with shipment ID 3

**Step 4:** Search for the Order Using sqlfilters

```
curl -s -X GET "http://localhost:8080/api/index.php/orders?sqlfilters=t.rowid:=:5" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq
```
## Buggy Response
HTTP 200 linkedObjectsIds` is `null` instead of containing the linked shipment.
```
[
  {
    "module": null,
    "id": "5",
    "entity": "1",
    "import_key": null,
    "array_options": [],
    "array_languages": null,
    "contacts_ids": [],
    "linkedObjectsIds": null,
    "canvas": null,
    "fk_project": null,
    "contact_id": null,
    "user": null,
    "origin_type": null,
    "origin_id": null,
    "ref": "SO2411-0003"
  }
]
```

## Expected Response:
HTTP 200
```
{
  "module": null,
  "id": "5",
  "entity": "1",
  "import_key": null,
  "array_options": [],
  "array_languages": null,
  "contacts_ids": [],
  "linkedObjectsIds": {
    "shipping": {
      "3": "3"
    }
  },
  "canvas": null,
  "fk_project": null,
  "contact_id": null,
  "user": null,
  "origin_type": null,
  "origin_id": null,
  "ref": "SO2411-0003"
}
```





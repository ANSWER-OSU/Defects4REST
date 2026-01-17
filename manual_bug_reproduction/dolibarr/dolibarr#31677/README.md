# **Dolibarr  31677**
 
## Description
API is missing support for the DefaultWorkstationId field resulting in incomplete or invalid payload handling for BomLine.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/31677
## Triggering Endpoints

*  /boms
* /boms/{id} 
*  /boms/{id}/lines
* /products
* /workstations

## Triggering Behavior

 **Step 1:** Create a Product
```
curl -s -X POST "http://localhost:8080/api/index.php/products" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "PROD-BUG-31677",
    "label": "Test Product for BOM Bug 31677"
  }' | jq
```

**Response:** HTTP 200
```
{
  "id": "1",
  "ref": "PROD-BUG-31677",
  "label": "Test Product for BOM Bug 31677"
}
```

**Step 2:** Create a Workstation
```
curl -s -X POST "http://localhost:8080/api/index.php/workstations" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "WS-001",
    "label": "Test Workstation"
  }' | jq
```

**Response:** HTTP 200
```
{
  "id": "1",
  "ref": "WS-001",
  "label": "Test Workstation"
}
```
 **Step 3:** Create a BOM with BOM Lines including DefaultWorkstationId
```
curl -s -X POST "http://localhost:8080/api/index.php/boms" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "BOM-BUG-31677",
    "label": "Test BOM for Bug 31677",
    "fk_product": 1,
    "lines": [
      {
        "fk_product": 1,
        "qty": 2,
        "fk_default_workstation": 1
      }
    ]
  }' | jq
```
## Buggy Response
HTTP 200, but the `fk_default_workstation` field is not saved or returned:
```
{
  "id": "1",
  "ref": "BOM-BUG-31677",
  "lines": [
    {
      "fk_product": 1,
      "qty": 2,
      "fk_default_workstation": null
    }
  ]
}
```
## Expected Response:
HTTP 200 with `fk_default_workstation` properly saved:
```
{
  "id": "1",
  "ref": "BOM-BUG-31677",
  "lines": [
    {
      "fk_product": 1,
      "qty": 2,
      "fk_default_workstation": 1
    }
  ]
}
```


**Step 3:** Try to Update BOM Line with DefaultWorkstationId
```
curl -s -X PUT "http://localhost:8080/api/index.php/boms/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "lines": [
      {
        "fk_product": 1,
        "qty": 2,
        "fk_default_workstation": 1
      }
    ]
  }' | jq
```
## Buggy Response
HTTP 200, but the field remains null or is not updated:
```
{
  "id": "1",
  "lines": [
    {
      "fk_product": 1,
      "qty": 2,
      "fk_default_workstation": null
    }
  ]
}
```
## Expected Response:
HTTP 200 with updated `fk_default_workstation`:
```
{
  "id": "1",
  "lines": [
    {
      "fk_product": 1,
      "qty": 2,
      "fk_default_workstation": 1
    }
  ]
}
```






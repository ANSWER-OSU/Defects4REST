# **Dolibarr  33689**
 
## Description
The issue is caused by a change in the validation logic for POST requests in the supplierorders API which breaks the ability to import order lines.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/33689
## Triggering Endpoints
* /products
* /thirdparties 
* /supplierorders
* /supplierorders/{id}/lines

## Triggering Behavior

**Step 1:** Create a Supplier (Third Party)
```bash
curl -s -X POST "http://localhost:8080/api/index.php/thirdparties" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Supplier for Bug 33689",
    "code_fournisseur": "SUPP-33689",
    "fournisseur": 1
  }' | jq
```

**Response:** HTTP 200 with supplier `id = 1`)
```json
{
  "id": "1",
  "name": "Test Supplier for Bug 33689"
}
```

---

**Step 2:** Create a Product
```bash
curl -s -X POST "http://localhost:8080/api/index.php/products" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "PROD-33689",
    "label": "Test Product for Bug 33689"
  }' | jq
```

**Response:** HTTP 200 with product `id = 1`)
```json
{
  "id": "1",
  "ref": "PROD-33689",
  "label": "Test Product for Bug 33689"
}
```

---

**Step 3:** Create a Supplier Order
```bash
curl -s -X POST "http://localhost:8080/api/index.php/supplierorders" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": 1,
    "ref": "SO-33689-TEST"
  }' | jq
```

**Response:** HTTP 200 with supplier order `id = 1`)
```json
{
  "id": "1",
  "ref": "SO-33689-TEST"
}
```

---

### Step 4: Add Lines to Supplier Order 

    curl -s -X POST "http://localhost:8080/api/index.php/supplierorders/1/lines" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "fk_product": 1,
        "qty": 5,
        "subprice": 10.00,
        "desc": "Test line for supplier order"
      }' | jq

## Buggy Response
HTTP 500 or error response due to validation failure
```
{
  "error": {
    "code": 500,
    "message": "Internal server error - validation failed"
  }
}
```

## Expected Response:
HTTP 200 with line successfully added
```json
{
  "success": {
    "code": 200,
    "message": "Line added successfully",
    "id": "1"
  }
}
```
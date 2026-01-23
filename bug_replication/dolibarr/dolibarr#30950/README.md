# **Dolibarr 30950 **
 
## Description
Creating a supplier invoice via the API from a template results in an incorrect reference suffix indicating a workflow or template misconfiguration.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/30950
## Triggering Endpoints
*  /thirdparties
*  /supplier_invoices

## Triggering Behavior

 **Step 1:** Create a third-party (supplier)
```
curl -s -X POST "http://localhost:8080/api/index.php/thirdparties" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Supplier",
    "client": 0,
    "fournisseur": 1
  }' | jq
```

**Response:** HTTP 200 with supplier `id = 1`

 **Step 2:** Create a supplier invoice template
```
curl -s -X POST "http://localhost:8080/api/index.php/supplier_invoices" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": 1,
    "type": 2,
    "ref_supplier": "TEMPLATE_REF",
    "label": "Recurring Invoice Template"
  }' | jq
```

**Response:** HTTP 200 with template `id = 1`

 **Step 3:** Create a supplier invoice from the template with a custom ref
```
curl -s -X POST "http://localhost:8080/api/index.php/supplier_invoices" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1725235200",
    "fac_rec": 1,
    "ref_supplier": "my_ref",
    "socid": 1
  }' | jq
```
## Buggy Response
HTTP 200 with invoice created, but the `ref_supplier` has `_1` appended:
```
{
  "id": 2,
  "ref": "(PROV2)",
  "ref_supplier": "my_ref_1",
  ...
}
```
## Expected Response:
HTTP 200 with the exact `ref_supplier` provided:
```
{
  "id": 2,
  "ref": "(PROV2)",
  "ref_supplier": "my_ref",
  ...
}
```

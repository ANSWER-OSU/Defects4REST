# **Dolibarr 29439**
 
## Description
The issue is caused by incorrect SQL WHERE clause using LIKE which returns unintended results for query parameters leading to inconsistent API responses.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/29439
## Triggering Endpoints
*  /invoices
*  /invoices/{id}/validate
*  /documents/builddoc
*  /documents

## Triggering Behavior


### Step 1: Create First Invoice

Create an invoice that will be used to generate a document.
```
curl -s -X POST "http://localhost:8080/api/index.php/invoices" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": "1",
    "date": 1710515325,
    "type": "0",
    "lines": [
      {
        "desc": "Test product",
        "subprice": "100",
        "qty": "1"
      }
    ]
  }' | jq
```

**Response:** HTTP 200 (Invoice ID = 1)

---

### Step 2: Validate the First Invoice

Validate the invoice to trigger document generation.
```
curl -s -X POST "http://localhost:8080/api/index.php/invoices/1/validate" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" | jq
```

**Response:** HTTP 200
```
{
  "success": {
    "code": 200,
    "message": "Invoice validated"
  }
}
```

---

### Step 3: Generate Share Link for First Invoice Document

Create a share link for the generated invoice document.
```
curl -s -X POST "http://localhost:8080/api/index.php/documents/builddoc" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "modulepart": "invoice",
    "original_file": "226/FA2403-0183.pdf",
    "doctemplate": "crabe",
    "langcode": "en_US"
  }' | jq
```

**Response:** HTTP 200

### Step 4: Get Documents for First Invoice (ID=1)
```
curl -s -X GET "http://localhost:8080/api/index.php/documents?modulepart=invoice&id=1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq
```

**Expected Response:** HTTP 200
```
[
  {
    "name": "FA2403-0183.pdf",
    "path": "/var/lib/dolibarr/documents/facture/FA2403-0183",
    "level1name": "FA2403-0183",
    "relativename": "FA2403-0183.pdf",
    "fullname": "/var/lib/dolibarr/documents/facture/FA2403-0183/FA2403-0183.pdf",
    "date": 1710515325,
    "size": 67051,
    "type": "file",
    "label": "Invoice FA2403-0183",
    "entity": "1",
    "filename": "FA2403-0183.pdf",
    "filepath": "facture/FA2403-0183",
    "fullpath_orig": "",
    "description": "",
    "keywords": "",
    "cover": null,
    "position": "1",
    "gen_or_uploaded": "generated",
    "extraparams": null,
    "date_c": 1710515325,
    "date_m": 1710515325,
    "fk_user_c": "1",
    "fk_user_m": null,
    "acl": null,
    "src_object_type": "facture",
    "src_object_id": "226",
    "id": "682",
    "ref": "682",
    "share": "XXXXXXXXXXXX"
  }
]
```

### Step 5: Create Second Invoice
```
curl -s -X POST "http://localhost:8080/api/index.php/invoices" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "socid": "1",
    "date": 1713257786,
    "type": "0",
    "lines": [
      {
        "desc": "Test product 2",
        "subprice": "150",
        "qty": "1"
      }
    ]
  }' | jq
```

**Response:** HTTP 200 (Invoice ID = 2)

---

### Step 6: Validate the Second Invoice
```
curl -s -X POST "http://localhost:8080/api/index.php/invoices/2/validate" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" | jq
```

**Response:** HTTP 200
```
{
  "success": {
    "code": 200,
    "message": "Invoice validated"
  }
}
```

---

### Step 7: Get Documents for Second Invoice (ID=2) 
```
curl -s -X GET "http://localhost:8080/api/index.php/documents?modulepart=invoice&id=251" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq
```

## Buggy Response
 HTTP 200 with the body missing ECM metadata fields:
- `label`, `entity`, `filename`, `filepath`, `gen_or_uploaded`
- `src_object_type`, `src_object_id`, `id`, `ref
```
[
  {
    "name": "FA2404-0204.pdf",
    "path": "/var/lib/dolibarr/documents/facture/FA2404-0204",
    "level1name": "FA2404-0204",
    "relativename": "FA2404-0204.pdf",
    "fullname": "/var/lib/dolibarr/documents/facture/FA2404-0204/FA2404-0204.pdf",
    "date": 1713257786,
    "size": 67550,
    "type": "file"
  }
]
```

## Expected Response:
 HTTP 200 with complete metadata
```
[
  {
    "name": "FA2403-0183.pdf",
    "path": "/var/lib/dolibarr/documents/facture/FA2403-0183",
    "level1name": "FA2403-0183",
    "relativename": "FA2403-0183.pdf",
    "fullname": "/var/lib/dolibarr/documents/facture/FA2403-0183/FA2403-0183.pdf",
    "date": 1710515325,
    "size": 67051,
    "type": "file",
    "label": "Invoice FA2403-0183",
    "entity": "1",
    "filename": "FA2403-0183.pdf",
    "filepath": "facture/FA2403-0183",
    "fullpath_orig": "",
    "description": "",
    "keywords": "",
    "cover": null,
    "position": "1",
    "gen_or_uploaded": "generated",
    "extraparams": null,
    "date_c": 1710515325,
    "date_m": 1710515325,
    "fk_user_c": "1",
    "fk_user_m": null,
    "acl": null,
    "src_object_type": "facture",
    "src_object_id": "226",
    "id": "682",
    "ref": "682",
    "share": "XXXXXXXXXXXX"
  }
]
```
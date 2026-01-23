## **Dolibarr#24661**

 
### Description
The API response schema changed in version 17  contract line date fields set as null that were previously present in version 16.

### GitHub Issue URL
  https://github.com/Dolibarr/dolibarr/issues/24661
### Triggering Endpoints

 - /thirdparties 
 - /contracts 
 - /products 
 - /contracts/{id}/lines
 - /contracts/{id}

### Triggering Behavior

**Step 1.** Create a Third-Party (Company)

    curl -X POST "http://localhost:8080/api/index.php/thirdparties" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Company",
        "client": 1
      }'

**Response:** HTTP 200 OK with response 1 (Third-party ID)

**Step 2.** Create a Contract

    curl -X POST "http://localhost:8080/api/index.php/contracts" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "socid": 1,
        "ref": "TEST-CONTRACT-001",
        "date_contrat": 1682899200,
        "commercial_signature_id": 1,
        "commercial_suivi_id": 1
      }'
  
  **Response:** HTTP 200 OK with response 1 (Contract ID)


**Step 3.** Create a Product

    curl -X POST "http://localhost:8080/api/index.php/products" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "ref": "SERV001",
        "label": "Test Service",
        "type": 1
      }'

  
  **Response:** HTTP 200 OK with response 1 (Product ID)



**Step 4.** Add Contract Line with Date Fields (English Names)

    curl -X POST "http://localhost:8080/api/index.php/contracts/1/lines" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "fk_product": 1,
        "qty": 1,
        "subprice": 100,
        "date_start": 1682899200,
        "date_end": 1698537600,
        "description": "Test service with start and end dates"
      }'

  
  **Response:** HTTP 200 OK with response 1 (Line ID)

**Step 5.** Add Contract Line with Date Fields (French Names)

    curl -X POST "http://localhost:8080/api/index.php/contracts/1/lines" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "fk_product": 1,
        "qty": 1,
        "subprice": 100,
        "date_debut_prevue": 1682899200,
        "date_fin_prevue": 1698537600,
        "description": "Test with French field names"
      }'

  
  **Response:** HTTP 200 OK with response 2 (Line ID)

**Step 6.** Retrieve Contract to Observe the Bug

    curl -X GET "http://localhost:8080/api/index.php/contracts/1" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Accept: application/json"


### Buggy Response
HTTP 200 with response both  contract lines show null values for ALL date fields

    "lines": [
        {
            "id": "1",
            "date_debut_prevue": null,
            "date_debut_reel": null,
            "date_fin_prevue": null,
            "date_fin_reel": null
        },
        {
            "id": "2",
            "date_debut_prevue": null,
            "date_debut_reel": null,
            "date_fin_prevue": null,
            "date_fin_reel": null
        }
    ]

### Expected Response:
HTTP 200 with response contract lines include date fields with values:

    "lines": [
        {
            "id": "1",
            "date_start": 1682899200,
            "date_start_real": "",
            "date_end": 1698537600,
            "date_end_real": ""
        },
        {
            "id": "2",
            "date_debut_prevue": 1682899200,
            "date_fin_prevue": 1698537600
        }
    ]
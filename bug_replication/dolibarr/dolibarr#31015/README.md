# **Dolibarr 31015 **
 
## Description
The API rejects the POST request due to an invalid or missing datetime value in the payload causing a 400 Bad Request error.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/31015
## Triggering Endpoints
-   /thirdparties
-   /invoices
-   /invoices/{id}/validate
-   /invoices/{id}/payments

## Triggering Behavior

**Step 1:** Create a Third Party (Customer)


    curl -s -X POST "http://localhost:8080/api/index.php/thirdparties" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Customer Bug 31015",
        "client": 1
      }' | jq


**Response:** HTTP 200

    {
      "id": 1,
      "name": "Test Customer Bug 31015",
      "client": 1
    }

**Step 2:** Create an Invoice

    curl -s -X POST "http://localhost:8080/api/index.php/invoices" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "socid": 1,
        "date": 1726652385,
        "type": 0,
        "lines": [
          {
            "desc": "Test Line Item",
            "subprice": 100,
            "qty": 1,
            "tva_tx": 20
          }
        ]
      }' | jq

**Response:** HTTP 200

    {
      "id": 1,
      "ref": "FA2409001",
      "socid": 1,
      "total_ht": 100,
      "total_ttc": 120
    }

**Step 3:** Validate the Invoice
curl -s -X POST 

    "http://localhost:8080/api/index.php/invoices/1/validate" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" | jq


**Response:** HTTP 200

    {
      "success": {
        "code": 200,
        "message": "Invoice validated"
      }
    }


**Step 4:** Add Payment to Invoice

    curl -s -X POST "http://localhost:8080/api/index.php/invoices/1/payments" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "datepaye": 1726652385,
        "paymentid": 6,
        "closepaidinvoices": "yes",
        "accountid": 5
      }' | jq

## Buggy Response
HTTP 400

    {
      "error": {
        "code": 400,
        "message": "Bad Request: Payment error : Incorrect datetime value: '' for column `dolibarr`.`llx_paiement`.`datep` at row 1"
      },
      "debug": {
        "source": "api_invoices.class.php:1516 at call stage",
        "stages": {
          "success": ["get", "route", "negotiate", "authenticate", "validate"],
          "failure": ["call", "message"]
        }
      }
    }

## Expected Response:
HTTP 200

    {
      "success": {
        "code": 200,
        "message": "Payment recorded"
      },
      "id": 1
    }
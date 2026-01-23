## dolibarr#32111

## Description
The API rejects a valid date string input for the payment date field due to inconsistent expectations between string and timestamp formats. This bug can be trigger without Invoice ever being created.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/33949
## Triggering Endpoints
-   /invoices/{id}/payments
## **Triggering Behavior**

**Step1.** Try to set datepaye as a date string

    curl -s -X POST ""http://localhost:8080/api/index.php/invoices/$INV_ID/payments" \
      -H "DOLAPIKEY: X80SLGxbt3lQ7L5k47BOd8Fvq7Lu2nOz" -H "Content-Type: application/json" \
      -d '{
        "datepaye": "2024/11/26",
        "paymentid": '"6"',
        "closepaidinvoices": "yes",
        "accountid": '"5"'
      }'

 ## **Buggy Response:** 
 HTTP 400 Bad Request with message 

     Invalid value specified for `datepaye`. Expecting unix timestamp, such as 1765955411"

   ## **Expected Response:** 
  HTTP 404 Not Found with message
    Invoice not found

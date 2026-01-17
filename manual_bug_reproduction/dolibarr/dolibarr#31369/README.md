# **Dolibarr  31369**
 
## Description
The API ignores the provided date_solde field in the POST payload and always sets it to the current time instead of using the client-supplied value.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/31369
## Triggering Endpoints

 - /bankaccounts

## Triggering Behavior

**Step 1:** Create a bank account with a specific date_solde

    curl -s -X POST "http://localhost:8080/api/index.php/bankaccounts" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "label": "Test Bank Account Bug 31369",
        "type": "2",
        "solde": 1000,
        "date_solde": "1609459200"
      }' | jq


## Buggy Response
HTTP 200 but the `date_solde` is set to the current timestamp instead

    {
      "id": 1,
      "label": "Test Bank Account Bug 31369",
      "type": "2",
      "solde": "1000",
      "date_solde": "1735689600",
      ...
    }

## Expected Response:
HTTP 200 with the bank account created using the provided `date_solde`

    {
      "id": 1,
      "label": "Test Bank Account Bug 31369",
      "type": "2",
      "solde": "1000",
      "date_solde": "1609459200",
      ...
    }




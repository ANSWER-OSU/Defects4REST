# **Dolibarr#26066**

 
## Description
GET /multicurrencies endpoint fails to enforce proper authorization checks allowing unauthorized users to access currency data.
## GitHub Issue URL
  https://github.com/Dolibarr/dolibarr/issues/26066
## Triggering Endpoints

 - /multicurrencies

## Prerequisites
**Step 1.** Currency Configuration
Navigate to:_Setup_ _→_ _Dictionaries_ _→_ _Currencies_
Ensure the following currencies exist (add if missing):

-   EUR (Euro)
-   DKK (Danish Krone)

**Step 2.** Limited User Account Creation
Navigate to: _Users & Groups_ _→_ _New User_
Create a new user and configure permissions as follows:
Granted Permissions:
-   Products → Read
-   Categories/Tags → Read

Denied Permissions:

-   Multicurrency → NO PERMISSIONS

## Triggering Behavior

**Step 1.** Test List All Currencies

    curl -i \
      -H "Accept: application/json" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      "http://localhost:8080/api/index.php/multicurrencies?sortfield=t.rowid&sortorder=ASC&limit=100"


## Buggy Response
HTTP 200 with response

     {
            "id": "1",
            "code": "EUR",
            "name": "Euros (€)",
            "rate": {
                "id": "1",
                "rate": "1",
                "date_sync": 1767143996
            }
        }

## Expected Response:
HTTP  403 with response

    {
      "error": {
        "code": 403,
        "message": "Unauthorized: Insufficient rights to read currencies"
      }
    }
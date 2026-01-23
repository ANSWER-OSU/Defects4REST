# **Dolibarr#29292**

 
## Description
The issue is caused by the colon character in the sqlfilters query parameter leading to incorrect or unexpected search results.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/29292

## Triggering Endpoints

 - /orders

## Triggering Behavior

**Step 1.** Create order with client ref "a:b"

    curl -s -X POST "http://localhost:8080/api/index.php/orders" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "socid": 1,
        "ref_client": "a:b"
      }' | jq

**Response:** HTTP 200 with order ID 1

**Step 2:** Create order with client ref "LAvionJaune"

    curl -s -X POST "http://localhost:8080/api/index.php/orders" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "socid": 1,
        "ref_client": "LAvionJaune"
      }' | jq

**Response:** HTTP 200 with order ID  2

**Step 3:** Search for orders using sqlfilters with colon in the value

    curl -s -X GET "http://localhost:8080/api/index.php/orders?sortfield=t.rowid&sortorder=ASC&limit=100&sqlfilters=t.ref_client%3A%3D%3A'a%3Ab'" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq


## Buggy Response
HTTP 200 with incorrect results - returns orders with client refs: `"LAvionJaune"` (all orders EXCEPT the one with `"a:b"`)


## Expected Response:
HTTP 200 with only one order returned - the order with `ref_client = "a:b"`

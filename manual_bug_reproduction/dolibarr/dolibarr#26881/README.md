# **Dolibarr#26881**

 
## Description
The API endpoint is misconfigured in the code causing the setlevelprice operation to fail due to incorrect URL mapping.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/26881
## Triggering Endpoints

 - /thirdparties/{id}/setpricelevel
 - /thirdparties

## Triggering Behavior

**Step 1.** Create a Third Party

    curl -s -X POST "http://localhost:8080/api/index.php/thirdparties" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Company",
        "client": 1
      }' | jq

**Response:** HTTP 200  with body

    {
      "id": 1,
      "name": "Test Company",
      "client": 1,
      "price_level": null
    }

**Step 2:** Attempt to Set Price Level

    curl -s -X PUT "http://localhost:8080/api/index.php/thirdparties/1/setpricelevel/2" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" | jq



## Buggy Response
HTTP 404 with body 

    {
      "error": {
        "code": "404",
        "message": "Endpoint not found"
      }
    }

## Expected Response:
HTTP  200 with body

    {
      "success": {
        "code": "200",
        "message": "Price level updated successfully"
      }
    }


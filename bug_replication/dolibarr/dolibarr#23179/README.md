# dolibarr#23179

## Description
The /products/{id} REST API does not update the note_public and note_private fields indicating a failure to process or validate the payload for these properties.

## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/23179

## Triggering Endpoints

-   /products
    
-   /products/{id}
   
## **Triggering Behavior**
**Step 1.** Create a product

    curl -s -X POST "http://localhost:8080/api/index.php/products" \
      -H "DOLAPIKEY: X80SLGxbt3lQ7L5k47BOd8Fvq7Lu2nOz" -H "Content-Type: application/json" \
      -d '{
        "ref": "BUG-23179-TEST",
        "label": "Bug 23179 test product"
      }' | jq

**Response:** HTTP 200 with e.g. id = 1:

**Step 2.** Try to update notes with product id =1 from step 1

   

     curl -s -X PUT "http://localhost:8080/api/index.php/products/1" \
          -H "DOLAPIKEY: X80SLGxbt3lQ7L5k47BOd8Fvq7Lu2nOz" -H "Content-Type: application/json" \
          -d '{
            "label": "Bug 23179 test product UPDATED",
            "note_public": "public NEW",
            "note_private": "private NEW"
          }' | jq


 ## **Buggy Response:** 
 HTTP 200 and the JSON still contains:

    "note_public": null,
    "note_private": null
   ## **Expected Response:** 
   HTTP 200 with the new values applied:

    "note_public": "public NEW",
    "note_private": "private NEW"

 


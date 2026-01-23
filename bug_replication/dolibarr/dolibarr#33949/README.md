## dolibarr#33949

## Description
The API accepts a PUT request to update the extrafield's default value but fails to persist or return the updated value indicating a payload handling or schema update issue.

## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/33949
## Triggering Endpoints
-   setup/extrafields/projet/call_to_action   
## **Triggering Behavior**

**Step1.** Create the extrafield

    curl -s -X POST "$BASE/setup/extrafields/projet/call_to_action" \
      -H "DOLAPIKEY: $APIKEY" -H "Content-Type: application/json" \
      -d '{
        "type": "varchar",
        "label": "Call_to_action",
        "size": "26",
        "default": null,
        "unique": "0",
        "required": "0",
        "pos": "160",
        "alwayseditable": "0",
        "list": "1",
        "printable": "0",
        "totalizable": "0"
      }'  
 **Response:** HTTP 200  
**Step 2.** Update the extrafield default using PUT 

    curl -s -X PUT "$BASE/setup/extrafields/projet/call_to_action" \
      -H "DOLAPIKEY: $APIKEY" -H "Content-Type: application/json" \
      -d '{
        "type": "varchar",
        "label": "Call_to_action",
        "size": "26",
        "default": "Begin Registration",
        "unique": "0",
        "required": "0",
        "pos": "160",
        "alwayseditable": "0",
        "list": "1",
        "printable": "0",
        "totalizable": "0"
      }'
      
    

 ## **Buggy Response:** 
 HTTP 200 and the JSON still contains default remains null after the PUT.

     {
      "projet": {
        "call_to_action": {
          "id": "3",
          "type": "varchar",
          "label": "Call_to_action",
          "size": "26",
          "elementtype": "projet",
          "default": null,
          "computed": null,
          "unique": "0",
          "required": "0",
          "param": "",
          "pos": "160",
          "alwayseditable": "0",
          "perms": null,
          "list": "1",
          "printable": "0",
          "totalizable": "0",
          "langs": null,
          "help": null,
          "css": null,
          "cssview": null,
          "csslist": null,
          "fk_user_author": "1",
          "fk_user_modif": "1",
          "datec": "2025-12-17 06:16:07",
          "tms": "2025-12-17 06:16:07"
        }
      }
    } 

   ## **Expected Response:** 
HTTP 200 and the JSON default should be updated to "Begin Registration"

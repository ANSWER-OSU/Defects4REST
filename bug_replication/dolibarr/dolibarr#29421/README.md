# **Dolibarr#29421**

 
## Description
The GET /members/types/{id} endpoint incorrectly returns a deletion message in its payload which is a schema and response validation issue for a GET API.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/29421

## Triggering Endpoints

 - /members/types/{id}

## Triggering Behavior

**Step 1.** Retrieve a non-existent member type

    curl -s -X GET "http://localhost:8080/api/index.php/members/types/89327434" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" | jq


## Buggy Response
HTTP 200 with body 

    {
      "success": {
        "code": 200,
        "message": "Member type deleted"
      }
    }

## Expected Response:
HTTP 404 with body
```
{
  "error": {
    "code": 404,
    "message": "Not Found: member type not found"
  },
  "debug": {
    "source": "api_members.class.php:649 at call stage",
    "stages": {
      "success": [
        "get",
        "route",
        "negotiate",
        "authenticate",
        "validate"
      ],
      "failure": [
        "call",
        "message"
      ]
    }
  }
}
```

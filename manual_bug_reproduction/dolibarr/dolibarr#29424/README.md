# **Dolibarr 29424**
 
## Description
API does not return an error when querying member categories for a non-existing member id leading to incorrect handling of query parameters.
## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/29424
## Triggering Endpoints

-  /categories
-   /members
-  /members/{id}/categories/{category_id} 
- /members/{id}/categories

## Triggering Behavior

**Step 1: Create Member Categories**
```
curl -s -X POST "http://localhost:8080/api/index.php/categories" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "Premium Members",
    "type": 3
  }' | jq
```
**Response**: HTTP 200
```
{
  "id": 1
}
```
**Step 2: Create a Valid Member**
```
curl -s -X POST "http://localhost:8080/api/index.php/members" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" \
  -d '{
    "morphy": "phy",
    "lastname": "Doe",
    "firstname": "John",
    "email": "john.doe@example.com"
  }' | jq
```
**Response**: HTTP 200
```
{
  "id": 1
}
```
**Step 3: Assign Member to Category**
```
curl -s -X POST "http://localhost:8080/api/index.php/members/1/categories/1" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
  -H "Content-Type: application/json" | jq
```
**Response**: HTTP 200
```
{
  "success": {
    "code": 200,
    "message": "Category linked to member"
  }
}
```
**Step 4: Attempt to GET categories for VALID member (baseline)**
```
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X GET "http://localhost:8080/api/index.php/members/1/categories" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq
```
**Expected Response**: HTTP 200
```
[
  {
    "id": "1",
    "label": "Premium Members",
    "type": "3",
    ...
  }
]
HTTP Status: 200
```
**Step 5: Attempt to GET categories for NON-EXISTING member **
```
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X GET "http://localhost:8080/api/index.php/members/99999/categories" \
  -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" | jq
```
## Buggy Response:
 HTTP 200 with body 
```
[]
HTTP Status: 200
```

## Expected Correct Response:
 HTTP 404 with
```
{
  "error": {
    "code": 404,
    "message": "Member does not exist"
  }
}
HTTP Status: 404
```
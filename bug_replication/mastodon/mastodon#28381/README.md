# **mastodon#28381**

 
## Description
The API returns a 500 error due to an ambiguous column in the SQL ORDER BY clause triggered by specific query parameters.
## GitHub Issue URL
https://github.com/mastodon/mastodon/issues/28381
## Triggering Endpoints

 - /api/v1/directory

## Triggering Behavior

**Step 1.** Access the Directory API Endpoint

    curl -v "http://localhost:3000/api/v1/directory?order=active&local=false&limit=20"


## Buggy Response
500 Internal Server Error

## Expected Response:
HTTP 200 with body `[]`
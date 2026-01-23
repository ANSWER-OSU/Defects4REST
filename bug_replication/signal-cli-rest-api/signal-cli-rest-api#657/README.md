# signal-cli-rest-api 657

  

## Description

  
 Group description is missing from API responses only in the Docker container environment despite being present in the official documentation.
  

## GitHub Issue URL

https://github.com/bbernhard/signal-cli-rest-api/issues/657
  

## Triggering Endpoint:

* /v1/groups/{number}


## Triggering Behavior:

 
**Step 1.** 

    curl -X GET 'http://localhost:8028/v1/groups/+5422244756' \
      -H 'Content-Type: application/json'

## Buggy Response
http 200 with body 

    [
      {
        "id": "Pmpi+EfPWmsxiomLe9Nx2XF9HOE483p6iKiFj65iMwI=",
        "name": "test Group",
        "internal_id": "group.abc123",
        "members": ["+5422244756"],
        "blocked": false,
        "pending_invites": [],
        "pending_requests": [],
        "invite_link": "https://signal.group/#CjQKIAtcbUw...",
        "admins": ["+5422244756"]
      }
    ]


## Expected Response:
HTTP 200 with body

    {
      "id": "Pmpi+EfPWmsxiomLe9Nx2XF9HOE483p6iKiFj65iMwI=",
      "name": "test Group",
      "description": "It is a teest group to test api.",
      "internal_id": "group.abc123",
      "members": ["+5422244756"],
      "blocked": false,
      "pending_invites": [],
      "pending_requests": [],
      "invite_link": "https://signal.group/#CjQKIAtcbUw...",
      "admins": ["+5422244756"],
      "member_details": [
        {
          "number": "+5422244756",
        }
      ]
    }


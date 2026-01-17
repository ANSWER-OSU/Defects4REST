# **mastodon#29071**

 
## Description
The API returns Suggestion.source as an array of strings instead of the documented string type causing schema decoding failures for clients.
## GitHub Issue URL
https://github.com/mastodon/mastodon/issues/29071
## Triggering Endpoints


## Triggering Behavior

**Step 1.** Access the Directory API Endpoint

    curl -H "Authorization: Bearer A21ixXRH8IHatJh1yZm6MuKFgnwYumAD6FuMOFH3BRM" \
         http://localhost:3000/api/v2/suggestions | jq '.'
         



## Buggy Response
http 200 with body 

     "source": [
          "most_followed"
        ],
        "account": {
          "id": "115857295330248208",
          "username": "alice",
          "acct": "alice",
          "display_name": "",
          "locked": false,
          "bot": false,
          "discoverable": true,
          "indexable": false,
          "group": false,
          "created_at": "2026-01-08T00:00:00.000Z",
          "note": "",
          "url": "https://localhost/@alice",
          "uri": "https://localhost/users/alice",
          "avatar": "https://localhost/avatars/original/missing.png",
          "avatar_static": "https://localhost/avatars/original/missing.png",
          "header": "https://localhost/headers/original/missing.png",
          "header_static": "https://localhost/headers/original/missing.png",
          "followers_count": 5,
          "following_count": 0,
          "statuses_count": 3,
          "last_status_at": "2026-01-08",
          "hide_collections": null,
          "noindex": false,
          "emojis": [],
          "roles": [
            {
              "id": "2",
              "name": "Admin",
              "color": ""
            }
          ],
          "fields": []
        }


`source` is an array
## Expected Response:
HTTP 200 with body 

    {
        "source": "global",
        "sources": [
          "most_followed"
        ],
        "account": {
          "id": "115857754488540270",
          "username": "alice",
          "acct": "alice",
          "display_name": "",
          "locked": false,
          "bot": false,
          "discoverable": true,
          "indexable": false,
          "group": false,
          "created_at": "2026-01-08T00:00:00.000Z",
          "note": "",
          "url": "https://localhost/@alice",
          "uri": "https://localhost/users/alice",
          "avatar": "https://localhost/avatars/original/missing.png",
          "avatar_static": "https://localhost/avatars/original/missing.png",
          "header": "https://localhost/headers/original/missing.png",
          "header_static": "https://localhost/headers/original/missing.png",
          "followers_count": 5,
          "following_count": 0,
          "statuses_count": 3,
          "last_status_at": "2026-01-08",
          "hide_collections": null,
          "noindex": false,
          "emojis": [],
          "roles": [
            {
              "id": "2",
              "name": "Admin",
              "color": ""
            }
          ],
          "fields": []
        }
      },
`source` is an string

# **mastodon#33357**

 
## Description
The API returns incorrect last usage dates for featured hashtags only when querying remote users, indicating the defect is specific to cross-instance or federated environment behavior.

## GitHub Issue URL
https://github.com/mastodon/mastodon/issues/33357
## Triggering Endpoints

 - /api/v1/directory
 - /api/v1/accounts/[id]/featured_hashtags

## Triggering Behavior

**Step 1.** Find a remote user ID who has featured hashtags
```
curl -H "Authorization: Bearer Kb_mvxDp-nWPvhtCB3zN8WJ9GXVJqwAca43Zf27xcAM" \
  "http://localhost:3000/api/v1/directory?local=false&limit=5"
```

**Response:**
HTTP 200 with body 
```
[
  {
    "id": "109281825849025262",
    "username": "remoteuser",
    "acct": "remoteuser@mastodon.online",
    "display_name": "Remote User",
    "locked": false,
    "bot": false,
    "discoverable": true,
    "group": false,
    "created_at": "2022-11-01T00:00:00.000Z",
    "note": "Remote user profile",
    "url": "https://mastodon.online/@remoteuser",
    "avatar": "https://mastodon.online/avatars/original/missing.png",
    "avatar_static": "https://mastodon.online/avatars/original/missing.png",
    "header": "https://mastodon.online/headers/original/missing.png",
    "header_static": "https://mastodon.online/headers/original/missing.png",
    "followers_count": 150,
    "following_count": 200,
    "statuses_count": 500,
    "last_status_at": "2025-01-09"
  }
]
```

**Step 2.** Get the featured hashtags for that remote user
```
curl -H "Authorization: Bearer Kb_mvxDp-nWPvhtCB3zN8WJ9GXVJqwAca43Zf27xcAM" \
  "http://localhost:3000/api/v1/accounts/109281825849025262/featured_tags"
```

## Buggy Response:
```
[
  {
    "id": "12345",
    "name": "swiftui",
    "url": "https://mastodon.online/@remoteuser/tagged/swiftui",
    "statuses_count": 50,
    "last_status_at": "2025-12-30"
  },
  {
    "id": "12346",
    "name": "pixelart",
    "url": "https://mastodon.online/@remoteuser/tagged/pixelart",
    "statuses_count": 233,
    "last_status_at": "2025-12-31"
  }
]
```

## Expected Response:**
```
[
  {
    "id": "12345",
    "name": "swiftui",
    "url": "https://mastodon.online/@remoteuser/tagged/swiftui",
    "statuses_count": 150,
    "last_status_at": "2026-01-09"
  },
  {
    "id": "12346",
    "name": "pixelart",
    "url": "https://mastodon.online/@remoteuser/tagged/pixelart",
    "statuses_count": 1000,
    "last_status_at": "2026-01-08"
  }
]
```

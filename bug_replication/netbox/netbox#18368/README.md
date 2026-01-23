## **NetBox#18368**

 
### Description

The API does not allow creation or retrieval of tags on MAC addresses while the web UI does indicating a mismatch in supported fields or schema between UI and API.

### GitHub Issue URL

[https://github.com/netbox-community/netbox/issues/18368](https://github.com/netbox-community/netbox/issues/18368)

  

### Triggering Endpoints

-  /api/dcim/mac-addresses/

### Triggering Behavior

**Step 1.** Get the MAC address:

    curl -X GET "http://localhost:8080/api/dcim/mac-addresses/" \
    -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567"

### Buggy Response:
HTTP 200 OK

    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 1,
          "url": "http://localhost:8080/api/dcim/mac-addresses/1/",
          "display_url": "http://localhost:8080/dcim/mac-addresses/1/",
          "display": "00:11:22:33:44:55",
          "mac_address": "00:11:22:33:44:55",
          "assigned_object_type": null,
          "assigned_object": null,
          "description": "",
          "comments": ""
        }
      ]
    }

### Buggy Response:
HTTP 200 

    {
          "count": 1,
          "next": null,
          "previous": null,
          "results": [
            {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/mac-addresses/1/",
              "display_url": "http://localhost:8080/dcim/mac-addresses/1/",
              "display": "00:11:22:33:44:55",
              "mac_address": "00:11:22:33:44:55",
              "assigned_object_type": null,
              "assigned_object_id": null,
              "assigned_object": null,
              "description": "",
              "comments": "",
              "tags": [],
              "custom_fields": {},
              "created": "2025-12-27T00:41:20.090031Z",
              "last_updated": "2025-12-27T00:41:20.090041Z"
            }
          ]
        }

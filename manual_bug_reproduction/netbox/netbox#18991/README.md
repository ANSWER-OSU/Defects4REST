## **netBox#18991**

 
### Description
An AttributeError is raised in the REST API when accessing the paths endpoint for ports indicating a runtime issue introduced by a recent code change.

### GitHub Issue URL
https://github.com/netbox-community/netbox/issues/18991
  
### Triggering Endpoints

 - /api/dcim/rear-ports/{id}/paths/

### Triggering Behavior

**Step 1.** Query Cable Paths

       curl -X GET \
      "http://localhost:8080/api/dcim/rear-ports/1/paths/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Accept: application/json"

### Buggy Response:
HTTP 500 with response 

```
'NoneType' object has no attribute 'model'
```

### Expected Response:
HTTP 200 with response

    [
      {
        "id": 1,
        "path": [
          [
            {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/interfaces/1/",
              "display": "eth0",
              "device": {
                "id": 2,
                "url": "http://localhost:8080/api/dcim/devices/2/",
                "display": "switch-01",
                "name": "switch-01",
                "description": ""
              },
              "name": "eth0",
              "description": "",
              "cable": {
                "id": 1,
                "url": "http://localhost:8080/api/dcim/cables/1/",
                "display": "#1",
                "label": "",
                "description": ""
              },
              "_occupied": true
            }
          ],
          [
            {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/cables/1/",
              "display": "#1",
              "label": "",
              "description": ""
            }
          ],
          [
            {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/front-ports/1/",
              "display": "Front Port 1",
              "device": {
                "id": 1,
                "url": "http://localhost:8080/api/dcim/devices/1/",
                "display": "patch-panel-01",
                "name": "patch-panel-01",
                "description": ""
              },
              "name": "Front Port 1",
              "description": "",
              "cable": {
                "id": 1,
                "url": "http://localhost:8080/api/dcim/cables/1/",
                "display": "#1",
                "label": "",
                "description": ""
              },
              "_occupied": true
            }
          ],
          [
            {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/rear-ports/1/",
              "display": "Rear Port 1",
              "device": {
                "id": 1,
                "url": "http://localhost:8080/api/dcim/devices/1/",
                "display": "patch-panel-01",
                "name": "patch-panel-01",
                "description": ""
              },
              "name": "Rear Port 1",
              "description": "",
              "cable": null,
              "_occupied": false
            }
          ]
        ],
        "is_active": true,
        "is_complete": false,
        "is_split": false
      }
    ]
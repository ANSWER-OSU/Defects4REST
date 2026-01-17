## **NetBox#18585**

 
### Description

Filtering circuits by location_id parameter returns all circuits instead of only the attached ones.

### GitHub Issue URL

https://github.com/netbox-community/netbox/issues/18585
  

### Triggering Endpoints

-   /api/dcim/sites/
-   /api/dcim/locations/
-   /api/circuits/providers/
-   /api/circuits/circuit-types/
-   api/circuits/circuits/
-   /api/circuits/circuit-terminations/


### Triggering Behavior

**Step 1.** Create a site

    curl -X POST \
      "http://localhost:8080/api/dcim/sites/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Site",
        "slug": "test-site"
      }'
**Response:** HTTP 200

    {
      "id": 1,
      "url": "http://localhost:8080/api/dcim/sites/1/",
      "display": "Test Site",
      "name": "Test Site",
      "slug": "test-site",
      "status": {"value": "active", "label": "Active"},
      "created": "2025-12-27T02:11:53.677653Z",
      "last_updated": "2025-12-27T02:11:53.677663Z"
    }
   
**Step 2.** Create a location using step 1 id = 1

    curl -X POST \
      "http://localhost:8080/api/dcim/locations/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Building",
        "slug": "test-building",
        "site": 1
      }'

**Response:** HTTP 200

    {
      "id": 1,
      "url": "http://localhost:8080/api/dcim/locations/1/",
      "display": "Test Building",
      "name": "Test Building",
      "slug": "test-building",
      "site": {
        "id": 1,
        "display": "Test Site",
        "name": "Test Site",
        "slug": "test-site"
      },
      "status": {"value": "active", "label": "Active"},
      "created": "2025-12-27T02:11:59.017929Z",
      "last_updated": "2025-12-27T02:11:59.017939Z"
    }

**Step 3.** Create a provider

    curl -X POST \
      "http://localhost:8080/api/circuits/providers/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Provider",
        "slug": "test-provider"
      }'
     
   **Response**: HTTP 200

       {
      "id": 1,
      "url": "http://localhost:8080/api/circuits/providers/1/",
      "display": "Test Provider",
      "name": "Test Provider",
      "slug": "test-provider",
      "created": "2025-12-27T02:12:03.625255Z",
      "last_updated": "2025-12-27T02:12:03.625265Z"
    }

**Step 4.** Create a circuit type

    curl -X POST \
      "http://localhost:8080/api/circuits/circuit-types/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Type",
        "slug": "test-type"
      }'

**Response:** HTTP 200

    {
      "id": 1,
      "url": "http://localhost:8080/api/circuits/circuit-types/1/",
      "display": "Test Type",
      "name": "Test Type",
      "slug": "test-type",
      "created": "2025-12-27T02:12:08.802082Z",
      "last_updated": "2025-12-27T02:12:08.802092Z"
    }

**Step 5.** Create first circuit

    curl -X POST \
      "http://localhost:8080/api/circuits/circuits/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "cid": "CIRCUIT-WITH-LOCATION",
        "provider": 1,
        "type": 1
      }'
**Response:** HTTP 200

    {
      "id": 1,
      "url": "http://localhost:8080/api/circuits/circuits/1/",
      "display": "CIRCUIT-WITH-LOCATION",
      "cid": "CIRCUIT-WITH-LOCATION",
      "provider": {
        "id": 1,
        "display": "Test Provider",
        "name": "Test Provider",
        "slug": "test-provider"
      },
      "type": {
        "id": 1,
        "display": "Test Type",
        "name": "Test Type",
        "slug": "test-type"
      },
      "status": {"value": "active", "label": "Active"},
      "termination_a": null,
      "termination_z": null,
      "created": "2025-12-27T02:12:13.453118Z",
      "last_updated": "2025-12-27T02:12:13.453127Z"
    }


**Step 6.** Add circuit termination with location

    curl -X POST \
      "http://localhost:8080/api/circuits/circuit-terminations/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "circuit": 1,
        "term_side": "A",
        "termination_type": "dcim.location",
        "termination_id": 1
      }'

**Response:** HTTP 200

    {
      "id": 1,
      "url": "http://localhost:8080/api/circuits/circuit-terminations/1/",
      "display": "CIRCUIT-WITH-LOCATION: Termination A",
      "circuit": {
        "id": 1,
        "display": "CIRCUIT-WITH-LOCATION",
        "cid": "CIRCUIT-WITH-LOCATION"
      },
      "term_side": "A",
      "termination_type": "dcim.location",
      "termination_id": 1,
      "termination": {
        "id": 1,
        "display": "Test Building",
        "name": "Test Building"
      },
      "created": "2025-12-27T02:25:00.000000Z",
      "last_updated": "2025-12-27T02:25:00.000000Z"
    }

**Step 7.** Create second circuit WITHOUT location 

    curl -X POST \
      "http://localhost:8080/api/circuits/circuits/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "cid": "CIRCUIT-NO-LOCATION",
        "provider": 1,
        "type": 1
      }'

**Response:** HTTP 200

    {
      "id": 2,
      "url": "http://localhost:8080/api/circuits/circuits/2/",
      "display": "CIRCUIT-NO-LOCATION",
      "cid": "CIRCUIT-NO-LOCATION",
      "provider": {
        "id": 1,
        "display": "Test Provider",
        "name": "Test Provider",
        "slug": "test-provider"
      },
      "type": {
        "id": 1,
        "display": "Test Type",
        "name": "Test Type",
        "slug": "test-type"
      },
      "status": {"value": "active", "label": "Active"},
      "termination_a": null,
      "termination_z": null,
      "created": "2025-12-27T02:12:26.902797Z",
      "last_updated": "2025-12-27T02:12:26.902807Z"
    }
   
 **Step 8.** Filter circuits by location_id=1  

    curl -X GET \
      "http://localhost:8080/api/circuits/circuits/?location_id=1" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json"




### Buggy Response:
HTTP 200 OK Both circuits are returned! The filter is completely ignored.

    {
      "count": 2,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 2,
          "url": "http://localhost:8080/api/circuits/circuits/2/",
          "display_url": "http://localhost:8080/circuits/circuits/2/",
          "display": "CIRCUIT-NO-LOCATION",
          "cid": "CIRCUIT-NO-LOCATION",
          "provider": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/providers/1/",
            "display": "Test Provider",
            "name": "Test Provider",
            "slug": "test-provider",
            "description": ""
          },
          "provider_account": null,
          "type": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/circuit-types/1/",
            "display": "Test Type",
            "name": "Test Type",
            "slug": "test-type",
            "description": ""
          },
          "status": {
            "value": "active",
            "label": "Active"
          },
          "tenant": null,
          "install_date": null,
          "termination_date": null,
          "commit_rate": null,
          "description": "",
          "distance": null,
          "distance_unit": null,
          "termination_a": null,
          "termination_z": null,
          "comments": "",
          "tags": [],
          "custom_fields": {},
          "created": "2025-12-27T03:48:56.967171Z",
          "last_updated": "2025-12-27T03:48:56.967183Z"
        },
        {
          "id": 1,
          "url": "http://localhost:8080/api/circuits/circuits/1/",
          "display_url": "http://localhost:8080/circuits/circuits/1/",
          "display": "CIRCUIT-WITH-LOCATION",
          "cid": "CIRCUIT-WITH-LOCATION",
          "provider": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/providers/1/",
            "display": "Test Provider",
            "name": "Test Provider",
            "slug": "test-provider",
            "description": ""
          },
          "provider_account": null,
          "type": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/circuit-types/1/",
            "display": "Test Type",
            "name": "Test Type",
            "slug": "test-type",
            "description": ""
          },
          "status": {
            "value": "active",
            "label": "Active"
          },
          "tenant": null,
          "install_date": null,
          "termination_date": null,
          "commit_rate": null,
          "description": "",
          "distance": null,
          "distance_unit": null,
          "termination_a": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/circuit-terminations/1/",
            "display_url": "http://localhost:8080/circuits/circuit-terminations/1/",
            "display": "CIRCUIT-WITH-LOCATION: Termination A",
            "termination_type": "dcim.location",
            "termination_id": 1,
            "termination": {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/locations/1/",
              "display": "Test Building",
              "name": "Test Building",
              "slug": "test-building",
              "description": "",
              "rack_count": 0,
              "_depth": 0
            },
            "port_speed": null,
            "upstream_speed": null,
            "xconnect_id": "",
            "description": ""
          },
          "termination_z": null,
          "comments": "",
          "tags": [],
          "custom_fields": {},
          "created": "2025-12-27T03:48:38.528733Z",
          "last_updated": "2025-12-27T03:48:48.247512Z"
        }
      ]
    }

   

### Expected Response:
HTTP 200 OK with only one circuit. 

    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 1,
          "url": "http://localhost:8080/api/circuits/circuits/1/",
          "display_url": "http://localhost:8080/circuits/circuits/1/",
          "display": "CIRCUIT-WITH-LOCATION",
          "cid": "CIRCUIT-WITH-LOCATION",
          "provider": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/providers/1/",
            "display": "Test Provider",
            "name": "Test Provider",
            "slug": "test-provider",
            "description": ""
          },
          "provider_account": null,
          "type": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/circuit-types/1/",
            "display": "Test Type",
            "name": "Test Type",
            "slug": "test-type",
            "description": ""
          },
          "status": {
            "value": "active",
            "label": "Active"
          },
          "tenant": null,
          "install_date": null,
          "termination_date": null,
          "commit_rate": null,
          "description": "",
          "distance": null,
          "distance_unit": null,
          "termination_a": {
            "id": 1,
            "url": "http://localhost:8080/api/circuits/circuit-terminations/1/",
            "display_url": "http://localhost:8080/circuits/circuit-terminations/1/",
            "display": "CIRCUIT-WITH-LOCATION: Termination A",
            "termination_type": "dcim.location",
            "termination_id": 1,
            "termination": {
              "id": 1,
              "url": "http://localhost:8080/api/dcim/locations/1/",
              "display": "Test Building",
              "name": "Test Building",
              "slug": "test-building",
              "description": "",
              "rack_count": 0,
              "_depth": 0
            },
            "port_speed": null,
            "upstream_speed": null,
            "xconnect_id": "",
            "description": ""
          },
          "termination_z": null,
          "comments": "",
          "tags": [],
          "custom_fields": {},
          "created": "2025-12-27T03:52:37.838679Z",
          "last_updated": "2025-12-27T03:52:44.007115Z"
        }
      ]
    }




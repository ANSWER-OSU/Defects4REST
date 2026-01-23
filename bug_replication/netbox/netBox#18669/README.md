## **NetBox#18669**

 
### Description
When the custom_fields section is present in the POST body the API ignores default values for unspecified custom fields leading to incorrect payload handling.

### GitHub Issue URL

https://github.com/netbox-community/netbox/issues/18669
  
### Triggering Endpoints

 - /api/extras/custom-fields/ 
 - /api/ipam/prefixes/

### Triggering Behavior

**Step 1.** Create primary_subnet custom field

    curl -X POST http://localhost:8080/api/extras/custom-fields/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "primary_subnet",
        "object_types": ["ipam.prefix"],
        "type": "boolean",
        "required": true,
        "default": true
      }'

**Response:** HTTP 201  

    {
      "id": 1,
      "url": "http://localhost:8080/api/extras/custom-fields/1/",
      "display_url": "http://localhost:8080/extras/custom-fields/1/",
      "display": "Primary subnet",
      "object_types": [
        "ipam.prefix"
      ],
      "type": {
        "value": "boolean",
        "label": "Boolean (true/false)"
      },
      "related_object_type": null,
      "data_type": "boolean",
      "name": "primary_subnet",
      "label": "",
      "group_name": "",
      "description": "",
      "required": true,
      "unique": false,
      "search_weight": 1000,
      "filter_logic": {
        "value": "loose",
        "label": "Loose"
      },
      "ui_visible": {
        "value": "always",
        "label": "Always"
      },
      "ui_editable": {
        "value": "yes",
        "label": "Yes"
      },
      "is_cloneable": false,
      "default": true,
      "related_object_filter": null,
      "weight": 100,
      "validation_minimum": null,
      "validation_maximum": null,
      "validation_regex": "",
      "choice_set": null,
      "comments": "",
      "created": "2025-12-28T02:29:44.400139Z",
      "last_updated": "2025-12-28T02:29:44.400151Z"
    }
**Step 2.** Create ripe_admin custom field

    curl -X POST http://localhost:8080/api/extras/custom-fields/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "ripe_admin",
        "object_types": ["ipam.prefix"],
        "type": "text",
        "required": false,
        "default": "xxx-RIPE"
      }'

**Response:** HTTP 201

    {
      "id": 2,
      "url": "http://localhost:8080/api/extras/custom-fields/2/",
      "display_url": "http://localhost:8080/extras/custom-fields/2/",
      "display": "Ripe admin",
      "object_types": [
        "ipam.prefix"
      ],
      "type": {
        "value": "text",
        "label": "Text"
      },
      "related_object_type": null,
      "data_type": "string",
      "name": "ripe_admin",
      "label": "",
      "group_name": "",
      "description": "",
      "required": false,
      "unique": false,
      "search_weight": 1000,
      "filter_logic": {
        "value": "loose",
        "label": "Loose"
      },
      "ui_visible": {
        "value": "always",
        "label": "Always"
      },
      "ui_editable": {
        "value": "yes",
        "label": "Yes"
      },
      "is_cloneable": false,
      "default": "xxx-RIPE",
      "related_object_filter": null,
      "weight": 100,
      "validation_minimum": null,
      "validation_maximum": null,
      "validation_regex": "",
      "choice_set": null,
      "comments": "",
      "created": "2025-12-28T02:29:52.258279Z",
      "last_updated": "2025-12-28T02:29:52.258289Z"
    }

**Step 3.** Create ripe_tech custom field

    curl -X POST http://localhost:8080/api/extras/custom-fields/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "ripe_tech",
        "object_types": ["ipam.prefix"],
        "type": "text",
        "required": false
      }'

     
   **Response**: HTTP 201

         {
      "id": 3,
      "url": "http://localhost:8080/api/extras/custom-fields/3/",
      "display_url": "http://localhost:8080/extras/custom-fields/3/",
      "display": "Ripe tech",
      "object_types": [
        "ipam.prefix"
      ],
      "type": {
        "value": "text",
        "label": "Text"
      },
      "related_object_type": null,
      "data_type": "string",
      "name": "ripe_tech",
      "label": "",
      "group_name": "",
      "description": "",
      "required": false,
      "unique": false,
      "search_weight": 1000,
      "filter_logic": {
        "value": "loose",
        "label": "Loose"
      },
      "ui_visible": {
        "value": "always",
        "label": "Always"
      },
      "ui_editable": {
        "value": "yes",
        "label": "Yes"
      },
      "is_cloneable": false,
      "default": null,
      "related_object_filter": null,
      "weight": 100,
      "validation_minimum": null,
      "validation_maximum": null,
      "validation_regex": "",
      "choice_set": null,
      "comments": "",
      "created": "2025-12-28T02:29:58.541156Z",
      "last_updated": "2025-12-28T02:29:58.541166Z"
    }

**Step 4.** Create ripe_netname custom field

    curl -X POST http://localhost:8080/api/extras/custom-fields/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "ripe_netname",
        "object_types": ["ipam.prefix"],
        "type": "text",
        "required": false
      }'

  

**Response:** HTTP 201

    {
      "id": 4,
      "url": "http://localhost:8080/api/extras/custom-fields/4/",
      "display_url": "http://localhost:8080/extras/custom-fields/4/",
      "display": "Ripe netname",
      "object_types": [
        "ipam.prefix"
      ],
      "type": {
        "value": "text",
        "label": "Text"
      },
      "related_object_type": null,
      "data_type": "string",
      "name": "ripe_netname",
      "label": "",
      "group_name": "",
      "description": "",
      "required": false,
      "unique": false,
      "search_weight": 1000,
      "filter_logic": {
        "value": "loose",
        "label": "Loose"
      },
      "ui_visible": {
        "value": "always",
        "label": "Always"
      },
      "ui_editable": {
        "value": "yes",
        "label": "Yes"
      },
      "is_cloneable": false,
      "default": null,
      "related_object_filter": null,
      "weight": 100,
      "validation_minimum": null,
      "validation_maximum": null,
      "validation_regex": "",
      "choice_set": null,
      "comments": "",
      "created": "2025-12-28T02:30:06.277864Z",
      "last_updated": "2025-12-28T02:30:06.277875Z"
    }

   

**Step 5.** Create prefix WITHOUT custom_fields 

    curl -X POST http://localhost:8080/api/ipam/prefixes/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "prefix": "10.0.1.0/24",
        "status": "active",
        "description": "Test prefix without custom_fields"
      }'

**Response:** HTTP 201

       {
      "id": 1,
      "url": "http://localhost:8080/api/ipam/prefixes/1/",
      "display_url": "http://localhost:8080/ipam/prefixes/1/",
      "display": "10.0.1.0/24",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "prefix": "10.0.1.0/24",
      "vrf": null,
      "scope_type": null,
      "scope_id": null,
      "scope": null,
      "tenant": null,
      "vlan": null,
      "status": {
        "value": "active",
        "label": "Active"
      },
      "role": null,
      "is_pool": false,
      "mark_utilized": false,
      "description": "Test prefix without custom_fields",
      "comments": "",
      "tags": [],
      "custom_fields": {
        "primary_subnet": true,
        "ripe_admin": "xxx-RIPE",
        "ripe_netname": null,
        "ripe_tech": null
      },
      "created": "2025-12-28T02:31:48.937486Z",
      "last_updated": "2025-12-28T02:31:48.937495Z",
      "children": 0,
      "_depth": 0
    }

**Step 6.** Create prefix WITH custom_fields

    curl -X POST http://localhost:8080/api/ipam/prefixes/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "prefix": "10.0.2.0/24",
        "status": "active",
        "description": "Test prefix with only primary_subnet",
        "custom_fields": {
          "primary_subnet": true
        }
      }'

### Buggy Response:
 HTTP 201 default value for ripe_admin is ignored and `null` is set

    {
      "id": 2,
      "url": "http://localhost:8080/api/ipam/prefixes/2/",
      "display_url": "http://localhost:8080/ipam/prefixes/2/",
      "display": "10.0.2.0/24",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "prefix": "10.0.2.0/24",
      "vrf": null,
      "scope_type": null,
      "scope_id": null,
      "scope": null,
      "tenant": null,
      "vlan": null,
      "status": {
        "value": "active",
        "label": "Active"
      },
      "role": null,
      "is_pool": false,
      "mark_utilized": false,
      "description": "Test prefix with only primary_subnet",
      "comments": "",
      "tags": [],
      "custom_fields": {
        "primary_subnet": true,
        "ripe_admin": null,
        "ripe_netname": null,
        "ripe_tech": null
      },
      "created": "2025-12-28T02:31:58.073663Z",
      "last_updated": "2025-12-28T02:31:58.073674Z",
      "children": 0,
      "_depth": 0
    }

### Expected Response:
 HTTP 201 default value for ripe_admin is set `"xxx-RIPE"`

    {
      "id": 2,
      "url": "http://localhost:8080/api/ipam/prefixes/2/",
      "display_url": "http://localhost:8080/ipam/prefixes/2/",
      "display": "10.0.2.0/24",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "prefix": "10.0.2.0/24",
      "vrf": null,
      "scope_type": null,
      "scope_id": null,
      "scope": null,
      "tenant": null,
      "vlan": null,
      "status": {
        "value": "active",
        "label": "Active"
      },
      "role": null,
      "is_pool": false,
      "mark_utilized": false,
      "description": "Test prefix with only primary_subnet",
      "comments": "",
      "tags": [],
      "custom_fields": {
        "primary_subnet": true,
        "ripe_admin": "xxx-RIPE",
        "ripe_netname": null,
        "ripe_tech": null
      },
      "created": "2025-12-28T03:01:53.363738Z",
      "last_updated": "2025-12-28T03:01:53.363748Z",
      "children": 0,
      "_depth": 0
    }




**Step 7.** Create prefix with different custom_field

    curl -X POST http://localhost:8080/api/ipam/prefixes/ \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "prefix": "10.0.3.0/24",
        "status": "active",
        "description": "Test prefix with only ripe_netname",
        "custom_fields": {
          "ripe_netname": "test"
        }
      }'

   
### Buggy Response:
400 Bad Request prefix is not created because primary_subnet (required) is not supplied
 

       {"__all__":["Missing required custom field 'primary_subnet'."]}

   

### Expected Response:
400 Bad Request prefix is not created because primary_subnet (required) is not supplied
  

      {"__all__":["Missing required custom field 'primary_subnet'."]}





## **NetBox#18887**

 
### Description
The API fails with an AttributeError because it receives a VMInterface object instead of the expected data dictionary during validation when saving a custom field via the API.

### GitHub Issue URL

https://github.com/netbox-community/netbox/issues/18887
  
### Triggering Endpoints

 - /api/extras/custom-fields/ 
 - /api/virtualization/cluster-types/
 - /api/virtualization/clusters/ 
 - /api/virtualization/virtual-machines/
 - /api/virtualization/interfaces/ 
 - /api/ipam/prefixes/
 - /api/ipam/prefixes/{id}/

### Triggering Behavior

**Step 1.** Create Custom Field

    curl -X POST "http://localhost:8080/api/extras/custom-fields/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "workflow_associated_prefix_to_interface_mapping",
        "label": "Associated VM Interface",
        "type": "object",
        "object_types": ["ipam.prefix"],
        "related_object_type": "virtualization.vminterface",
        "required": false
      }'

**Response:** HTTP 201  

    {
      "id": 1,
      "url": "http://localhost:8080/api/extras/custom-fields/1/",
      "display_url": "http://localhost:8080/extras/custom-fields/1/",
      "display": "Associated VM Interface",
      "object_types": [
        "ipam.prefix"
      ],
      "type": {
        "value": "object",
        "label": "Object"
      },
      "related_object_type": "virtualization.vminterface",
      "data_type": "object",
      "name": "workflow_associated_prefix_to_interface_mapping",
      "label": "Associated VM Interface",
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
      "created": "2025-12-29T00:22:21.687466Z",
      "last_updated": "2025-12-29T00:22:21.687476Z"
    }
    
**Step 2.** Create a Cluster Type

    curl -X POST "http://localhost:8080/api/virtualization/cluster-types/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "VMware",
        "slug": "vmware"
      }'



**Response:** HTTP 201

    {
      "id": 1,
      "url": "http://localhost:8080/api/virtualization/cluster-types/1/",
      "display_url": "http://localhost:8080/virtualization/cluster-types/1/",
      "display": "VMware",
      "name": "VMware",
      "slug": "vmware",
      "description": "",
      "tags": [],
      "custom_fields": {},
      "created": "2025-12-29T00:24:32.288652Z",
      "last_updated": "2025-12-29T00:24:32.288663Z"
    }




**Step 3.** Create a Cluster

    curl -X POST "http://localhost:8080/api/virtualization/clusters/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Test Cluster",
        "type": 1
      }'

  
     
   **Response**: HTTP 201

       {
      "id": 1,
      "url": "http://localhost:8080/api/virtualization/clusters/1/",
      "display_url": "http://localhost:8080/virtualization/clusters/1/",
      "display": "Test Cluster",
      "name": "Test Cluster",
      "type": {
        "id": 1,
        "url": "http://localhost:8080/api/virtualization/cluster-types/1/",
        "display": "VMware",
        "name": "VMware",
        "slug": "vmware",
        "description": ""
      },
      "group": null,
      "status": {
        "value": "active",
        "label": "Active"
      },
      "tenant": null,
      "scope_type": null,
      "scope_id": null,
      "scope": null,
      "description": "",
      "comments": "",
      "tags": [],
      "custom_fields": {},
      "created": "2025-12-29T00:24:57.208515Z",
      "last_updated": "2025-12-29T00:24:57.208525Z"
    }

   


**Step 4.** Create Virtual Machine with Cluster

    curl -X POST "http://localhost:8080/api/virtualization/virtual-machines/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "test-vm-01",
        "status": "active",
        "cluster": 1
      }'

  

**Response:** HTTP 201

    {
      "id": 1,
      "url": "http://localhost:8080/api/virtualization/virtual-machines/1/",
      "display_url": "http://localhost:8080/virtualization/virtual-machines/1/",
      "display": "test-vm-01",
      "name": "test-vm-01",
      "status": {
        "value": "active",
        "label": "Active"
      },
      "site": null,
      "cluster": {
        "id": 1,
        "url": "http://localhost:8080/api/virtualization/clusters/1/",
        "display": "Test Cluster",
        "name": "Test Cluster",
        "description": ""
      },
      "device": null,
      "serial": "",
      "role": null,
      "tenant": null,
      "platform": null,
      "primary_ip": null,
      "primary_ip4": null,
      "primary_ip6": null,
      "vcpus": null,
      "memory": null,
      "disk": null,
      "description": "",
      "comments": "",
      "config_template": null,
      "local_context_data": null,
      "tags": [],
      "custom_fields": {},
      "config_context": {},
      "created": "2025-12-29T00:25:43.881298Z",
      "last_updated": "2025-12-29T00:25:43.881308Z",
      "interface_count": 0,
      "virtual_disk_count": 0
    }

   

**Step 5.** Create VM Interface 

    curl -X POST "http://localhost:8080/api/virtualization/interfaces/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "virtual_machine": 1,
        "name": "eth0",
        "type": "virtual"
      }'

**Response:** HTTP 201

    {
      "id": 1,
      "url": "http://localhost:8080/api/virtualization/interfaces/1/",
      "display_url": "http://localhost:8080/virtualization/interfaces/1/",
      "display": "eth0",
      "virtual_machine": {
        "id": 1,
        "url": "http://localhost:8080/api/virtualization/virtual-machines/1/",
        "display": "test-vm-01",
        "name": "test-vm-01",
        "description": ""
      },
      "name": "eth0",
      "enabled": true,
      "parent": null,
      "bridge": null,
      "mtu": null,
      "mac_address": null,
      "primary_mac_address": null,
      "mac_addresses": [],
      "description": "",
      "mode": null,
      "untagged_vlan": null,
      "tagged_vlans": [],
      "qinq_svlan": null,
      "vlan_translation_policy": null,
      "vrf": null,
      "l2vpn_termination": null,
      "tags": [],
      "custom_fields": {},
      "created": "2025-12-29T00:26:17.453314Z",
      "last_updated": "2025-12-29T00:26:17.453325Z",
      "count_ipaddresses": 0,
      "count_fhrp_groups": 0
    }

**Step 6.** Create Prefix

    curl -X POST "http://localhost:8080/api/ipam/prefixes/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "prefix": "10.0.0.0/24",
        "status": "active"
      }'
**Response:** HTTP 201

    {
      "id": 1,
      "url": "http://localhost:8080/api/ipam/prefixes/1/",
      "display_url": "http://localhost:8080/ipam/prefixes/1/",
      "display": "10.0.0.0/24",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "prefix": "10.0.0.0/24",
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
      "description": "",
      "comments": "",
      "tags": [],
      "custom_fields": {},
      "created": "2025-12-29T00:26:48.407235Z",
      "last_updated": "2025-12-29T00:26:48.407245Z",
      "children": 0,
      "_depth": 0
    }


**Step 7.** Update Prefix with VMInterface Custom Field

    curl -X PATCH "http://localhost:8080/api/ipam/prefixes/1/" \
      -H "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
      -H "Content-Type: application/json" \
      -d '{
        "custom_fields": {
          "workflow_associated_prefix_to_interface_mapping": 1
        }
      }'

### Buggy Response:
HTTP 500 with response 

    {
      "error": "'VMInterface' object has no attribute 'get'",
      "exception": "AttributeError",
      "netbox_version": "4.2.5-Docker-3.2.0",
      "python_version": "3.12.3"
    }



### Expected Response:
HTTP 200 with response

    {
      "id": 1,
      "url": "http://localhost:8080/api/ipam/prefixes/1/",
      "display_url": "http://localhost:8080/ipam/prefixes/1/",
      "display": "10.0.0.0/24",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "prefix": "10.0.0.0/24",
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
      "description": "",
      "comments": "",
      "tags": [],
      "custom_fields": {
        "workflow_associated_prefix_to_interface_mapping": {
          "id": 1,
          "url": "http://localhost:8080/api/virtualization/interfaces/1/",
          "display": "eth0",
          "virtual_machine": {
            "id": 1,
            "url": "http://localhost:8080/api/virtualization/virtual-machines/1/",
            "display": "test-vm-01",
            "name": "test-vm-01",
            "description": ""
          },
          "name": "eth0",
          "description": ""
        }
      },
      "created": "2025-12-29T00:14:36.072773Z",
      "last_updated": "2025-12-29T00:15:11.052446Z",
      "children": 0,
      "_depth": 0
    }
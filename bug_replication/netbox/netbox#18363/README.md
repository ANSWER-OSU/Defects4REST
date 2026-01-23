## Netbox#18363

## Description
API POST request to create a MAC address fails with a 400 error indicating a schema validation issue for the assigned_object_id field.

## GitHub Issue URL
https://github.com/netbox-community/netbox/issues/18363
## Triggering Endpoints

 - /api/dcim/mac-addresses/

## **Triggering Behavior**
Step 1: Attempt to create a MAC address for the VM interface

    curl -i -X 'POST' \
      'http://localhost:8080/api/dcim/mac-addresses/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Token 0123456789abcdef0123456789abcdef01234567' \
      -d '{
      "mac_address": "BC:24:11:7E:0E:BF",
      "assigned_object_type": "virtualization.vminterface",
      "assigned_object_id": 1
    }'

 **Buggy Response:** 
 HTTP 400 Bad Request with message 

        {
      "assigned_object_id": [
        "This field cannot be null."
      ]
    }

   **Expected Response:** 
    HTTP 201 Created

        {
        "id":2,
        "url":"http://localhost:8080/api/dcim/mac-addresses/2/",
        "display_url":"http://localhost:8080/dcim/mac-addresses/2/",
        "display":"BC:24:11:7E:0E:BF",
        "mac_address":"BC:24:11:7E:0E:BF",
        "assigned_object_type":"virtualization.vminterface",
        "assigned_object_id":1,"assigned_object":
        {"id":1,"url":"http://localhost:8080/api/virtualization/interfaces/1/",
        "display":"eth0","virtual_machine":{"id":1,"url":"http://localhost:8080/api/virtualization/virtual-machines/1/","display":"test-vm","name":"test-vm","description":""},
        "name":"eth0","description":""},"description":"","comments":"","tags":[],
        "custom_fields":{},
        "created":"2025-12-26T04:15:41.705795Z","last_updated":"2025-12-26T04:15:41.705802Z"}

# **awx#11130**

 
## Description
API allows modification of restricted fields in the controlplane group without proper validation resulting in unintended changes.
## GitHub Issue URL
https://github.com/ansible/awx/issues/11130
## Triggering Endpoints

 - /api/v2/instance_groups/{id}/

## Triggering Behavior

**Step 1.**  Attempt to modify `is_container_group` to true

    curl -X PATCH https://localhost:8043/api/v2/instance_groups/1/ \
      -H "Content-Type: application/json" \
      -u admin:password \
      -d '{
        "is_container_group": true
      }' \
      -k

## Buggy Response
HTTP 200 with body 

    {
      "id": 1,
      "type": "instance_group",
      "url": "/api/v2/instance_groups/1/",
      "name": "controlplane",
      "is_container_group": true,
      "credential": null,
      "policy_instance_percentage": 100,
      "policy_instance_minimum": 0,
      "policy_instance_list": [],
      "pod_spec_override": ""
    }

## Expected Response:
HTTP 400 Bad Request with body 

    {
      "is_container_group": [
        "The controlplane instance group cannot be converted to a container group."
      ]
    }


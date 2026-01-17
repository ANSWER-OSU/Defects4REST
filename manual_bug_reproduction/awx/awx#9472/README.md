# **awx#9472**

 
## Description
The API returns an incorrectly formatted ansible_version field when ansible-core is installed due to changes in the ansible --version output specific to that environment.
## GitHub Issue URL
https://github.com/ansible/awx/issues/9472
## Triggering Endpoints

 - /api/v2/config/

## Triggering Behavior

**Step 1.**  Get Config 

    curl -X GET \ http://localhost:8013/api/v2/config/ \ -u admin:password

## Buggy Response
HTTP 200 with body 

    { "ansible_version":  "2.11.0"}

## Expected Response:
HTTP 200 with body 

    { "ansible_version":  "[core 2.11.0.dev0]"}
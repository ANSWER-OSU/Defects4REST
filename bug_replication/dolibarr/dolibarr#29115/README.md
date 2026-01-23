# **Dolibarr#29115**

 
## Description
Extra fields with and without default values behave inconsistently when updated via the API indicating environment or configuration-dependent behavior.

## GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/29115
## Triggering Endpoints

 - /products/{id}
 - /products

## Triggering Behavior

**Step 1.** Create a product with extra fields already set

    curl -s -X POST "http://localhost:8080/api/index.php/products" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "ref": "BUG-29115-TEST",
        "label": "Bug 29115 test product",
        "array_options": {
          "options_checkbox_field": "1",
          "options_text_field": "Original text value",
          "options_select_field": "option1",
          "options_another_field": "Another value"
        }
      }' | jq

**Response:** HTTP 200  with body

    {
      "id": 1,
      "ref": "BUG-29115-TEST",
      "label": "Bug 29115 test product",
      "array_options": {
        "options_checkbox_field": "1",
        "options_text_field": "Original text value",
        "options_select_field": "option1",
        "options_another_field": "Another value"
      }
    }

**Step 2:** Update only ONE extra field (checkbox)

    curl -s -X PUT "http://localhost:8080/api/index.php/products/1" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "array_options": {
          "options_checkbox_field": "0"
        }
      }' | jq

## Buggy Response
HTTP 200 with body 

    {
      "id": 1,
      "ref": "BUG-29115-TEST",
      "label": "Bug 29115 test product",
      "array_options": {
        "options_checkbox_field": "0",
        "options_text_field": null,
        "options_select_field": null,
        "options_another_field": null
      }
    }


## Expected Response:
HTTP  200 with body

    {
      "id": 1,
      "ref": "BUG-29115-TEST",
      "label": "Bug 29115 test product",
      "array_options": {
        "options_checkbox_field": "0",
        "options_text_field": "Original text value",
        "options_select_field": "option1",
        "options_another_field": "Another value"
      }
    }







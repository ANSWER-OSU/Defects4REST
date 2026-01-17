## **Dolibarr#23415**

 
### Description
The API allows invalid or missing values for the 'ref' field when creating or updating a BOM which indicates improper validation of required fields in the payload.

### GitHub Issue URL
https://github.com/Dolibarr/dolibarr/issues/23415
  
### Triggering Endpoints

 - /boms 
 - /boms/{id}

### Triggering Behavior

**Step 1.** Create a BOM in DRAFT Status with Temporary Reference

    curl -X POST "http://localhost:8080/api/index.php/boms" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "ref": "(PROV54)",
        "label": "Test BOM",
        "fk_product": 1,
        "bomtype": 0,
        "qty": 1,
        "status": 0
      }'

Response: HTTP 200 OK with response `BOM id = 1`

**Step 2.** Update BOM to VALIDATED Status While Keeping Temporary Reference

    curl -X PUT "http://localhost:8080/api/index.php/boms/1" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "ref": "(PROV54)",
        "status": 1
      }'

### Buggy Response
HTTP 200 with response still contains the temporary reference `"(PROV54)"`

    {
      "ref": "(PROV54)",
      "label": "Test BOM",
      "bomtype": 0,
      "description": null,
      "date_creation": 1767054978,
      "tms": 1767054978,
      "fk_user_creat": 1,
      "fk_user_modif": 1,
      "import_key": null,
      "status": 1,
      "fk_product": 1,
      "qty": 1,
      "efficiency": 1,
      "lines": [],
      "total_cost": 0,
      "unit_cost": 0,
      "id": 1,
      "entity": null,
      "array_options": [],
      "array_languages": null,
      "contacts_ids": null,
      "linked_objects": null,
      "linkedObjectsIds": null,
      "fk_project": null,
      "contact_id": null,
      "user": null,
      "origin": null,
      "origin_id": null,
      "ref_ext": null,
      "region_id": null,
      "demand_reason_id": null,
      "transport_mode_id": null,
      "model_pdf": null,
      "last_main_doc": null,
      "fk_bank": null,
      "note_public": null,
      "note_private": null,
      "date_validation": null,
      "date_modification": null,
      "date_cloture": null,
      "user_author": null,
      "user_creation": null,
      "user_creation_id": null,
      "user_valid": null,
      "user_validation": null,
      "user_validation_id": null,
      "user_closing_id": null,
      "user_modification": null,
      "user_modification_id": null,
      "specimen": 0,
      "duration": null,
      "fk_warehouse": null,
      "date_valid": "",
      "fk_user_valid": null
    }


### Expected Response:
HTTP 200 with response have proper numbered references like "BOM2512-0001" for ref

    {
      "ref": "BOM2512-0001",
      "label": "Test BOM",
      "bomtype": 0,
      "description": null,
      "date_creation": 1767054626,
      "tms": 1767054626,
      "fk_user_creat": 1,
      "fk_user_modif": 1,
      "import_key": null,
      "status": 1,
      "fk_product": 1,
      "qty": 1,
      "efficiency": 1,
      "lines": [],
      "total_cost": 0,
      "unit_cost": 0,
      "id": 1,
      "entity": null,
      "array_options": [],
      "array_languages": null,
      "contacts_ids": null,
      "linked_objects": null,
      "linkedObjectsIds": null,
      "fk_project": null,
      "contact_id": null,
      "user": null,
      "origin": null,
      "origin_id": null,
      "ref_ext": null,
      "region_id": null,
      "demand_reason_id": null,
      "transport_mode_id": null,
      "model_pdf": null,
      "last_main_doc": null,
      "fk_bank": null,
      "note_public": null,
      "note_private": null,
      "date_validation": null,
      "date_modification": null,
      "date_cloture": null,
      "user_author": null,
      "user_creation": null,
      "user_creation_id": null,
      "user_valid": null,
      "user_validation": null,
      "user_validation_id": null,
      "user_closing_id": null,
      "user_modification": null,
      "user_modification_id": null,
      "specimen": 0,
      "duration": null,
      "fk_warehouse": null,
      "date_valid": "",
      "fk_user_valid": null,
      "product": {
        "libelle": null,
        "label": null,
        "description": null,
        "other": null,
        "type": 0,
        "price": null,
        "price_formated": null,
        "price_ttc": null,
        "price_ttc_formated": null,
        "price_min": null,
        "price_min_ttc": null,
        "price_base_type": null,
        "multiprices": [],
        "multiprices_ttc": [],
        "multiprices_base_type": [],
        "multiprices_min": [],
        "multiprices_min_ttc": [],
        "multiprices_tva_tx": [],
        "multiprices_recuperableonly": [],
        "price_by_qty": null,
        "prices_by_qty": [],
        "prices_by_qty_id": [],
        "prices_by_qty_list": [],
        "multilangs": [],
        "default_vat_code": null,
        "tva_tx": null,
        "tva_npr": 0,
        "remise_percent": null,
        "localtax1_tx": null,
        "localtax2_tx": null,
        "localtax1_type": null,
        "localtax2_type": null,
        "desc_supplier": null,
        "vatrate_supplier": null,
        "default_vat_code_supplier": null,
        "fourn_multicurrency_price": null,
        "fourn_multicurrency_unitprice": null,
        "fourn_multicurrency_tx": null,
        "fourn_multicurrency_id": null,
        "fourn_multicurrency_code": null,
        "packaging": null,
        "lifetime": null,
        "qc_frequency": null,
        "stock_reel": 0,
        "stock_theorique": null,
        "cost_price": null,
        "pmp": null,
        "seuil_stock_alerte": 0,
        "desiredstock": 0,
        "duration_value": null,
        "fk_default_workstation": null,
        "duration_unit": null,
        "status": 0,
        "tosell": null,
        "status_buy": 0,
        "tobuy": null,
        "finished": null,
        "fk_default_bom": null,
        "status_batch": 0,
        "batch_mask": "",
        "customcode": null,
        "url": null,
        "weight": null,
        "weight_units": null,
        "length": null,
        "length_units": null,
        "width": null,
        "width_units": null,
        "height": null,
        "height_units": null,
        "surface": null,
        "surface_units": null,
        "volume": null,
        "volume_units": null,
        "net_measure": null,
        "net_measure_units": null,
        "accountancy_code_sell": null,
        "accountancy_code_sell_intra": null,
        "accountancy_code_sell_export": null,
        "accountancy_code_buy": null,
        "accountancy_code_buy_intra": null,
        "accountancy_code_buy_export": null,
        "barcode": null,
        "date_creation": null,
        "date_modification": null,
        "product_fourn_id": null,
        "product_id_already_linked": null,
        "nbphoto": 0,
        "stock_warehouse": [],
        "fk_default_warehouse": null,
        "fk_price_expression": null,
        "fourn_qty": null,
        "fourn_pu": null,
        "fourn_price_base_type": null,
        "fourn_socid": null,
        "ref_fourn": null,
        "ref_supplier": null,
        "fk_unit": null,
        "price_autogen": 0,
        "supplierprices": null,
        "is_object_used": null,
        "mandatory_period": null,
        "id": null,
        "entity": null,
        "import_key": null,
        "array_options": [],
        "array_languages": null,
        "contacts_ids": null,
        "linked_objects": null,
        "linkedObjectsIds": null,
        "fk_project": null,
        "contact_id": null,
        "user": null,
        "origin": null,
        "origin_id": null,
        "ref": null,
        "ref_ext": null,
        "region_id": null,
        "demand_reason_id": null,
        "transport_mode_id": null,
        "model_pdf": null,
        "last_main_doc": null,
        "fk_bank": null,
        "note_public": null,
        "note_private": null,
        "lines": null,
        "date_validation": null,
        "date_cloture": null,
        "user_author": null,
        "user_creation": null,
        "user_creation_id": null,
        "user_valid": null,
        "user_validation": null,
        "user_validation_id": null,
        "user_closing_id": null,
        "user_modification": null,
        "user_modification_id": null,
        "specimen": 0
      }
    }
    

**Step 3.** Attempt to Create Validated BOM Without Providing 'ref' Field

    curl -X POST "http://localhost:8080/api/index.php/boms" \
      -H "DOLAPIKEY: 4ooZSJGOzXBojF7g4p54hr6u5YK2w09B" \
      -H "Content-Type: application/json" \
      -d '{
        "label": "Test BOM Without Ref",
        "fk_product": 1,
        "bomtype": 0,
        "qty": 1,
        "status": 1
      }'


### Buggy Response
HTTP 400 with response 

    "Bad Request: ref field missing"


### Expected Response:
HTTP 200 Ok with response ID = 2 (Created the new BOM)

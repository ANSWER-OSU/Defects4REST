# nocodb#1756

## Description
Filtering on linked record columns returns incorrect results indicating the filter logic for query parameters is faulty. (HTTP 200)

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/1756

## Triggering Endpoints
- `/api/v1/db/meta/views/{viewId}/filters`
- `/api/v1/db/data/noco/{projectName}/{tableName}/views/{tableName}`

## Prerequisites
**Step 1.** Sign Up
```
curl 'http://localhost:8080/api/v1/db/auth/user/signup' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"admin@admin.com","password":"@Admin123","ignore_subscribe":true}'
```
**Response:** HTTP 200.
```
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc"}
```

**Step 2.** Create a project
```
curl 'http://localhost:8080/api/v1/db/meta/projects/' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data-raw '{"title":"Buggy1756"}'
```
**Response:** HTTP 200.
```
{"is_meta":1,"id":"p_zmw0yw7bgaf2e2","title":"Buggy1756","prefix":"nc_lm05__","status":null,"description":null,"meta":null,"color":null,"uuid":null,"password":null,"roles":null,"deleted":0,"order":null,"created_at":"2025-12-11 16:01:08","updated_at":"2025-12-11 16:01:08","bases":[{"id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","alias":null,"meta":null,"is_meta":1,"type":"sqlite3","inflection_column":"camelize","inflection_table":"camelize","created_at":"2025-12-11 16:01:08","updated_at":"2025-12-11 16:01:08"}]}
```
**Step 3.** Create Table A
```
curl 'http://localhost:8080/api/v1/db/meta/projects/p_zmw0yw7bgaf2e2/tables' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data-raw '{"table_name":"nc_lm05__table_a","title":"TableA","columns":[{"column_name":"id","title":"Id","dt":"integer","dtx":"integer","ct":"int(11)","nrqd":false,"rqd":true,"ck":false,"pk":true,"un":false,"ai":true,"cdf":null,"clen":null,"np":null,"ns":0,"dtxp":"","dtxs":"","altered":1,"uidt":"ID","uip":"","uicn":""},{"column_name":"title","title":"Title","dt":"varchar","dtx":"specificType","ct":"varchar","nrqd":true,"rqd":false,"ck":false,"pk":false,"un":false,"ai":false,"cdf":null,"clen":45,"np":null,"ns":null,"dtxp":"","dtxs":"","altered":1,"uidt":"SingleLineText","uip":"","uicn":""}]}'
```
**Response:** HTTP 200.
```
{"id":"md_auxbkadorbcnwt","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","table_name":"nc_lm05__table_a","title":"TableA","type":"table","meta":null,"schema":null,"enabled":1,"mm":0,"tags":null,"pinned":null,"deleted":null,"order":1,"created_at":"2025-12-11 16:01:43","updated_at":"2025-12-11 16:01:43","columns":[{"id":"cl_kex9dd9lunlouz","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_auxbkadorbcnwt","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":"0","clen":null,"cop":null,"pk":1,"pv":null,"rqd":1,"un":0,"ct":"int(11)","ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"integer","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:01:43","updated_at":"2025-12-11 16:01:43"},{"id":"cl_a4rfyfyg582hwg","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_auxbkadorbcnwt","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":null,"pk":0,"pv":1,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:01:44","updated_at":"2025-12-11 16:01:44"}],"views":[{"id":"vw_2je1e6v9g5g49a","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_auxbkadorbcnwt","title":"TableA","type":3,"is_default":1,"show_system_fields":null,"lock_type":"collaborative","uuid":null,"password":null,"show":1,"order":1,"created_at":"2025-12-11 16:01:43","updated_at":"2025-12-11 16:01:43","view":{"fk_view_id":"vw_2je1e6v9g5g49a","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","uuid":null,"created_at":"2025-12-11 16:01:43","updated_at":"2025-12-11 16:01:43"}}],"columnsById":{"cl_kex9dd9lunlouz":{"id":"cl_kex9dd9lunlouz","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_auxbkadorbcnwt","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":"0","clen":null,"cop":null,"pk":1,"pv":null,"rqd":1,"un":0,"ct":"int(11)","ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"integer","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:01:43","updated_at":"2025-12-11 16:01:43"},"cl_a4rfyfyg582hwg":{"id":"cl_a4rfyfyg582hwg","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_auxbkadorbcnwt","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":null,"pk":0,"pv":1,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:01:44","updated_at":"2025-12-11 16:01:44"}}}
```

**Step 4.** Create Table B
```
curl 'http://localhost:8080/api/v1/db/meta/projects/p_zmw0yw7bgaf2e2/tables' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data-raw '{"table_name":"nc_lm05__table_b","title":"TableB","columns":[{"column_name":"id","title":"Id","dt":"integer","dtx":"integer","ct":"int(11)","nrqd":false,"rqd":true,"ck":false,"pk":true,"un":false,"ai":true,"cdf":null,"clen":null,"np":null,"ns":0,"dtxp":"","dtxs":"","altered":1,"uidt":"ID","uip":"","uicn":""},{"column_name":"title","title":"Title","dt":"varchar","dtx":"specificType","ct":"varchar","nrqd":true,"rqd":false,"ck":false,"pk":false,"un":false,"ai":false,"cdf":null,"clen":45,"np":null,"ns":null,"dtxp":"","dtxs":"","altered":1,"uidt":"SingleLineText","uip":"","uicn":""}]}'
```
**Response:** HTTP 200.
```
{"id":"md_8l8buwrs5j757t","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","table_name":"nc_lm05__table_b","title":"TableB","type":"table","meta":null,"schema":null,"enabled":1,"mm":0,"tags":null,"pinned":null,"deleted":null,"order":2,"created_at":"2025-12-11 16:03:04","updated_at":"2025-12-11 16:03:04","columns":[{"id":"cl_6d2ab5tw5dooz8","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":"0","clen":null,"cop":null,"pk":1,"pv":null,"rqd":1,"un":0,"ct":"int(11)","ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"integer","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"},{"id":"cl_o60cevkhaelbkw","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":null,"pk":0,"pv":1,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"}],"views":[{"id":"vw_lphr03h9l85407","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"TableB","type":3,"is_default":1,"show_system_fields":null,"lock_type":"collaborative","uuid":null,"password":null,"show":1,"order":1,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05","view":{"fk_view_id":"vw_lphr03h9l85407","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","uuid":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"}}],"columnsById":{"cl_6d2ab5tw5dooz8":{"id":"cl_6d2ab5tw5dooz8","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":"0","clen":null,"cop":null,"pk":1,"pv":null,"rqd":1,"un":0,"ct":"int(11)","ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"integer","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"},"cl_o60cevkhaelbkw":{"id":"cl_o60cevkhaelbkw","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":null,"pk":0,"pv":1,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"}}}
```

**Step 5.** Populate Table B
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/data/bulk/noco/Buggy1756/TableB \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data '[
  {
    "Title": "B1"
  },
  {
    "Title": "B2"
  },
  {
    "Title": "B3"
  }
]'
```
**Response:** HTTP 200.

**Step 6.** Table B: Create hasMany column to Table A
```
curl 'http://localhost:8080/api/v1/db/meta/tables/md_8l8buwrs5j757t/columns' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data-raw '{"parentId":"md_8l8buwrs5j757t","childID":null,"childColumn":"nc_lm05__table_b_id","childTable":"nc_lm05__table_b","parentTable":"","parentColumn":"","onDelete":"NO ACTION","onUpdate":"NO ACTION","updateRelation":false,"virtual":true,"childId":"md_auxbkadorbcnwt","uidt":"LinkToAnotherRecord","title":"Example","type":"hm"}'
```
**Response:** HTTP 200.
```
{"id":"md_8l8buwrs5j757t","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","table_name":"nc_lm05__table_b","title":"TableB","type":"table","meta":null,"schema":null,"enabled":1,"mm":0,"tags":null,"pinned":null,"deleted":null,"order":2,"created_at":"2025-12-11 16:03:04","updated_at":"2025-12-11 16:03:04","columns":[{"id":"cl_6d2ab5tw5dooz8","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":"0","clen":null,"cop":null,"pk":1,"pv":null,"rqd":1,"un":0,"ct":"int(11)","ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"integer","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"},{"id":"cl_o60cevkhaelbkw","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":null,"pk":0,"pv":1,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"},{"id":"cl_4af7di3r334fq7","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Example","column_name":null,"uidt":"LinkToAnotherRecord","dt":null,"np":null,"ns":null,"clen":null,"cop":null,"pk":null,"pv":null,"rqd":null,"un":null,"ct":null,"ai":null,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":null,"dtxp":null,"dtxs":null,"au":null,"validate":null,"virtual":null,"deleted":null,"system":0,"order":null,"created_at":"2025-12-11 16:05:13","updated_at":"2025-12-11 16:05:13","colOptions":{"virtual":1,"id":"ln_cm2zkxsleey506","ref_db_alias":null,"type":"hm","db_type":null,"fk_column_id":"cl_4af7di3r334fq7","fk_related_model_id":"md_auxbkadorbcnwt","fk_child_column_id":"cl_jxuxqdmxnpqhrl","fk_parent_column_id":"cl_6d2ab5tw5dooz8","fk_mm_model_id":null,"fk_mm_child_column_id":null,"fk_mm_parent_column_id":null,"ur":null,"dr":null,"fk_index_name":null,"deleted":null,"created_at":"2025-12-11 16:05:13","updated_at":"2025-12-11 16:05:13"}}],"views":[{"id":"vw_lphr03h9l85407","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"TableB","type":3,"is_default":1,"show_system_fields":null,"lock_type":"collaborative","uuid":null,"password":null,"show":1,"order":1,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05","view":{"fk_view_id":"vw_lphr03h9l85407","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","uuid":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"}}],"columnsById":{"cl_6d2ab5tw5dooz8":{"id":"cl_6d2ab5tw5dooz8","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":"0","clen":null,"cop":null,"pk":1,"pv":null,"rqd":1,"un":0,"ct":"int(11)","ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"integer","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"},"cl_o60cevkhaelbkw":{"id":"cl_o60cevkhaelbkw","base_id":"ds_vlzmwlh34h4hkn","project_id":"p_zmw0yw7bgaf2e2","fk_model_id":"md_8l8buwrs5j757t","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":null,"pk":0,"pv":1,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":null,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 16:03:05","updated_at":"2025-12-11 16:03:05"}}}
```

**Step 7.** Populate Table A
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/data/bulk/noco/Buggy1756/TableA \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data '[
  {
    "Title": "A1"
  },
  {
    "Title": "A2"
  },
  {
    "Title": "A3"
  }
]'
```
**Response:** HTTP 200.


**Step 7b.** Table B: Populate data on hasMany column
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/data/noco/Buggy1756/TableA/1/hm/TableBRead/1 \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc'
```
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/data/noco/Buggy1756/TableA/2/hm/TableBRead/2 \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc'
```
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/data/noco/Buggy1756/TableA/3/hm/TableBRead/3 \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc'
```
**Response:** HTTP 200.
```
{"msg":"success"}
```
## Triggering Behavior

**Step 8.** Create "isEqual" filter on "TableBRead" in Table A
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/meta/views/vw_3pbiyig1evk2xn/filters \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --data '{
  "comparison_op": "eq",
  "comparison_sub_op": null,
  "fk_column_id": "cl_xf46fgfejluv2s",
  "is_group": false,
  "logical_op": "and",
  "value": "B1"
}'
```
**Response:** HTTP 200.
```
{
  "id": "fi_pw7bsst934zqco",
  "base_id": "ds_vlzmwlh34h4hkn",
  "project_id": "p_zmw0yw7bgaf2e2",
  "fk_view_id": "vw_3pbiyig1evk2xn",
  "fk_hook_id": null,
  "fk_column_id": "cl_xf46fgfejluv2s",
  "fk_parent_id": null,
  "logical_op": "and",
  "comparison_op": "eq",
  "value": "B1",
  "is_group": 0,
  "order": 1,
  "created_at": "2025-12-11 16:09:53",
  "updated_at": "2025-12-11 16:09:53"
}
```

**Step 9.** Retrieve filtered data on Table A
```
curl --request GET \
  --url http://localhost:8080/api/v1/db/data/noco/Buggy1756/TableA/views/TableA \
  --header 'accept: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfNGEybTk1cG8zNHV2ZzQiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0Njg4MzN9.1v99bLdmaLJOSoZalXg9ghxQGDuDyMDrfxrNthMt1Gc' \
  --cookie refresh_token=cd95ec427b22ccec0bdcd7891bfb4e8d5f9ab0a25ca3d9671a5ad11dbd4c6ff902be8bb026299e7a
```
## Buggy Response: 
HTTP 200 - Data is not filtered
```
{
  "list": [
    {
      "Id": 1,
      "Title": "A1",
      "TableBRead": {
        "Id": 1,
        "Title": "B1"
      }
    },
    {
      "Id": 2,
      "Title": "A2",
      "TableBRead": {
        "Id": 2,
        "Title": "B2"
      }
    },
    {
      "Id": 3,
      "Title": "A3",
      "TableBRead": {
        "Id": 3,
        "Title": "B3"
      }
    }
  ],
  "pageInfo": {
    "totalRows": 3,
    "page": 1,
    "pageSize": 25,
    "isFirstPage": true,
    "isLastPage": true
  }
}
```

## Expected Response:
HTTP 200 - Only retrieve filtered data based on the filter
```
{
    "list": [
        {
            "Id": 1,
            "Title": "A1",
            "TableBRead": {
                "Id": 1,
                "Title": "B1"
            }
        }
    ],
    "pageInfo": {
        "totalRows": 1,
        "page": 1,
        "pageSize": "25",
        "isFirstPage": true,
        "isLastPage": true
    }
}
```

# nocodb#1981

## Description
The API does not correctly interpret the (*) wildcard in the nested fields query parameter resulting in incomplete field selection. (HTTP 200)

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/1981

## Triggering Endpoints
`/api/v1/db/data/noco/{projectName}/{tableName}?nested[{m2mColumnName}][fields]=%2A`

(encoded version): `/api/v1/db/data/noco/{projectName}/{tableName}?nested%5B{m2mColumnName}%5D%5Bfields%5D=%2A`

## Prerequisites

**Step 1.** Sign Up
```
curl 'http://localhost:8080/api/v1/db/auth/user/signup' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"admin@admin.com","password":"@Admin123","ignore_subscribe":true}'
```
**Response:** HTTP 200
```
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c"}
```

**Step 2.** Create a project
```curl 'http://localhost:8080/api/v1/db/meta/projects/' \
  -H 'Accept: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
  --data-raw '{"title":"Buggy1981"}'
```
**Response:** HTTP 200
```
{"is_meta":1,"id":"p_ki6z7rki0r2k0q","title":"Buggy1981","prefix":"nc_b2ja__","status":null,"description":null,"meta":null,"color":null,"uuid":null,"password":null,"roles":null,"deleted":0,"order":null,"created_at":"2025-12-11 12:07:17","updated_at":"2025-12-11 12:07:17","bases":[{"id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","alias":null,"meta":null,"is_meta":1,"type":"sqlite3","inflection_column":"camelize","inflection_table":"camelize","created_at":"2025-12-11 12:07:17","updated_at":"2025-12-11 12:07:17"}]}
```

**Step 3.** Create Table: Students
```
curl --request POST \
  --url http://localhost:8080/api/v1/db/meta/projects/p_ki6z7rki0r2k0q/tables \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfeGZqNDZmNTlwZHdqZWwiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTU4NjN9.RAraoAlxks5CYftXQer0KZq4OTbOLnO30ENwjdXk-Rw' \
  --data '{
  "table_name": "students",
  "title": "Students",
  "columns": [
    {
      "column_name": "id",
      "title": "Id",
      "dt": "integer",
      "dtx": "integer",
      "ct": "int(11)",
      "nrqd": false,
      "rqd": true,
      "ck": false,
      "pk": true,
      "un": false,
      "ai": true,
      "cdf": null,
      "clen": null,
      "np": null,
      "ns": 0,
      "dtxp": "",
      "dtxs": "",
      "altered": 1,
      "uidt": "ID",
      "uip": "",
      "uicn": ""
    },
    {
      "column_name": "title",
      "title": "Title",
      "dt": "varchar",
      "dtx": "specificType",
      "ct": "varchar",
      "nrqd": true,
      "rqd": false,
      "ck": false,
      "pk": false,
      "un": false,
      "ai": false,
      "cdf": null,
      "clen": 45,
      "np": null,
      "ns": null,
      "dtxp": "",
      "dtxs": "",
      "altered": 1,
      "uidt": "SingleLineText",
      "uip": "",
      "uicn": ""
    }
  ]
}'
```
**Response:** HTTP 200.
```
{"id":"md_c7ohgov0ah4uu5","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","table_name":"nc_b2ja__students","title":"Students","type":"table","meta":null,"schema":null,"enabled":1,"mm":0,"tags":null,"pinned":null,"deleted":null,"order":1,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10","columns":[{"id":"cl_fvo6uey8uacym8","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_c7ohgov0ah4uu5","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":null,"clen":null,"cop":"0","pk":1,"pv":null,"rqd":1,"un":null,"ct":null,"ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":1,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10"},{"id":"cl_ij9ojfhug1fk7c","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_c7ohgov0ah4uu5","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":null,"cop":"1","pk":0,"pv":1,"rqd":0,"un":null,"ct":null,"ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":2,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10"}],"views":[{"id":"vw_s071v7n7v8htmp","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_c7ohgov0ah4uu5","title":"Students","type":3,"is_default":1,"show_system_fields":null,"lock_type":"collaborative","uuid":null,"password":null,"show":1,"order":1,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10","view":{"fk_view_id":"vw_s071v7n7v8htmp","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","uuid":null,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10"}}],"columnsById":{"cl_fvo6uey8uacym8":{"id":"cl_fvo6uey8uacym8","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_c7ohgov0ah4uu5","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":null,"clen":null,"cop":"0","pk":1,"pv":null,"rqd":1,"un":null,"ct":null,"ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":1,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10"},"cl_ij9ojfhug1fk7c":{"id":"cl_ij9ojfhug1fk7c","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_c7ohgov0ah4uu5","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":null,"cop":"1","pk":0,"pv":1,"rqd":0,"un":null,"ct":null,"ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":2,"created_at":"2025-12-11 12:08:10","updated_at":"2025-12-11 12:08:10"}}}
```

**Step 4.** Create Table: Courses
```
curl 'http://localhost:8080/api/v1/db/meta/projects/p_ki6z7rki0r2k0q/tables' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
  --data-raw '{"table_name":"nc_b2ja__courses","title":"Courses","columns":[{"column_name":"id","title":"Id","dt":"integer","dtx":"integer","ct":"int(11)","nrqd":false,"rqd":true,"ck":false,"pk":true,"un":false,"ai":true,"cdf":null,"clen":null,"np":null,"ns":0,"dtxp":"","dtxs":"","altered":1,"uidt":"ID","uip":"","uicn":""},{"column_name":"title","title":"Title","dt":"varchar","dtx":"specificType","ct":"varchar","nrqd":true,"rqd":false,"ck":false,"pk":false,"un":false,"ai":false,"cdf":null,"clen":45,"np":null,"ns":null,"dtxp":"","dtxs":"","altered":1,"uidt":"SingleLineText","uip":"","uicn":""}]}'
```
**Response:** HTTP 200.
```
{"id":"md_cdk4i2fvwc9539","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","table_name":"nc_b2ja__courses","title":"Courses","type":"table","meta":null,"schema":null,"enabled":1,"mm":0,"tags":null,"pinned":null,"deleted":null,"order":2,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29","columns":[{"id":"cl_aaqzc0x8qqxz3y","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":null,"clen":null,"cop":"0","pk":1,"pv":null,"rqd":1,"un":null,"ct":null,"ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":1,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"},{"id":"cl_o2ipjavs5nwg4f","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":null,"cop":"1","pk":0,"pv":1,"rqd":0,"un":null,"ct":null,"ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":2,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"}],"views":[{"id":"vw_w8nr8yme97f40v","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Courses","type":3,"is_default":1,"show_system_fields":null,"lock_type":"collaborative","uuid":null,"password":null,"show":1,"order":1,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29","view":{"fk_view_id":"vw_w8nr8yme97f40v","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","uuid":null,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"}}],"columnsById":{"cl_aaqzc0x8qqxz3y":{"id":"cl_aaqzc0x8qqxz3y","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":null,"clen":null,"cop":"0","pk":1,"pv":null,"rqd":1,"un":null,"ct":null,"ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":1,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"},"cl_o2ipjavs5nwg4f":{"id":"cl_o2ipjavs5nwg4f","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":null,"cop":"1","pk":0,"pv":1,"rqd":0,"un":null,"ct":null,"ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":2,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"}}}
```
**Step 5.** Courses: Create Column "teacher"
```
curl 'http://localhost:8080/api/v1/db/meta/tables/md_cdk4i2fvwc9539/columns' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
  --data-raw '{"column_name":"teacher","dt":"varchar","dtx":"specificType","ct":"varchar","nrqd":true,"rqd":false,"ck":false,"pk":false,"un":false,"ai":false,"cdf":null,"clen":45,"np":null,"ns":null,"dtxp":"","dtxs":"","altered":1,"uidt":"SingleLineText","uip":"","uicn":"","cno":"title3","table_name":"nc_b2ja__courses","title":"teacher"}'
```
**Response:** HTTP 200.
```
{"id":"md_cdk4i2fvwc9539","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","table_name":"nc_b2ja__courses","title":"Courses","type":"table","meta":null,"schema":null,"enabled":1,"mm":0,"tags":null,"pinned":null,"deleted":null,"order":2,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29","columns":[{"id":"cl_aaqzc0x8qqxz3y","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":null,"clen":null,"cop":"0","pk":1,"pv":null,"rqd":1,"un":null,"ct":null,"ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":1,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"},{"id":"cl_o2ipjavs5nwg4f","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":null,"cop":"1","pk":0,"pv":1,"rqd":0,"un":null,"ct":null,"ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":2,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"},{"id":"cl_dfaajviamutt8d","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"teacher","column_name":"teacher","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":"45","cop":"2","pk":0,"pv":null,"rqd":0,"un":0,"ct":"varchar","ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":null,"created_at":"2025-12-11 12:10:37","updated_at":"2025-12-11 12:10:37"}],"views":[{"id":"vw_w8nr8yme97f40v","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Courses","type":3,"is_default":1,"show_system_fields":null,"lock_type":"collaborative","uuid":null,"password":null,"show":1,"order":1,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29","view":{"fk_view_id":"vw_w8nr8yme97f40v","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","uuid":null,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"}}],"columnsById":{"cl_aaqzc0x8qqxz3y":{"id":"cl_aaqzc0x8qqxz3y","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Id","column_name":"id","uidt":"ID","dt":"integer","np":null,"ns":null,"clen":null,"cop":"0","pk":1,"pv":null,"rqd":1,"un":null,"ct":null,"ai":1,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"specificType","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":1,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"},"cl_o2ipjavs5nwg4f":{"id":"cl_o2ipjavs5nwg4f","base_id":"ds_vswq2ldd66gb66","project_id":"p_ki6z7rki0r2k0q","fk_model_id":"md_cdk4i2fvwc9539","title":"Title","column_name":"title","uidt":"SingleLineText","dt":"varchar","np":null,"ns":null,"clen":null,"cop":"1","pk":0,"pv":1,"rqd":0,"un":null,"ct":null,"ai":0,"unique":null,"cdf":null,"cc":null,"csn":null,"dtx":"string","dtxp":"","dtxs":"","au":0,"validate":null,"virtual":null,"deleted":null,"system":null,"order":2,"created_at":"2025-12-11 12:09:29","updated_at":"2025-12-11 12:09:29"}}}
```

**Step 6.** Students: Create M2M column: "coursesTaken"
```
curl 'http://localhost:8080/api/v1/db/meta/tables/md_c7ohgov0ah4uu5/columns' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
  --data-raw '{"parentId":"md_c7ohgov0ah4uu5","childID":null,"childColumn":"nc_b2ja__students_id","childTable":"nc_b2ja__students","parentTable":"","parentColumn":"","onDelete":"NO ACTION","onUpdate":"NO ACTION","updateRelation":false,"virtual":true,"childId":"md_cdk4i2fvwc9539","uidt":"LinkToAnotherRecord","title":"coursesTaken","type":"mm"}'
```

**Step 7.** Courses: Insert data
```
curl 'http://localhost:8080/api/v1/db/data/noco/Buggy1981/Courses' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
  --data-raw '{"Title":"Math","teacher":"John"}'
```
**Response:** HTTP 200.
```
{"Id":1,"Title":"Math","teacher":"John"}
```
## Triggering Behavior
**Step 8.** Students: Insert data
```
curl 'http://localhost:8080/api/v1/db/data/noco/Buggy1981/Students' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
  --data-raw '{"Title":"Michael"}'
```
**Response:** HTTP 200
```
{"Id":1,"Title":"Michael"}
```

**Step 8b.** Students: Insert M2M value
```
curl 'http://localhost:8080/api/v1/db/data/noco/Buggy1981/Students/1/mm/coursesTaken/1' \
  -X 'POST' \
  -H 'Accept: application/json' \
  -H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfbm96ZmQxZm1xc3E5bGIiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTQ3NzR9.hgbj20ONiuLgIx6v7J-sSFqTDXF7wBJJlf0w8SCPi_c' \
```
**Response:** HTTP 200

**Step 9.** Retrieve data from Students, including all columns in nested field.
```
curl -X GET "http://localhost:8080/api/v1/db/data/noco/Buggy1981/Students?nested%5BcoursesTaken%5D%5Bfields%5D=%2A" -H "xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfeGZqNDZmNTlwZHdqZWwiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjU0NTU4NjN9.RAraoAlxks5CYftXQer0KZq4OTbOLnO30ENwjdXk-Rw"
```
## Buggy Response:
HTTP 200. - Not all columns in nested value are returned.
```
{
    "list": [
        {
            "Id": 1,
            "Title": "Michael",
            "nc_iyil___nc_m2m_eutsk8puooList": [
                {
                    "table2_id": 1,
                    "table1_id": 1
                }
            ],
            "coursesTaken": [
                {
                    "Id": 1,
                    "Title": "Math"
                }
            ]
        }
    ],
    "pageInfo": {
        "totalRows": 1,
        "page": 1,
        "pageSize": 25,
        "isFirstPage": true,
        "isLastPage": true
    }
}
```
## Expected Response:
HTTP 200. All columns in nested value are returned.
```
{
    "list": [
        {
            "Id": 1,
            "Title": "Alex",
            "nc_jvvl___nc_m2m_4ny0l9hde9List": [
                {
                    "table2_id": 1,
                    "table1_id": 1
                }
            ],
            "coursesTaken": [
                {
                    "Id": 1,
                    "Title": "Math",
                    "teacher": "John",
                    "nc_jvvl___nc_m2m_4ny0l9hde9List": [
                        {
                            "table2_id": 1,
                            "table1_id": 1
                        }
                    ],
                    "CoursesMMList": [
                        {
                            "Id": 1,
                            "Title": "Alex"
                        }
                    ]
                }
            ]
        }
    ],
    "pageInfo": {
        "totalRows": 1,
        "page": 1,
        "pageSize": 25,
        "isFirstPage": true,
        "isLastPage": true
    }
}
```


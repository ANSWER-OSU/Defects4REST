# Nocodb#1866

## Description:
Using lookup columns in filters or formulas causes errors (HTTP 400) indicating the API does not handle these query parameters correctly.

## GitHub Issue URL
https://github.com/nocodb/nocodb/issues/1866

## Triggering endpoints
- `/api/v1/db/meta/views/{view_id}/filters`
- `/api/v1/db/data/noco/{projectName}/{tableName}/views/{tableName}`

## Prerequisites
**Step 1.** Signin as a super user (admin)
```
curl 'http://localhost:8081/api/v1/db/auth/user/signin' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"admin@admin.com","password":"@Admin123"}'
```
**Response:** HTTP 200.
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE"
}
```
**Step 2.** Create project
```
curl -X 'POST' 'http://localhost:8081/api/v1/db/meta/projects/' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{
"title":"buggy1866"
}' | jq .
```
**Response:** HTTP 200.
```
{
  "is_meta": 1,
  "id": "p_jliccmcwokpx7x",
  "title": "buggy1866",
  "prefix": "nc_gd18__",
...
}
```
**Step 3.** Create table: "Parents"
```
curl -X "POST" 'http://localhost:8081/api/v1/db/meta/projects/p_jliccmcwokpx7x/tables' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"table_name":"nc_qmjm__parents",
"title":"Parents",
"columns":[{"column_name":"id","title":"Id","dt":"integer","dtx":"integer","ct":"int(11)","nrqd":false,"rqd":true,"ck":false,"pk":true,"un":false,"ai":true,"cdf":null,"clen":null,"np":null,"ns":0,"dtxp":"","dtxs":"","altered":1,"uidt":"ID","uip":"","uicn":""},{"column_name":"title","title":"Title","dt":"varchar","dtx":"specificType","ct":"varchar","nrqd":true,"rqd":false,"ck":false,"pk":false,"un":false,"ai":false,"cdf":null,"clen":45,"np":null,"ns":null,"dtxp":"","dtxs":"","altered":1,"uidt":"SingleLineText","uip":"","uicn":""}]}' | jq .
```
**Response:** HTTP 200.
```
{
  "id": "md_9ak2cjeqv3x3wu",
  "base_id": "ds_vr51k780reigsr",
  "project_id": "p_jliccmcwokpx7x",
  "table_name": "nc_gd18___nc_qmjm__parents",
  "title": "Parents",
...
  "columns": [
    {
      "id": "cl_gl91urp36b2mzy",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "Id",
      "column_name": "id",
      ...
    },
    {
      "id": "cl_v2sirtxhoj3aca",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "Title",
      "column_name": "title",
      "uidt": "SingleLineText",
      ...
    }
  ],
  "views": [
    {
      "id": "vw_b3l28rubimls2l",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "Parents",
      "type": 3,
      ...
      }
    }
  ],
  ...
}
```
**Step 4.** Populate data for "Parents"
```
curl -X "POST" 'http://localhost:8081/api/v1/db/data/noco/buggy1866/Parents' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"Title":"FooParents"}' | jq .
```
**Response:** HTTP 200.
```
{
  "Id": 1,
  "Title": "FooParents"
}
```
**Step 5.** Create table: "Children"
```
curl -X "POST" 'http://localhost:8081/api/v1/db/meta/projects/p_jliccmcwokpx7x/tables' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"table_name":"nc_qmjm__children",
"title":"Children",
"columns":[{"column_name":"id","title":"Id","dt":"integer","dtx":"integer","ct":"int(11)","nrqd":false,"rqd":true,"ck":false,"pk":true,"un":false,"ai":true,"cdf":null,"clen":null,"np":null,"ns":0,"dtxp":"","dtxs":"","altered":1,"uidt":"ID","uip":"","uicn":""},{"column_name":"title","title":"Title","dt":"varchar","dtx":"specificType","ct":"varchar","nrqd":true,"rqd":false,"ck":false,"pk":false,"un":false,"ai":false,"cdf":null,"clen":45,"np":null,"ns":null,"dtxp":"","dtxs":"","altered":1,"uidt":"SingleLineText","uip":"","uicn":""}]}' | jq .
```
**Response:** HTTP 200.
```
{
  "id": "md_9b02agojxpdky5",
  "base_id": "ds_vr51k780reigsr",
  "project_id": "p_jliccmcwokpx7x",
  "table_name": "nc_gd18___nc_qmjm__children",
  "title": "Children",
  "type": "table",
  ...
    {
      "id": "cl_fqgmq2nuwik9sp",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Id",
      "column_name": "id",
      "uidt": "ID",
      ...
    },
    {
      "id": "cl_t60uajwy8gdxwz",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Title",
      "column_name": "title",
      "uidt": "SingleLineText",
      "dt": "varchar",
      ...
    }
  ],
  "views": [
    {
      "id": "vw_2km51lo2ifp3ar",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Children",
      ...
    }
  ],
  ...
}
```
**Step 6.** Populate data for "Children"
```
curl -X "POST" 'http://localhost:8081/api/v1/db/data/noco/buggy1866/Children' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"Title":"BarChildren"}' | jq .
```
**Response:** HTTP 200.
```
{
  "Id": 1,
  "Title": "BarChildren"
}
```
**Step 7.** Parents: Create new column > LinkToAnotherRecord > Has Many > Children
```
curl -X "POST" 'http://localhost:8081/api/v1/db/meta/tables/md_9ak2cjeqv3x3wu/columns' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{
"parentId":"md_9ak2cjeqv3x3wu",
"childID":null,
"childColumn":"nc_qmjm__parents_id",
"childTable":"nc_qmjm__parents",
"parentTable":"",
"parentColumn":"",
"onDelete":"NO ACTION","onUpdate":"NO ACTION","updateRelation":false,"virtual":true,"childId":"md_9b02agojxpdky5","uidt":"LinkToAnotherRecord","title":"title5","type":"hm"}' | jq .
```
**Response:** HTTP 200.
```
{
  "id": "md_9ak2cjeqv3x3wu",
  "base_id": "ds_vr51k780reigsr",
  "project_id": "p_jliccmcwokpx7x",
  "table_name": "nc_gd18___nc_qmjm__parents",
  "title": "Parents",
  "type": "table",
  "meta": null,
  ...
    {
      "id": "cl_gl91urp36b2mzy",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "Id",
      "column_name": "id",
      "uidt": "ID",
      ...
    },
    {
      "id": "cl_v2sirtxhoj3aca",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "Title",
      "column_name": "title",
      "uidt": "SingleLineText",
      "dt": "varchar",
      ...
    },
    {
      "id": "cl_uv0kd65qizlnrk",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "title5",
      "column_name": null,
      "uidt": "LinkToAnotherRecord",
      ...
    }
  ],
  "views": [
    {
      "id": "vw_b3l28rubimls2l",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9ak2cjeqv3x3wu",
      "title": "Parents",
      "type": 3,
      ...
    }
  ],
  ...
}
```
**Step 8.** Children: Create new column "lookup_child_name" > Lookup > Child table: "Parents" > Child column: "Title"

**Step 8a.** Get ID for Children>ParentsRead first
```
curl 'http://localhost:8081/api/v1/db/meta/views/vw_2km51lo2ifp3ar/columns' \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' | jq .
```
**Response:** HTTP 200.
```
[
  {
    "id": "nc_ojou1f4h4wl5zs",
    ...
  },
  {
    "id": "nc_2ys6qs9jqzlns0",
    ...
  },
  {
    "id": "nc_t0n11a3wk7tnoe",
    ...
  },
  {
    "id": "nc_iz4f32rqshqz5g", 
    "fk_view_id": "vw_2km51lo2ifp3ar",
    "fk_column_id": "cl_v1ewvd1n2sk8d7", // <- this one
    "base_id": "ds_vr51k780reigsr",
    "project_id": "p_jliccmcwokpx7x",
    ...
  }
]
```
**Step 8b.** Create lookup column
```
curl -X "POST" 'http://localhost:8081/api/v1/db/meta/tables/md_9b02agojxpdky5/columns' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"title":"lookup_child_name","fk_relation_column_id":"cl_v1ewvd1n2sk8d7","fk_lookup_column_id":"cl_v2sirtxhoj3aca","uidt":"Lookup"}' | jq .
```
Note: `fk_relation_column_id` is ID for ParentsRead column in Children. 

**Response:** HTTP 200.
```
{
  "id": "md_9b02agojxpdky5",
  "base_id": "ds_vr51k780reigsr",
  "project_id": "p_jliccmcwokpx7x",
  "table_name": "nc_gd18___nc_qmjm__children",
  "title": "Children",
  "type": "table",
  "meta": null,
  "schema": null,
  ...
  "columns": [
    {
      "id": "cl_fqgmq2nuwik9sp",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Id",
      "column_name": "id",
      "uidt": "ID",
      ...
    },
    {
      "id": "cl_t60uajwy8gdxwz",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Title",
      "column_name": "title",
      ...
    },
    {
      "id": "cl_d4kw7kj4utuz6f",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "nc_gd18___nc_qmjm__parents_id",
      "column_name": "nc_gd18___nc_qmjm__parents_id",
      "uidt": "ForeignKey",
      "dt": "integer",
      ...
    },
    {
      "id": "cl_v1ewvd1n2sk8d7",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "ParentsRead",
      "column_name": null,
      "uidt": "LinkToAnotherRecord",
      ...
    },
    {
      "id": "cl_w824o6l954c3ia",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "lookup_child_name",
      "column_name": null,
      "uidt": "Lookup",
      "dt": null,
      ...
    }
  ],
  "views": [
    {
      "id": "vw_2km51lo2ifp3ar",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Children",
      "type": 3,
      "is_default": 1,
      ...
    }
  ],
  ...
}
```
## Triggering Behavior
**Step 9.** Children: Create new column "formula" > Formula > {lookup_child_name}

`/api/v1/db/meta/tables/{table_id}/columns`
```
curl -X "POST" 'http://localhost:8081/api/v1/db/meta/tables/md_9b02agojxpdky5/columns' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"title":"formula","uidt":"Formula","formula_raw":"{lookup_child_name}"}' | jq .
```
**Response:** HTTP 200.
```
{
  "id": "md_9b02agojxpdky5",
  "base_id": "ds_vr51k780reigsr",
  "project_id": "p_jliccmcwokpx7x",
  "table_name": "nc_gd18___nc_qmjm__children",
  "title": "Children",
  "type": "table",
  "meta": null,
  ...
  "columns": [
    {
      "id": "cl_fqgmq2nuwik9sp",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Id",
      "column_name": "id",
      "uidt": "ID",
      ...
    },
    {
      "id": "cl_t60uajwy8gdxwz",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Title",
      "column_name": "title",
      ...
    },
    {
      "id": "cl_d4kw7kj4utuz6f",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "nc_gd18___nc_qmjm__parents_id",
      "column_name": "nc_gd18___nc_qmjm__parents_id",
      ...
    },
    {
      "id": "cl_v1ewvd1n2sk8d7",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "ParentsRead",
      "column_name": null,
      "uidt": "LinkToAnotherRecord",
      ...
      }
    },
    {
      "id": "cl_w824o6l954c3ia",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "lookup_child_name",
      "column_name": null,
      "uidt": "Lookup",
      ...
      }
    },
    {
      "id": "cl_b5bnw3hnwv3f3e",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "formula",
      "column_name": null,
      "uidt": "Formula",
      ...
      }
    }
  ],
  "views": [
    {
      "id": "vw_2km51lo2ifp3ar",
      "base_id": "ds_vr51k780reigsr",
      "project_id": "p_jliccmcwokpx7x",
      "fk_model_id": "md_9b02agojxpdky5",
      "title": "Children",
      "type": 3,
      "is_default": 1,
     ...
    }
  ],
  ...
}
```
**Step 10.** Set filter in 'Children' table where 'formula' is not empty.

**Step 10a.** Create filter

`/api/v1/db/meta/views/{view_id}/filters`
```
curl -X POST 'http://localhost:8081/api/v1/db/meta/views/vw_2km51lo2ifp3ar/filters' \
-H "Content-Type: application/json" \
-H 'accept: application/json' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' \
-d '{"fk_column_id":"cl_b5bnw3hnwv3f3e","comparison_op":"notempty","value":"","status":"update","logical_op":"and"}' | jq .
```
**Response:** HTTP 200.
```
{"id":"fi_u1mspllkj90gf3","base_id":"ds_vr51k780reigsr","project_id":"p_jliccmcwokpx7x","fk_view_id":"vw_2km51lo2ifp3ar","fk_hook_id":null,"fk_column_id":"cl_b5bnw3hnwv3f3e","fk_parent_id":null,"logical_op":"and","comparison_op":"eq","value":"","is_group":null,"order":1,"created_at":"2025-12-02 14:10:02","updated_at":"2025-12-02 14:10:02"}
```
**Step 10b.** Get filter

`/api/v1/db/data/noco/{project_name}/Children/views/Children`
```
curl -X GET 'http://localhost:8081/api/v1/db/data/noco/buggy1866/Children/views/Children' \
-H 'xc-auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImZpcnN0bmFtZSI6bnVsbCwibGFzdG5hbWUiOm51bGwsImlkIjoidXNfdG5jMnUxbGt4aWVlOXgiLCJyb2xlcyI6InVzZXIsc3VwZXIiLCJpYXQiOjE3NjQ2ODMwODl9.fMiJz51i9ag2i75gEu8_FYnq0S9gcBzcr9WSReMljPE' | jq .
```
## Buggy Response:
HTTP 400.
```
{
  "msg": "select * from (select (select `__nc_formula0`.`title` from `nc_gd18___nc_qmjm__parents` as `__nc_formula0` where `__nc_formula0`.`id` = `nc_gd18___nc_qmjm__children`.`nc_gd18___nc_qmjm__parents_id`) as `formula`, `nc_gd18___nc_qmjm__children`.`id` as `Id`, `nc_gd18___nc_qmjm__children`.`title` as `Title`, `nc_gd18___nc_qmjm__children`.`nc_gd18___nc_qmjm__parents_id` as `nc_gd18___nc_qmjm__parents_id` from `nc_gd18___nc_qmjm__children` where ((((not `` = (select `__nc_formula0`.`title` from `nc_gd18___nc_qmjm__parents` as `__nc_formula0` where `__nc_formula0`.`id` = `nc_gd18___nc_qmjm__children`.`nc_gd18___nc_qmjm__parents_id`))))) order by `id` asc limit 25) __nc_alias - SQLITE_ERROR: no such column: "
}
```
## Expected Response:
HTTP 200.
```
{
  "list": [],
  "pageInfo": {
    "totalRows": 0,
    "page": 1,
    "pageSize": 25,
    "isFirstPage": true,
    "isLastPage": true
  }
}
```

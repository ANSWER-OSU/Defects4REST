## Restcountries#116

## Description

The issue reports incorrect country name translation returned by the API when queried for Morocco in Arabic.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/116](https://github.com/apilayer/restcountries/issues/116)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query the country data and verify that the translations object contains the **fa** field for the target country:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq '{fa: (.[] | select(.name=="Morocco") | .translations.fa)}'
```

**Buggy Response:** HTTP 200 with incorrect Arabic translation

```json
{
  "fa": "مراکش"
}
```

**Expected Response:** HTTP 200 with correct Arabic translation

```json
{
  "fa": "المغرب"
}
```

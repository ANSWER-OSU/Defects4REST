## Restcountries#209

## Description

The API incorrectly lists the United Kingdom as a member of the European Union. Although the UK officially left the EU in **2020**, the API still returns `"EU"` in the `regionalBlocs` field of the UK object.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/209](https://github.com/apilayer/restcountries/issues/209)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the UK object with `regionalBlocs`:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"GBR\") | {name: .name, alpha2Code: .alpha2Code, alpha3Code: .alpha3Code, regionalBlocs: (.regionalBlocs // [])}"
```

**Buggy Response:** HTTP 200 but UK incorrectly listed as EU

```json
{
  "name": "United Kingdom of Great Britain and Northern Ireland",
  "alpha2Code": "GB",
  "alpha3Code": "GBR",
  "regionalBlocs": [
    {
      "acronym": "EU",
      "name": "European Union",
      "otherAcronyms": [],
      "otherNames": []
    }
  ]
}
```

**Expected Response:** HTTP 200 and UK no longer in EU

```json
{
  "name": "United Kingdom of Great Britain and Northern Ireland",
  "alpha2Code": "GB",
  "alpha3Code": "GBR",
  "regionalBlocs": []
}
```


## Restcountries#184

## Description

The API endpoint for EU regional bloc returns incorrect results by including Faroe Islands, which are not part of the EU.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/184](https://github.com/apilayer/restcountries/issues/184)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the `regionalBlocs` value for **Faroe Islands (FRO)**:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"FRO\") | {regionalBlocs: .regionalBlocs}"
```

**Buggy Response:** HTTP 200, but incorrectly indicates EU membership

```json
{
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

**Expected Response:** HTTP 200 and should not show EU membership

```json
{
  "regionalBlocs": null
}
```


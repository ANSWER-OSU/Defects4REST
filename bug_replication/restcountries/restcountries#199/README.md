## Restcountries#199

## Description

The API returns an incorrect country name (North Macedonia) for a valid country code, indicating a problem with how country data is retrieved or mapped based on query parameters.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/199](https://github.com/apilayer/restcountries/issues/199)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the name fields for **North Macedonia (MKD)**:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"MKD\") | {name: .name, nativeName: .nativeName}"
```

**Buggy Response:** HTTP 200, but with outdated country name

```json
{
  "name": "Macedonia (the former Yugoslav Republic of)",
  "nativeName": "Македонија"
}
```

**Expected Response:** HTTP 200 and shows recognized/updated name

```json
{
  "name": "North Macedonia",
  "nativeName": "северна Македонија"
}
```


## Restcountries#221

## Description

The API returns an incorrect native name for Luxembourg, indicating a problem with how country name data is filtered or selected for the response.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/221](https://github.com/apilayer/restcountries/issues/221)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the name and native name for Luxembourg:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"LUX\") | {name: .name, nativeName: .nativeName}"
```

**Buggy Response:** HTTP 200 but with incorrect native name

```json
{
  "name": "Luxembourg",
  "nativeName": "Luxembourg"
}
```

**Expected Response:** HTTP 200 with correct native name

```json
{
  "name": "Luxembourg",
  "nativeName": "Lëtzebuerg"
}
```


## Restcountries#156

## Description

The API returns incorrect data for the capital field when queried for Vatican City, indicating an error in handling or returning search parameters.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/156](https://github.com/apilayer/restcountries/issues/156)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query Vatican City’s country data and extract the `capital` field:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"VAT\") | {capital: .capital}"
```

**Buggy Response:** HTTP 200 with incorrect capital

```json
{
  "capital": "Rome"
}
```

**Expected Response:** HTTP 200 with the correct capital

```json
{
  "capital": "Vatican City"
}
```


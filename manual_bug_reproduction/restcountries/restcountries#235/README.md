## Restcountries#235

## Description
The issue reports that the API returns the outdated capital name Kiev instead of the correct Kyiv indicating incorrect handling or mapping of country data in response to query parameters.


## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/235](https://github.com/apilayer/restcountries/issues/235)

## Triggering Endpoints:

* `/v2/alpha/{code}`

## Triggering Behavior:

**Step 1.** Query the country data for Kyiv and check the capital

```bash
curl -s http://localhost:8080/restcountries/rest/v2/alpha/UKR | jq '.capital'
```

**Buggy Response:** HTTP 200 with incorrect capital name

```json
"capital":["Kiev"]
```

**Expected Response:** HTTP 200 with correct capital name

```json
"capital":["Kyiv"]
```


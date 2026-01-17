## Restcountries#226

## Description

The API returns incorrect border country codes for Kuwait, indicating an error in how country border data is queried or filtered.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/226](https://github.com/apilayer/restcountries/issues/226)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query the country data for **Kuwait** and check the borders:

```bash
curl -s http://localhost:8080/restcountries/rest/v2/alpha/KW | jq '.borders'
```

**Buggy Response:** HTTP 200 but with incorrect border

```json
["IRN", "SAU"]
```

**Expected Response:** HTTP 200 with correct border

```json
["IRQ", "SAU"]
```


## Restcountries#201

## Description

The API returns an incorrect timezone for Tbilisi, Georgia, indicating a misconfiguration of environment-specific data.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/201](https://github.com/apilayer/restcountries/issues/201)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Use `curl` to query the country data for **Georgia**:

```bash
curl http://localhost:8080/restcountries/rest/v2/alpha/GE | jq
```

**Buggy Response:** HTTP 200, but with wrong timezone

```json
"timezones": [
    "UTC-05:00"
]
```

**Expected Response:** HTTP 200 and shows correct timezone

```json
"timezones": [
    "UTC+04:00"
]
```


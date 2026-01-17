## Restcountries#202

## Description

The API returns an incomplete list of bordering countries for **Brazil (BRA)**. Although Brazil borders **French Guiana (FRA)**, the current response does not include France (FRA) in the `borders` field. For comparison, neighboring country **Suriname (SUR)** correctly lists France as a border.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/202](https://github.com/apilayer/restcountries/issues/202)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the `borders` for Brazil:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/alpha/SUR" | jq "{borders: .borders}"
```

**Buggy Response:** HTTP 200, but **France (FRA)** missing

```json
{
  "borders": [
    "ARG",
    "BOL",
    "COL",
    "GUF",
    "GUY",
    "PRY",
    "PER",
    "SUR",
    "URY",
    "VEN"
  ]
}
```

**Expected Response:** HTTP 200 and includes **France (FRA)**

```json
{
  "borders": [
    "ARG",
    "BOL",
    "COL",
    "FRA",
    "GUF",
    "GUY",
    "PRY",
    "PER",
    "SUR",
    "URY",
    "VEN"
  ]
}
```


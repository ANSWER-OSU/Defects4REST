## Restcountries#120

## Description

The API response for Chad's borders omits Sudan, indicating an error in how border data is queried or filtered for this country.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/120](https://github.com/apilayer/restcountries/issues/120)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query Chad’s country data and extract the `borders` field:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"TCD\") | {borders: .borders}"
```

**Buggy Response:** HTTP 200 with missing Sudan (`SDN`) in the borders array:

```json
{
  "borders": [
    "CMR",
    "CAF",
    "LBY",
    "NER",
    "NGA",
    "SSD"
  ]
}
```

**Expected Response:** HTTP 200 with Sudan (`SDN`) correctly included

```json
{
  "borders": [
    "CMR",
    "CAF",
    "LBY",
    "NER",
    "NGA",
    "SDN"
  ]
}
```


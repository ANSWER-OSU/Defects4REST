## Restcountries#237

## Description

The API returns inconsistent border data. While Nepal correctly lists China and India as bordering countries, and India lists both Nepal and China, China incorrectly omits Nepal from its list of borders. This results in inaccurate and non-reciprocal geographic information.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/237](https://github.com/apilayer/restcountries/issues/237)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query to check the borders of China:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"CHN\") | {borders: .borders}"
```

**Buggy Response:** HTTP 200 but with incomplete border, Nepal (NPL) missing

```json
{
  "borders": [
    "AFG",
    "BTN",
    "MMR",
    "HKG",
    "IND",
    "KAZ",
    "PRK",
    "KGZ",
    "LAO",
    "MAC",
    "MNG",
    "PAK",
    "RUS",
    "TJK",
    "VNM"
  ]
}
```

**Expected Response:** HTTP 200 with correct border, Nepal (NPL) included

```json
{
  "borders": [
    "AFG",
    "BTN",
    "MMR",
    "HKG",
    "IND",
    "NPL",
    "KAZ",
    "PRK",
    "KGZ",
    "LAO",
    "MAC",
    "MNG",
    "PAK",
    "RUS",
    "TJK",
    "VNM"
  ]
}
```


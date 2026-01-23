## Restcountries#249

## Description

The API returns an outdated country name for Eswatini, which leads to incorrect query and search results for users.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/249](https://github.com/apilayer/restcountries/issues/249)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the name and native name for Eswatini:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"SWZ\") | {name: .name, nativeName: .nativeName}"
```

**Buggy Response:** HTTP 200 but with outdated name

```json
{
  "name": "Swaziland",
  "nativeName": "Swaziland"
}
```

**Expected Response:** HTTP 200 with correct official name

```json
{
  "name": "Eswatini",
  "nativeName": "eSwatini"
}
```


## Restcountries#177

## Description

The API response for Antarctica omits expected currencies and languages, indicating incomplete or inconsistent configuration for this specific region.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/177](https://github.com/apilayer/restcountries/issues/177)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query Antarctica’s country data and extract the `currencies` and `languages` fields:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"ATA\") | {currencies: .currencies, languages: .languages}"
```

**Buggy Response:** HTTP 200 with incorrect currencies

```json
{
  "currencies": [
    {
      "code": "AUD",
      "name": "Australian dollar",
      "symbol": "$"
    },
    {
      "code": "GBP",
      "name": "British pound",
      "symbol": "£"
    }
  ],
  "languages": [
    {
      "iso639_1": "en",
      "iso639_2": "eng",
      "name": "English",
      "nativeName": "English"
    },
    {
      "iso639_1": "ru",
      "iso639_2": "rus",
      "name": "Russian",
      "nativeName": "Русский"
    }
  ]
}
```

**Expected Response:** HTTP 200 with the correct currencies (should be empty)

```json
{
  "currencies": null,
  "languages": [
    {
      "iso639_1": "en",
      "iso639_2": "eng",
      "name": "English",
      "nativeName": "English"
    },
    {
      "iso639_1": "ru",
      "iso639_2": "rus",
      "name": "Russian",
      "nativeName": "Русский"
    }
  ]
}
```

## Restcountries#118

## Description

The API returns incorrect language data for Aruba and Curaçao, indicating a misconfiguration of the country-language mapping.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/118](https://github.com/apilayer/restcountries/issues/118)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all country data and filter for the incorrect Punjabi language entry using `jq`:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".. | objects | select(.iso639_1==\"pa\")"
```

**Buggy Response:** HTTP 200 showing incorrect language entry

```json
{
  "iso639_1": "pa",
  "iso639_2": "pan",
  "name": "(Eastern) Punjabi",
  "nativeName": "ਪੰਜਾਬੀ"
}
{
  "iso639_1": "pa",
  "iso639_2": "pan",
  "name": "(Eastern) Punjabi",
  "nativeName": "ਪੰਜਾਬੀ"
}
```

**Expected Response:** HTTP 200 without any Punjabi entry, showing the correct Caribbean language

```json
{
  "iso639_1": "",
  "iso639_2": "pap",
  "name": "Papiamento",
  "nativeName": "Papiamentu"
}
{
  "iso639_1": "",
  "iso639_2": "pap",
  "name": "Papiamento",
  "nativeName": "Papiamentu"
}
```

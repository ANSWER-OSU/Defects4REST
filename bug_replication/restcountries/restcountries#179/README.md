## Restcountries#179

## Description

The API returns an incorrect list of time zones for France instead of the expected single value, indicating a configuration or data mapping issue.

## GitHub Issue URL

[https://github.com/apilayer/restcountries/issues/179](https://github.com/apilayer/restcountries/issues/179)

## Triggering Endpoints:

* `/v2/all`

## Triggering Behavior:

**Step 1.** Query all countries and extract the time zones for **France (FRA)**:

```bash
curl -s "http://localhost:8080/restcountries/rest/v2/all" | jq ".[] | select(.alpha3Code==\"FRA\") | {timezones: .timezones}"
```

**Buggy Response:** HTTP 200, but missing time zone

```json
{
  "timezones": [
    "UTC-10:00",
    "UTC-09:30",
    "UTC-09:00",
    "UTC-08:00",
    "UTC-04:00",
    "UTC-03:00",
    "UTC+01:00",
    "UTC+03:00",
    "UTC+04:00",
    "UTC+05:00",
    "UTC+11:00",
    "UTC+12:00"
  ]
}
```

**Expected Response:** HTTP 200 with the correct time zones(UTC+10:00 included)

```json
{
  "timezones": [
    "UTC-10:00",
    "UTC-09:30",
    "UTC-09:00",
    "UTC-08:00",
    "UTC-04:00",
    "UTC-03:00",
    "UTC+01:00",
    "UTC+03:00",
    "UTC+04:00",
    "UTC+05:00",
    "UTC+10:00",
    "UTC+11:00",
    "UTC+12:00"
  ]
}
```


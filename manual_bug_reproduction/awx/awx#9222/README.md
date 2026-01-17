## awx#9222

## Description


API returns a 500 error when an unsupported query parameter modifier is used instead of a proper 4xx error.

## GitHub Issue URL

[
https://github.com/ansible/awx/issues/9222
](
https://github.com/ansible/awx/issues/9222
)

## Triggering Endpoints:

* `/api/v2/jobs/{id}`

## Triggering Behavior:

**Step 1.** Send a request with _iexact=1 filter

```bash
curl "http://localhost:8052/api/v2/jobs/?id__iexact=1" -u admin:password -v
```

**Buggy Response:** Throws 500 error

**Expected Response:** iexact isn't supported on the id field, so API should throw 4xx error that says that modifier is not supported.

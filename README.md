# pr-review-sandbox

A small Python 3.12 + FastAPI project for testing AI PR review tools.

## Endpoints

- `GET /users/{id}`
- `POST /payments/charge`
- `POST /payments/refund`
- `GET /admin/audit-log` with `X-Role: admin`

The app uses in-memory data only. It does not include real secrets, external services, payment SDKs, or network calls.

## Development

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest
```

# pr-review-sandbox

A small Python 3.12 + FastAPI project for testing AI PR review tools.

## Endpoints

- `GET /users/{id}`
- `POST /payments/charge`
- `POST /payments/refund`
- `GET /admin/audit-log` with `X-Role: admin`

## API Usage Notes

All API examples use local in-memory data and are intended for sandbox testing only.

- User IDs `1` and `2` are available in the default data set.
- Payment charge and refund calls mutate only the in-memory process state.
- The audit log endpoint is read-only and requires the `X-Role: admin` header.

The app uses in-memory data only. It does not include real secrets, external services, payment SDKs, or network calls.

## Development

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest
```

## Frontend

```bash
cd frontend
npm install
npm test
npm run build
```

During development, run the FastAPI app on `127.0.0.1:8000` and start Vite with `npm run dev`.

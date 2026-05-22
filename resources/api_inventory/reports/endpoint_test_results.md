# Endpoint Test Results

- Generated at: `2026-05-22T22:52:40.824247+00:00`
- Tested endpoint method cases: `3`

| Method | Path | Transport | Status | Note |
|---|---|---|---:|---|
| `GET` | `/api/query` | `query_params` | `200` | standard documented query form |
| `POST` | `/api/query` | `form_body` | `200` | supported live POST shape |
| `POST` | `/api/query` | `query_params_only` | `400` | returns HTTP 400; avoid this form |

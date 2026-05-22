# arXiv API Inventory

This inventory captures the current public arXiv metadata query surface used by `arxiv_cli`.

## Endpoints

- `GET /api/query`
- `POST /api/query`

## Notes

- The endpoint is public and does not require auth.
- Normal and error bodies are Atom XML.
- GET is the standard documented form; POST works when fields are form-encoded in the body.

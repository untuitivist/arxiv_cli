# C_fetch_by_id_or_query

Goal: fetch exact records once promising ids or search terms are known.

Recommended sequence:

- use `arxiv paper get ...` for exact id retrieval
- use `arxiv query run ...` when you need endpoint-native arguments
- use `POST` only when intentionally testing the endpoint form-body behavior

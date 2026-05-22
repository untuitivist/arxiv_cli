# GET|POST /api/query

## Summary

- URL: `https://export.arxiv.org/api/query`
- Methods: `GET`, `POST`
- Response format: `application/atom+xml` (Atom 1.0 XML)

## Query Logic

The search_query parameter accepts a search expression used to find articles, while id_list accepts a comma-delimited list of arXiv ids. If only search_query is present, the API returns matching articles. If only id_list is present, the API returns the listed articles. If both are present, the API returns only the listed articles that also match search_query.

## Paging

start is a 0-based offset of the first returned result. max_results controls how many results are returned. The manual recommends a 3 second delay between repeated calls, limits max_results to 30000 overall, and advises retrieving slices of at most 2000 at a time.

## Sorting

sortBy can be relevance, lastUpdatedDate, or submittedDate. sortOrder can be ascending or descending.

## Rate Limits

When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request every three seconds, and limit requests to a single connection at a time.

# API Documentation

- API Access: https://info.arxiv.org/help/api/index.html
- API Basics: https://info.arxiv.org/help/api/basics.html
- API User Manual: https://info.arxiv.org/help/api/user-manual.html
- API Terms of Use: https://info.arxiv.org/help/api/tou.html

## Extracted guidance

- Query logic: The search_query parameter accepts a search expression used to find articles, while id_list accepts a comma-delimited list of arXiv ids. If only search_query is present, the API returns matching articles. If only id_list is present, the API returns the listed articles. If both are present, the API returns only the listed articles that also match search_query.
- Paging: start is a 0-based offset of the first returned result. max_results controls how many results are returned. The manual recommends a 3 second delay between repeated calls, limits max_results to 30000 overall, and advises retrieving slices of at most 2000 at a time.
- Sorting: sortBy can be relevance, lastUpdatedDate, or submittedDate. sortOrder can be ascending or descending.
- Response format: Everything returned by the API in HTTP response bodies, including errors, is Atom 1.0 XML.
- Rate limits: When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request every three seconds, and limit requests to a single connection at a time.

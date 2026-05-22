# query/run

Call the `/api/query` endpoint with arguments that closely match the native API surface.

Examples:

```powershell
arxiv query run --search-query "all:\"graph neural network\"" --max-results 5
arxiv query run --id 1706.03762 --id 2401.10401 --method POST --dry-run --format text
```
